from env import get_env
import os

# Import relevant functionality
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain import hub
from langchain.agents import create_tool_calling_agent, AgentExecutor


os.environ["OPENAI_API_KEY"] = get_env("OPENAI_API_KEY")
os.environ["TAVILY_API_KEY"] = get_env("TAVILY_API_KEY")

@tool
def search(query: str):
    """Call to surf the web."""
    # This is a placeholder, but don't tell the LLM that...
    if "sf" in query.lower() or "san francisco" in query.lower():
        return ["It's 60 degrees and foggy."]
    return ["It's 90 degrees and sunny."]

model = ChatOpenAI(model="gpt-4o-mini")
prompt = hub.pull("hwchase17/openai-functions-agent")
tools = [search]

agent = create_tool_calling_agent(model, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

response = agent_executor.invoke({"input": "whats the weather in sf?"})
print(response)