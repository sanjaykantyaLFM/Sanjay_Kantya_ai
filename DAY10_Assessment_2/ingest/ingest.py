from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

files = [
    "docs/ai.txt",
    "docs/rag.txt",
    "docs/langgraph.txt"
]

documents = []

for file in files:
    loader = TextLoader(file)
    docs = loader.load()

    for doc in docs:
        doc.metadata["source"] = file

    documents.extend(docs)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)


for idx, chunk in enumerate(chunks):
    chunk.metadata["chunk_id"] = idx


embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004"
)


vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="chroma_db"
)

print(f"Loaded {len(documents)} documents")
print(f"Created {len(chunks)} chunks")
print("Vector database created successfully")