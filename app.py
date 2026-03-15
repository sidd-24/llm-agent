import streamlit as st
from agent.executor import run_agent


st.set_page_config(
    page_title="LLM Agent",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 Multi-tool LLM Agent")
st.caption("Ask anything. The agent will search the web, Wikipedia, or calculate to find the answer.")

with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Get a free key at console.groq.com",
    )
    st.markdown("---")
    st.markdown("**Available Tools**")
    st.markdown(
        "- 🌐 **WebSearch** — searches the web\n"
        "- 📖 **Wikipedia** — gets factual info\n"
        "- 🧮 **Calculator** — solves math problems"
    )
    st.markdown("---")
    st.markdown("**Example questions**")
    st.markdown(
        "- What is the GDP of Germany in 2024?\n"
        "- Who is the CEO of Anthropic?\n"
        "- What is 15% of 3500?\n"
        "- Explain what LangChain is"
    )

if not api_key:
    st.warning("Please enter your Groq API key in the sidebar to continue.")
else:
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    for entry in st.session_state["chat_history"]:
        with st.chat_message("user"):
            st.write(entry["question"])
        with st.chat_message("assistant"):
            st.write(entry["answer"])

    question = st.chat_input("Ask the agent anything...")

    if question:
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            with st.spinner("Agent is thinking..."):
                try:
                    answer = run_agent(api_key, question)
                    st.write(answer)
                    st.session_state["chat_history"].append({
                        "question": question,
                        "answer": answer,
                    })
                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}")