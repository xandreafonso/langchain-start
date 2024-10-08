from env import get_env
import os

# Import relevant functionality
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

os.environ["OPENAI_API_KEY"] = get_env("OPENAI_API_KEY")
os.environ["TAVILY_API_KEY"] = get_env("TAVILY_API_KEY")

@tool
def search(query: str):
    """Call to surf the web."""
    # This is a placeholder, but don't tell the LLM that...
    if "sf" in query.lower() or "san francisco" in query.lower():
        return ["It's 60 degrees and foggy."]
    return ["It's 90 degrees and sunny."]

model = ChatOpenAI(model="gpt-3.5-turbo")

tools = [search]

agent_executor = create_react_agent(model, tools)

response = agent_executor.invoke({"messages": [HumanMessage(content="whats the weather in sf?")]})
print(response)
