import os
from env import get_env

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

os.environ["OPENAI_API_KEY"] = get_env("OPENAI_API_KEY")

model = ChatOpenAI(model="gpt-3.5-turbo")
parser = StrOutputParser()

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "Translate the following into {language}:"),
        ("user", "{text}")
    ]
)

response = prompt_template.invoke({"language": "italian", "text": "hi"})
print("Exibindo o template de duas formas.")
print("Forma 1:")
print(response)
print("Forma 2:")
print(response.to_messages())

chain = prompt_template | model | parser
content = chain.invoke({"language": "italian", "text": "hi"})

print("Content:")
print(content)



