from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FakeEmbeddings

def create_vector_store(chunks):

    # 🔥 lightweight embeddings (NO memory issue)
    embedding_model = FakeEmbeddings(size=384)

    vectorstore = FAISS.from_documents(
        chunks,
        embedding_model
    )

    return vectorstore