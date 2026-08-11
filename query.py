import sys
import os
import chromadb



from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, StorageContext, Settings, get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.llms.anthropic import Anthropic

load_dotenv()

Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")


def load_index():
    #  we connect to the chromadb database and GET a collection called "second_brain"
    chroma_client = chromadb.PersistentClient(path="./.chroma")
    chroma_collection = chroma_client.get_or_create_collection("second_brain")


    # storage context bridge
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # load index from ChromaDB
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store
                                               , storage_context=storage_context
                                               , show_progress=True)

    return index


def retrieve(query):
    index = load_index()

    # create a retriever with a similarity postprocessor
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=10)

    # create a query engine with the retriever
    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=get_response_synthesizer(llm=Anthropic(model="claude-haiku-3-5-20251001", temperature=0.0))
    )

    # perform the query
    response = query_engine.query(query)

    return response


if __name__ == "__main__":
    question = "This file will index the contents of a file, store it in ChromaDB collection, and allow the user to query the collection."
    print(f"\nQuestion: {question}\n")
    response = retrieve(question)
    print(f"Answer: {response}")
    

    


