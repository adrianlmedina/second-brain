import sys
import os
import chromadb



from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.readers.file import PDFReader
load_dotenv()

# choosing which model to use for embedding
Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# choosing Chunking Strategy 
Settings.text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=64)

def ingest_file(file_path):

    if not os.path.exists(file_path):
        print("file not found...")

    # this is where we read the file 
    # we are using PDFReader to explicitly to gaurentee text extraction from PDF files
    ext = os.path.splitext(file_path)[1].lower()
    if ext ==".pdf":
        loader = PDFReader()
        documents = loader.load_data(file=file_path)
    else:
        documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
    print(f"      Loaded {len(documents)} document(s)")


    # here we connect to the chromadb database and create a collection called "second_brain"
    chroma_client = chromadb.PersistentClient(path="./.chroma")
    chroma_collection = chroma_client.get_or_create_collection("second_brain")


    # storage context bridge
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)


    # storing vectors from the document that it's taken
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        show_progress=True,
    )
    print(f"      Collection now has {chroma_collection.count()} vectors stored.")

    return index

def inspect_collection():
    # connect to chromadb
    chroma_client = chromadb.PersistentClient(path="./.chroma")
    collection = chroma_client.get_or_create_collection("second_brain")
    count = collection.count()

    if count == 0:
        print("empty run... nothing stored yet")


    # this fetches the first 3 items from ChromaDB, loops through the text docs,
    # and prints a numbered list showing up to 200 chars of each doc
    results = collection.peek(limit=3) 
    for i, doc in enumerate(results["documents"]):
        print(f"   [{i+1}] {doc[:200]}{'...' if len(doc) > 200 else ''}")
        print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python ingest.py <path_to_file>   → ingest a file")
        print("  python ingest.py --inspect        → peek at stored vectors")
        sys.exit(0)

    if sys.argv[1] == "--inspect":
        inspect_collection()
    else:
        ingest_file(sys.argv[1])
        inspect_collection()

