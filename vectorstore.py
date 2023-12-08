import chromadb
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

data_dir = 'my_kb'
persistent_chroma_client = chromadb.PersistentClient(path=data_dir)
embeddings = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")

def getVectorStore(collection):
    return Chroma(client=persistent_chroma_client, persist_directory=data_dir,
                  collection_name=collection, embedding_function=embeddings)