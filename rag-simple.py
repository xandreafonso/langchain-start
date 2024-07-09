from env import get_env
import os

from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate

os.environ["OPENAI_API_KEY"] = get_env("OPENAI_API_KEY")

documents = [
    Document(
        page_content="Dogs are great companions, known for their loyalty and friendliness.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Cats are independent pets that often enjoy their own space.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Goldfish are popular pets for beginners, requiring relatively simple care.",
        metadata={"source": "fish-pets-doc"},
    ),
    Document(
        page_content="Parrots are intelligent birds capable of mimicking human speech.",
        metadata={"source": "bird-pets-doc"},
    ),
    Document(
        page_content="Rabbits are social animals that need plenty of space to hop around.",
        metadata={"source": "mammal-pets-doc"},
    ),
]

vectorstore = Chroma.from_documents(
    documents,
    embedding=OpenAIEmbeddings(),
)

# result = vectorstore.similarity_search("cat")
# print(result)

# Note that providers implement different scores; 
# Chroma here returns a distance metric that should vary inversely with similarity.
# result = vectorstore.similarity_search_with_score(query="cat", k=2)
# print(result)

# async def asearch_and_print(query):
#     results = await vectorstore.asimilarity_search(query)
#     print(results)

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(asearch_and_print("Goldfish"))



# retriever = RunnableLambda(vectorstore.similarity_search).bind(k=1)  # select top result
# result = retriever.batch(["cat", "shark"])
# print(result)

# retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 1})
# result = retriever.batch(["cat", "shark"])
# print(result)



llm = ChatOpenAI(model="gpt-3.5-turbo")
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 2})

message = """
Answer this question using the provided context only.

{question}

Context:
{context}
"""

prompt = ChatPromptTemplate.from_messages([("human", message)])
rag_chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | llm
question = "tell me about cats"
response = rag_chain.invoke(question)
print("Question:", question, "Response:", response.content)






