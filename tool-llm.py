from env import get_env
import os

# Import relevant functionality
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import create_react_agent

os.environ["OPENAI_API_KEY"] = get_env("OPENAI_API_KEY")
os.environ["TAVILY_API_KEY"] = get_env("TAVILY_API_KEY")

model = ChatOpenAI(model="gpt-3.5-turbo")
search = TavilySearchResults(max_results=2)
tools = [search]

model_with_tools = model.bind_tools(tools)

response = model_with_tools.invoke([HumanMessage(content="What's the weather in SF?")])

# Repare que a tool não foi invocada
# A LLM apenas pede que a gente faça a invocação
print(f"ContentString: {response.content}")
print(f"ToolCalls: {response.tool_calls}")