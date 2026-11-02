import os

from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from agent.tools import get_tools


# The model picks tools through native tool calling. The older text-based
# ReAct format (Thought / Action / Observation) does not work with current
# Groq models such as gpt-oss, which return tool calls instead of that text.
SYSTEM_PROMPT = """You are a helpful assistant with access to tools for web search, Wikipedia and calculations.
Use a tool whenever the answer depends on current information, facts you are unsure about, or arithmetic.
You may call several tools in a row. Answer concisely and mention which sources you used."""


def build_agent(api_key: str) -> AgentExecutor:
    llm = ChatGroq(
        api_key=api_key,
        model_name=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
        temperature=0,
    )

    tools = get_tools()

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(
        llm=llm,
        tools=tools,
        prompt=prompt,
    )

    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=5,
        handle_parsing_errors=True,
    )

    return executor


def run_agent(api_key: str, question: str) -> str:
    executor = build_agent(api_key)
    result = executor.invoke({"input": question})
    return result["output"]
