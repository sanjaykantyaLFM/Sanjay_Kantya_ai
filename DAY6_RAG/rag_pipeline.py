from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain_chroma import Chroma   # to store the database we use it
from langchain_core.prompts import PromptTemplate   # it helps to write dynamic prompt instead of single fixed prompt 
from langchain_core.runnables import RunnablePassthrough  # new way to chain things together instead of RetrievalQA
from langchain_core.output_parsers import StrOutputParser  # converts AI output to plain string
from transformers import pipeline    # pipeline is highlevel api from hugging face transformer ...with this evertyhting is automaize no manual laod token

# file loader
loader = PyPDFLoader("notes.pdf") 
docs = loader.load()
print(f"PDF loaded successfuly - total pages: {len(docs)}")

#text spliter part
text_splitter = RecursiveCharacterTextSplitter(
    # chunk_size = 500,
    # chunk_overlap = 50
    chunk_size = 200,
    chunk_overlap = 20
)

chunks = text_splitter.split_documents(docs)

print("Chroma DB created successfully")
print("Total chunks:", len(chunks))
print("\nFirst Chunk:\n")
print(chunks[0].page_content)

# embedding part
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector = embedding_model.embed_query(chunks[0].page_content)

print("\nVector length:", len(vector))
print("Embedding created successfully")

#store in chroma
vectorStore = Chroma.from_documents(
    documents=chunks,
    embedding= embedding_model, 
    persist_directory="./chroma_db_folder"
)

#now ai loading part start here
print("loading Ai model to answer questions..")
print("..Kindly wait first time it might take 2-3 minutes")

pipe = pipeline(
    "text-generation",        # text2text-generation removed in new version
    model="google/flan-t5-base",
    max_new_tokens=200,
    do_sample=False           # gives consistent answers, no randomness
)
llm = HuggingFacePipeline(pipeline=pipe)

#context in template
# {context} and {question} are placeholders -langchain will  fills them automatically
prompt_template = """
Use the following context to answer the question.
If the answer is not in the context, say "I don't know".
Always mention which part of the document you used.

Context:{context}

Question: {question}

Answer:"""

prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

# creating retriever - get top 3 most relevant chunks
retriever = vectorStore.as_retriever(search_kwargs={"k": 3})

# ques asking and getting answer
question = "What is RAG?"

# invoke() does 5 things automatically:
# 1. takes your question "What is RAG?"
# 2. converts question to vector (numbers) using embedding model
# 3. searches Chroma DB for top 3 chunks closest in meaning
# 4. returns the most relevant chunks from your PDF
relevant_chunks = retriever.invoke(question)

print("\n" + "="*0)
print("Ques:", question)

print("\n answer form pdf is>>")
for i, doc in enumerate(relevant_chunks):
    print(f"\nSource {i+1}:")
    print(doc.page_content)