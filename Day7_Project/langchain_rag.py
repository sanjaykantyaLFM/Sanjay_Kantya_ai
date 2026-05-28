from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFacePipeline
from langchain_core.runnables import RunnablePassthrough
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
# from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnableMap
# from langchain.chains import ConversationRetrievalChain
# from langchain.chains.retrieval_qa.base import ConversationRetrievalChain


loader = PyPDFLoader("notes.pdf")
docs = loader.load()
print(f"pdf loaded successfuly {len(docs)}")


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=20 
)


chunk_medium = text_splitter.split_documents(docs)
print(f"len of chunks {len(chunk_medium)}")


print(" Embedding model loaded")
#embedding 
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# vector to store in chroma
vectorStore = Chroma.from_documents(
    documents=chunk_medium,
    embedding=embedding_model,
    persist_directory="./chroma_db_folder"
)

print(f"vector store created and len is {len(chunk_medium)} docs")

# #llm language
pipe = pipeline(
    "text-generation",
    model="gpt2",
    max_new_tokens=100,
    do_sample=True,
    temperature=0.7
)


# model_name = "google/flan-t5-base"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

llm = HuggingFacePipeline(pipeline=pipe)


#prompt template
prompt = PromptTemplate(
    template="""Use the following context to answer the question.
If the answer is not in the context, say "I don't know".

Context: {context}
Question: {question}
Answer:""",

    input_variables=["context", "question"]
)


print("Prompt template created")

#Create Output Parser
print("\n Setting up of output parser..")
output_parser = StrOutputParser()

# creating retriever
retriever = vectorStore.as_retriever(search_kwargs={"k": 3})
print("retriever created k=3 means top 3 relevant chunks from docs from medium chukns")


def format_docs(docs):
    return "\n".join(doc.page_content for doc in docs)     # Function to format retrieved documents

# # Now LCEL chain building lcel meand langchain expression language   | this is pipe operator "|"
# BUILD CHAIN: retriever → format → prompt → llm → parser
chain = (  # this is we assume as original chain with retirver k 3
    {"context": retriever | format_docs,"question": RunnablePassthrough()}
    | prompt
    | llm
    | output_parser
)

print("LCEL chain is builted successfuly")


# # test the chain
# Question 1
question1 = "What is RAG?"
print(f"Question: {question1}")
print("*****")

answer1 = chain.invoke(question1)
print(f"Answer: {answer1}")


question2 = "What is LangChain?"
print(f"\nQuestion: {question2}")
print("-" *5)
answer2 = chain.invoke(question2)
print(f"Answer: {answer2}")



# Swaping of components
print("Swapping of component")

textSplitterLarge = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 50 
)

chunk_large = textSplitterLarge.split_documents(docs)

textSplitterSmall = RecursiveCharacterTextSplitter(
    chunk_size = 100, 
    chunk_overlap =10
)


chunk_small = textSplitterSmall.split_documents(docs)

print("Length of Large chunks", len(chunk_large))
print(f"Length of small chunks {len(chunk_large)}")
print(f"length of medium chunks{len(chunk_medium)}")


retriever_k1 = vectorStore.as_retriever(search_kwargs={"k": 1})
retriever_k5 = vectorStore.as_retriever(search_kwargs={"k": 5})

ques_test = "what is RAG" 

result_k1 = retriever_k1.invoke(ques_test)
print(f"retrived {len(result_k1)} chunks")

result_k3 = retriever.invoke(ques_test) # yha pr retriver medium chunks wala hai 
print(f"retrived {len(result_k3)} chunks")

result_k5 = retriever_k5.invoke(ques_test)
print(f"retrived {len(result_k5)} chunks")

# testing with diffrecnt retriver
print("testing chain with diffrent retrivers..")


chain_k1 = ( 
    {"context": retriever_k1 | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | output_parser
)

# Chain with k=5
chain_k5 = (
    {"context": retriever_k5 | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | output_parser
)

#note:****** creating new new chains is the real swapping like phle chain one me retriver_1 or k = 3 ke according data ata or isi jgh waps se chain likh diya with new retriver2 so it give new generation of content with diffrent k and same for more chain

print(f"\nQuestion: {ques_test}")
print("-" *10)

answer_k1 = chain_k1.invoke(ques_test)
print(f"\nanswer with k1 {answer_k1[:100] + "..."}") 

print("\nAnswer with k=3 (original):")
answer_k3 = chain.invoke(ques_test)
print(answer_k3[:100] + "...")

print("\nAnswer with k=5:")
answer_k5 = chain_k5.invoke(ques_test)
print(answer_k5[:100] + "...")



# Now adding Conversational memory 

# #creating the memory
# memory = ConversationBufferMemory(
#     memory_key="chat_history",
#     return_messages=True
# )

# # this is used to build chain with memory

# qa_with_memory = ConversationRetrievalChain.from_llm(
#     llm=llm,
#     retriever=retriever,
#     memory=memory,
#     return_source_documents=True
# )

# conversation_questions = [
#     "What is RAG?",
#     "Give me more details",
#     "What is LangChain?"
# ]

# for i, question in enumerate(conversation_questions):
#     print(f"Turn {i+1}")
#     print(f"Question: {question}")
#     print("-" *10)
    
#     response = qa_with_memory({"question": question})
#     answer = response["answer"]
    
#     print(f"Answer: {answer[:200]}...\n")


# # show memory content
# print("chat History :):")
# print(memory.buffer)
