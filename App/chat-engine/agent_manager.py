"""
# App/chat-engine/agent_manager.py
This module manages the agent for interacting with project documents.
It uses LangChain to create a retriever that can search and rerank documents,
generate PlantUML diagrams, and handle user queries effectively.
"""

import os
import torch
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_postgres import PGVector
from langchain.chains import LLMChain
from langchain_core.documents import Document
from langchain.retrievers.document_compressors.base import BaseDocumentCompressor
from langchain_core.callbacks import BaseCallbackHandler
from langchain.retrievers import ContextualCompressionRetriever
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

from utils.helpers import *
from utils.tools import *

from pydantic import Field
from typing import List, Optional, Sequence
from concurrent.futures import ThreadPoolExecutor

retriever_prompt_template = """Given the query:\n{query}\n\n
Rate the relevance of the following document to the query on a scale from 1 to 10:\n{document}\n\n
Only output the score as an integer.
"""

batch_retriever_prompt_template = """Given the query:\n{query}\n\n
Rate the relevance of the following documents to the query on a scale from 1 to 10:\n{documents}\n\n
Only output the scores as a list of integers.
"""

system_message = (
            "You are an expert assistant. Use the provided context from project documents to answer the user's question. "
            "The topic is a software project with various documents including code, design, and architecture. "
            "The application is called 'Eprice' and is a web application for viewing market electricity prices. "
            "You have access to tools to search the project documents, retrieve files by name, and generate PlantUML diagrams from code or files. "
            "Always first use the project_search tool to retrieve relevant information from the project documents. "
            "Only if this does not provide sufficient information, then try looking up individual files using the get_file_by_name tool. "
            "You can also use the get_project_directory_structure tool to understand the project structure and see what files are available. "
            "You also have access to tools to generate PlantUML diagrams from code or files. "
            "When appropriate, you can use these tools to generate diagrams to give a visual representation of the information. "
            "If the answer is not in the documents/files, state that the documents do not contain the answer. "
            "If the answer is in the documents/files, provide it and reference the document(s) used. "
            "Do not make up information. "
        )


class LLMRerankerParallel(BaseDocumentCompressor):
    llm_chain: object = Field(LLMChain, description="LLM chain to rerank documents in parallel")
    document_variable_name: str = "document"
    top_k: int = 10  # Number of top documents to return

    def _score_document(self, doc, query):
        inputs = {
            "query": query,
            self.document_variable_name: [doc.page_content],
        }
        output = self.llm_chain.invoke(inputs)
        try:
            score = int(output.strip())
        except Exception:
            score = 0
        return (doc, score)

    def compress_documents(
        self,
        documents: Sequence[Document],
        query: str,
        callbacks: Optional[list] = None,
    ) -> List[Document]:
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(lambda doc: self._score_document(doc, query), documents))
        results.sort(key=lambda x: x[1], reverse=True)
        return [doc for doc, _ in results[:self.top_k]]

class LLMRerankerBatched(BaseDocumentCompressor):
    llm_chain: object = Field(LLMChain, description="LLM chain to rerank documents")
    document_variable_name: str = "documents"
    top_k: int = 10  # Number of top documents to return

    def compress_documents(
        self,
        documents: Sequence[Document],
        query: str,
        callbacks: Optional[list] = None,
    ) -> List[Document]:
        inputs = {
            "query": query,
            self.document_variable_name: [doc.page_content for doc in documents],
        }
        output = self.llm_chain.invoke(inputs)
        try:
            scores = [int(score.strip()) for score in output.split(",")]
        except Exception:
            scores = [0] * len(documents)
        scored_docs = list(zip(documents, scores))
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        return [doc for doc, score in scored_docs[:self.top_k]]
    
class Embedder:
    def __init__(self, model_name: str = "BAAI/bge-small-en"):
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={"device": self.device},
            encode_kwargs={"normalize_embeddings": True},
        )

    def embed_query(self, text: str):
        return self.embedding_model.embed_query(text)

    def count_tokens(self, text: str) -> int:
        return len(self.embedding_model.tokenizer.encode(text, add_special_tokens=False))

class VectorStore:
    def __init__(self, collection_name, connection_string, embeddings, async_mode=True):
        self.vector_store = PGVector(
            embeddings=embeddings.embedding_model,
            collection_name=collection_name,
            connection=connection_string,
            async_mode=async_mode,
        )

    def as_retriever(self, search_kwargs=None):
        if search_kwargs is None:
            search_kwargs = {"k": 20}
        return self.vector_store.as_retriever(search_kwargs=search_kwargs)

class RerankingRetriever:
    def __init__(
        self,
        vector_store,
        reranker_model_name="gpt-4o-mini",
        rerank_top_k=10,
        retriever_k=20,
    ):
        self.base_retriever = vector_store.as_retriever(search_kwargs={"k": retriever_k})
        self.rerank_prompt = PromptTemplate(
            input_variables=["query", "document"],
            template=retriever_prompt_template,
        )
        self.llm_reranker = ChatOpenAI(
            model_name=reranker_model_name,
            temperature=0.0
        )
        self.reranker_batched = LLMRerankerParallel(
            llm_chain=self.rerank_prompt | self.llm_reranker,
            top_k=rerank_top_k
        )
        self.retriever = ContextualCompressionRetriever(
            base_retriever=self.base_retriever,
            base_compressor=self.reranker_batched,
        )

    def as_tool(self, name="project_search", description="Searches the project documents for relevant information."):
        return create_retriever_tool(
            self.retriever,
            name=name,
            description=description
        )

class AgentManager:
    def __init__(self, config=None):
        self.config = config or {}
        self._setup_env()
        self._setup_embeddings()
        self._setup_vector_store()
        self._setup_retriever()
        self._setup_tools()
        self._setup_agent()
        self.max_history = 10
        self.chat_history = []

    def _setup_env(self):
        self.PGHOST = os.getenv("PGHOST", "localhost")
        self.PGPORT = os.getenv("PGPORT")
        self.PGUSER = os.getenv("PGUSER")
        self.PGPASSWORD = os.getenv("PGPASSWORD")
        self.PGDATABASE = os.getenv("PGDATABASE")
        self.connection_string = f"postgresql+psycopg://{self.PGUSER}:{self.PGPASSWORD}@{self.PGHOST}:{self.PGPORT}/{self.PGDATABASE}"
        self.collection_name = "project_documents"

    def _setup_embeddings(self):
        self.embedding_model = Embedder(model_name="BAAI/bge-small-en")

    def _setup_vector_store(self):
        self.vector_store = VectorStore(
            collection_name=self.collection_name,
            connection_string=self.connection_string,
            embeddings=self.embedding_model,
            async_mode=True,
        )

    def _setup_retriever(self):
        self.reranking_retriever = RerankingRetriever(
            vector_store=self.vector_store,
            reranker_model_name="gpt-4o-mini",
            rerank_top_k=10,
            retriever_k=20
        )

    def _setup_tools(self):
        retriever_tool = self.reranking_retriever.as_tool(
            name="project_search",
            description="Searches the project documents for relevant information."
        )
        self.tools = [retriever_tool,
                      get_file_by_name_tool,
                      generate_plantuml_diagram_from_file_tool,
                      generate_plantuml_diagram_from_code_tool,
                      get_project_directory_structure_tool]

    def _setup_agent(self):
        self.llm_streaming = ChatOpenAI(
            model="gpt-4o",
            temperature=0.2,
            streaming=True,
        )
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm_streaming,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=False,
            system_message=system_message,
        )
    
    def _add_to_history(self, user_input, ai_output):
        self.chat_history.append(HumanMessage(content=user_input))
        self.chat_history.append(AIMessage(content=ai_output))
        while len(self.chat_history) > self.max_history * 2:
            self.chat_history.pop(0)

    def _history_as_string(self, new_message):
        history_str = ""
        for message in self.chat_history:
            if isinstance(message, HumanMessage):
                history_str += f"User: {message.content}\n"
            elif isinstance(message, AIMessage):
                history_str += f"AI: {message.content}\n"
        history_str += f"User: {new_message}\n"
        return history_str

    async def stream_response(self, query: str, mem: bool = True):
        messages = self._history_as_string(query) if mem else query
        response = ""
        async for chunk in self.agent.astream(messages):
            content = None
            if hasattr(chunk, "content") and isinstance(chunk.content, str) and chunk.content.strip():
                content = chunk.content
            elif isinstance(chunk, dict):
                if "output" in chunk and isinstance(chunk["output"], str) and chunk["output"].strip():
                    content = chunk["output"]
                elif "content" in chunk and isinstance(chunk["content"], str) and chunk["content"].strip():
                    content = chunk["content"]
            elif isinstance(chunk, str) and chunk.strip():
                content = chunk
            if content:
                response += content
                yield response
        # After streaming, add to history
        if mem:
            self._add_to_history(query, response)
        
