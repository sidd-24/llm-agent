from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from agent.tools import get_tools


PROMPT_TEMPLATE = """You are a helpful assistant with access to the following tools:

{tools}

Use the following format strictly:

Question: the input question you must answer
Thought: think about what to do
Action: the action to take, must be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (repeat Thought/Action/Action Input/Observation as needed)
Thought: I now know the final answer
Final Answer: the final answer to the original question

Begin!

Question: {input}
Thought: {agent_scratchpad}"""


def build_agent(api_key: str) -> AgentExecutor:
    llm = ChatGroq(
        api_key=api_key,
        model_name="llama-3.3-70b-versatile",
        temperature=0,
    )

    tools = get_tools()

    prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)

    agent = create_react_agent(
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