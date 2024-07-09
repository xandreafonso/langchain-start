from env import get_env
import os

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

os.environ["OPENAI_API_KEY"] = get_env("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-3.5-turbo")

loader = WebBaseLoader(web_paths=("https://alexandreafonso.com.br/curso-headlines",))
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

prompt = hub.pull("rlm/rag-prompt")
result = prompt.invoke({"question": "A pergunta fica aqui?", "context": "Nenhum contexto."})
print("Prompt: ", result)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = {"context": retriever | format_docs, "question": RunnablePassthrough()} | prompt | llm | StrOutputParser()
response = rag_chain.invoke("Qual a maior vantagem do curso?")
print(response)