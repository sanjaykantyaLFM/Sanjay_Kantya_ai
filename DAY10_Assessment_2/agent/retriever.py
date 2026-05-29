from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004"
)

vectorstore = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 2}
)


def retrieve_documents(query):
    docs = retriever.invoke(query)

    results = []

    for doc in docs:
        results.append({
            "content": doc.page_content,
            "source": doc.metadata.get("source"),
            "chunk_id": doc.metadata.get("chunk_id")
        })

    return results