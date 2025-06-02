from typing import List, Sequence, Optional
from pydantic import Field
from langchain.schema import Document
from langchain.chains import LLMChain
from langchain_core.compressors import BaseDocumentCompressor

class LLMReranker(BaseDocumentCompressor):
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
            output = self.llm_chain.run(inputs)
            try:
                score = int(output.strip())
            except Exception:
                score = 0
            scored_docs.append((doc, score))
        scored_docs.sort(key=lambda x: x[[1]], reverse=True)
        return [doc for doc, score in scored_docs[:self.top_k]]  # Return only top_k documents

class LLMRerankerParallel(BaseDocumentCompressor):
    llm_chain: object = Field(LLMChain, description="LLM chain to rerank documents")
    document_variable_name: str = "document"
    top_k: int = 5  # Number of top documents to return

    async def compress_documents(
        self,
        documents: Sequence[Document],
        query: str,
        *,
        callbacks: Optional[list] = None,
    ) -> List[Document]:
        import asyncio

        async def get_score(doc):
            inputs = {
                "query": query,
                self.document_variable_name: doc.page_content,
            }
            # If your llm_chain.run is not async, use run_in_executor instead
            output = await self.llm_chain.arun(inputs)
            try:
                score = int(output.strip())
            except Exception:
                score = 0
            return doc, score

        # Run all LLM calls in parallel
        results = await asyncio.gather(*(get_score(doc) for doc in documents))
        # Sort by score descending
        results.sort(key=lambda x: x[1], reverse=True)
        return [doc for doc, score in results[:self.top_k]]  # Return only top_k documents
    
class LLMRerankerBatched(BaseDocumentCompressor):
    """ LLM Reranker that uses LLMChain to rerank documents in batches.
    It passes the documents to the LLM in a single call and expects the LLM to return a list of scores.
    """
    llm_chain: object = Field(LLMChain, description="LLM chain to rerank documents")
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
        output = self.llm_chain.run(inputs)
        try:
            scores = [int(score.strip()) for score in output.split(",")]
        except Exception:
            scores = [0] * len(documents)
        scored_docs = list(zip(documents, scores))
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        return [doc for doc, score in scored_docs[:self.top_k]]
    