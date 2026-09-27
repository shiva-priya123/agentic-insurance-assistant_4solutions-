from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


VECTORSTORE_PATH = "models/vectorstore"


# Load the same embedding model used to create
# our existing Project 3 FAISS vector store.
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Load the existing FAISS vector store.
vectorstore = FAISS.load_local(
    VECTORSTORE_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)


def search_policy(question: str, k: int = 3):
    """
    Search the insurance policy knowledge base
    and return the most relevant policy information.
    """

    documents = vectorstore.similarity_search(
        question,
        k=k
    )

    results = []

    for document in documents:
        results.append({
            "source": document.metadata.get("source"),
            "page": document.metadata.get("page"),
            "content": document.page_content
        })

    return results