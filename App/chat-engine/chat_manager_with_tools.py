"""
App/chat-engine/agent_manager.py
This module manages the agent for interacting with project documents.
It uses a language model to rerank documents based on relevance to a query,
and provides tools for searching and retrieving files from the project directory.
"""


import os
import torch
from transformers import AutoModel, AutoTokenizer
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_postgres import PGVector
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain.retrievers import ContextualCompressionRetriever
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.retrievers import ContextualCompressionRetriever
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.retrievers.document_compressors.base import BaseDocumentCompressor
from langchain.tools.retriever import create_retriever_tool
from langchain_core.documents import Document


from pydantic import Field
from typing import List, Optional, Sequence, Dict, Any
import json

from utils.tools import (
    get_file_by_name_tool,
    get_project_directory_structure_tool,
)

retriever_prompt_template = """Given the query:\n{query}\n\n
Rate the relevance of the following document to the query on a scale from 1 to 10:\n{document}\n\n
Only output the score as an integer.
"""

batch_retriever_prompt_template = """Given the query:\n{query}\n\n
Rate the relevance of the following documents to the query on a scale from 1 to 10:\n{documents}\n\n
Only output the scores as a list of integers.
"""

system_message = (
            "You are an expert assistant for answering questions about a software project named 'Eprice'.\n"
            "You have access to the following tools:\n"
            "- project_search: args: {\"query\": <string>}\n"
            "- get_file_by_name: args: {\"file_name\": <string>}\n"
            "- get_project_directory_structure: args: {}\n"
            "Always first use the project_search tool to retrieve relevant information from the project documents.\n"
            "If project_search does not provide sufficient information, then try looking up individual files using get_file_by_name.\n"
            "You can use get_project_directory_structure to understand the project structure and see what files are available.\n"
            "Be pro-active in using these tools to find the information needed to answer the user's question.\n"
            "If you get name conflicts when you use get_file_by_name tool, try using the full file name with path.\n"
            "If the answer is in the documents or files, provide it and reference the document(s) or file(s) used.\n"
            "If the answer is not in the documents or files, state that the documents do not contain the answer.\n"
            "To use a tool, respond ONLY with a JSON block in this format:\n"
            '{"tool": "tool_name", "args": {"arg1": "value1", ...}}.\n'
            "Do not include any explanation or extra text outside the JSON block when calling a tool.\n"
            "Otherwise, answer the user's question directly and clearly."
        )

class LLMReranker(BaseDocumentCompressor):
    """LLM Reranker that uses LLMChain to rerank documents.
    It passes each document to the LLM and expects the LLM to return a score for each document.
    The documents are then sorted by score and the top_k documents are returned.
    """
    llm_chain: object = Field(LLMChain, description="LLM chain to rerank documents")
    document_variable_name: str = "document"
    top_k: int = 5  # Number of top documents to return

    def compress_documents(
        self,
        documents: Sequence[Document],
        query: str,
        *,
        callbacks: Optional[list] = None,
    ) -> List[Document]:
        
        scored_docs = []
        for doc in documents:
            inputs = {
                "query": query,
                self.document_variable_name: doc.page_content,
            }
            output = self.llm_chain.invoke(inputs)
            try:
                score = int(output.strip())
            except Exception:
                score = 0
            scored_docs.append((doc, score))
        scored_docs.sort(key=lambda x: x[[1]], reverse=True)
        return [doc for doc, score in scored_docs[:self.top_k]]  # Return only top_k documents    

class LLMRerankerBatched(BaseDocumentCompressor):
    """ LLM Reranker that uses LLMChain to rerank documents in batches.
    It passes the documents to the LLM in a single call and expects the LLM to return a list of scores.
    """
    llm_chain: object = Field(LLMChain, description="LLM chain to rerank documents in batches")
    document_variable_name: str = "documents"
    top_k: int = 5  # Number of top documents to return

    def compress_documents(
        self,
        documents: Sequence[Document],
        query: str,
        *,
        callbacks: Optional[list] = None,
    ) -> List[Document]:
        
        scored_docs = []
        
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
        return [doc for doc, _ in scored_docs[:self.top_k]]
    
class RerankingRetriever:
    """
    Encapsulates a retriever with LLM-based reranking using ContextualCompressionRetriever.
    """
    def __init__(
        self,
        vector_store,
        reranker_model_name: str = "gpt-4o-mini",
        rerank_top_k: int = 10,
        retriever_k: int = 20,
    ):
        # Set up the base retriever
        self.base_retriever = vector_store.as_retriever(search_kwargs={"k": retriever_k})

        self.rerank_prompt = PromptTemplate(
            input_variables=["query", "documents"],
            template=batch_retriever_prompt_template,
        )

        # Set up the reranker LLM
        self.llm_reranker = ChatOpenAI(
            model_name=reranker_model_name,
            temperature=0.0
        )

        # Set up the reranker compressor
        self.reranker_batched = LLMRerankerBatched(
            llm_chain=self.rerank_prompt | self.llm_reranker,
            top_k=rerank_top_k
        )

        # Compose the contextual compression retriever
        self.retriever = ContextualCompressionRetriever(
            base_retriever=self.base_retriever,
            base_compressor=self.reranker_batched,
        )

    def as_tool(self, name="project_search", description="Searches the project documents for relevant information."):
        """
        Returns a retriever tool for use in tool-augmented chat.
        """
        return create_retriever_tool(
            self.retriever,
            name=name,
            description=description
        )


class Embedder:
    def __init__(self, model_name: str = "BAAI/bge-small-en"):
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(self.device)

    def embed_query(self, text: str) -> List[float]:
        """Embed the input text using the Hugging Face model."""
        inputs = self.tokenizer(text, return_tensors="pt").to(self.device)
        with torch.no_grad():
            embeddings = self.model(**inputs).last_hidden_state.mean(dim=1).squeeze().cpu().numpy()
        return embeddings.tolist()
    
    def _count_tokens(self, text: str) -> int:
        """Count the number of tokens in the input text."""
        return len(self.tokenizer.encode(text, add_special_tokens=False))

    # This is solely for suppressing the token limit warning in the Hugging Face tokenizer
    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in the input text, handling texts longer than the model's max length."""
        max_length = getattr(self.tokenizer.model_max_length, "item", lambda: self.tokenizer.model_max_length)()
        tokens = self.tokenizer.encode(text, add_special_tokens=False)
        if len(tokens) <= max_length:
            return len(tokens)
        # For long texts, split into chunks and sum
        return sum(
            len(tokens[i:i+max_length])
            for i in range(0, len(tokens), max_length)
        )
    
class WrappedEmbedder:
    def __init__(self, model_name: str = "BAAI/bge-small-en"):
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={"device": "cuda" if torch.cuda.is_available() else "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
    
    def embed_query(self, text: str) -> List[float]:
        return self.embedding_model.embed_query(text)

    
class VectorStore:
    def __init__(self, collection_name: str, connection_string: str, embeddings: Embedder, async_mode: bool = False):
        self.vector_store = PGVector(
            embeddings=embeddings,
            collection_name=collection_name,
            connection= connection_string,
            async_mode= async_mode,
        )

    def as_retriever(self, search_kwargs: dict = None):
        if search_kwargs is None:
            search_kwargs = {"k": 20}
        return self.vector_store.as_retriever(search_kwargs=search_kwargs)
    

class ChatManagerWithTools:
    def __init__(self, config=None):
        self.config = config or {}
        self._setup_env()
        self._setup_embeddings()
        self._setup_vector_store()
        self._setup_retriever()
        self._setup_llm()
        self._setup_memory()
        self._setup_tools()
        self._setup_prompt()

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
        )

    def _setup_retriever(self):
        self.reranking_retriever = RerankingRetriever(
            vector_store=self.vector_store,
            reranker_model_name="gpt-4o-mini",
            rerank_top_k=10,
            retriever_k=20
        ).retriever

    def _setup_llm(self):
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.2,
            streaming=True,
        )

    def _setup_memory(self):
        self.message_history = InMemoryChatMessageHistory()

    def _setup_tools(self):
        retriever_tool = self.reranking_retriever.as_tool(
            name="project_search",
            description="Searches the project documents for relevant information."
        )
        self.tools = {
            "project_search": retriever_tool,
            "get_file_by_name": get_file_by_name_tool,
            "get_project_directory_structure": get_project_directory_structure_tool,
        }

    def _setup_prompt(self):
        self.system_message = system_message

    def _count_memory_tokens(self) -> int:
        return sum(self.embedding_model.count_tokens(msg.content) for msg in self.message_history.messages)

    def _enforce_memory_limit(self, max_tokens=8000):
        messages = self.message_history.messages
        while self._count_memory_tokens() > max_tokens and messages:
            # Remove the oldest message (after system message)
            messages.pop(0)

    def _enforce_memory_message_limit(self, max_messages: int = 20):
        """
        Keeps only the most recent `max_messages` in memory.
        """
        messages = self.message_history.messages
        if len(messages) > max_messages:
            # Remove oldest messages, keep only the last `max_messages`
            del messages[:len(messages) - max_messages]

    # All the milk and honey is here
    async def stream_response(self, user_message: str):
        # Build chat history
        history_msgs = self.message_history.messages
        system_msg = SystemMessage(content=self.system_message)
        user_msg = HumanMessage(content=user_message)
        messages = [system_msg] + history_msgs + [user_msg]

        # Stream LLM response
        assistant_reply = ""
        async for chunk in self.llm.astream(messages):
            if hasattr(chunk, "content") and chunk.content:
                assistant_reply += chunk.content
 
        # Check if LLM wants to use a tool (by outputting a JSON block)
        tool_call = self._extract_tool_call(assistant_reply)
        if tool_call:
            tool_name = tool_call.get("tool")
            args = tool_call.get("args", {})
            tool_func = self.tools.get(tool_name)
            if tool_func:
                tool_result = tool_func.invoke(args)
                tool_context_msg = HumanMessage(
                    content=f"The result of your tool call `{tool_name}` is:\n{tool_result}\n"
                            "Please use this information to answer the user's question."
                )
                messages.append(AIMessage(content=assistant_reply))
                messages.append(tool_context_msg)
                final_reply = ""
                async for chunk in self.llm.astream(messages):
                    if hasattr(chunk, "content") and chunk.content:
                        final_reply += chunk.content
                        yield chunk.content  # Only yield the final answer
                assistant_reply = final_reply
        else:
            # Only yield if no tool call was made
            yield assistant_reply

        # Update memory
        self.message_history.add_user_message(user_message)
        self.message_history.add_ai_message(assistant_reply)
        # self._enforce_memory_limit(max_tokens=4000)
        self._enforce_memory_message_limit(max_messages=20)

    def _extract_tool_call(self, text: str) -> Dict[str, Any] | None:
        # Look for a JSON block in the LLM output
        try:
            start = text.index("{")
            end = text.rindex("}") + 1
            json_block = text[start:end]
            return json.loads(json_block)
        except Exception:
            return None
        