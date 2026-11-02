# 🤖 Multi-tool LLM Agent

An autonomous LLM agent that decides which tools to use to answer any question. Built with LangChain's tool-calling agent and Groq as the LLM. No paid search API required.

## Stack

| Layer | Tool |
|---|---|
| LLM | Groq (`openai/gpt-oss-120b`, configurable with `GROQ_MODEL`) |
| Agent Framework | LangChain tool-calling agent |
| Web Search | DuckDuckGo (free) |
| Knowledge Tool | Wikipedia |
| Math Tool | NumExpr |
| UI | Streamlit |

## How it works

The agent reasons and acts in a loop until it has the final answer. The model selects tools through native tool calling, so no text format has to be parsed:

```
Question
   ↓
Thought — what should I do?
   ↓
Action — pick a tool (WebSearch / Wikipedia / Calculator)
   ↓
Observation — tool returns result
   ↓
Thought — do I have enough info?
   ↓
Final Answer
```

## Available Tools

| Tool | Description |
|------|-------------|
| 🌐 WebSearch | Searches the web via DuckDuckGo |
| 📖 Wikipedia | Fetches factual summaries from Wikipedia |
| 🧮 Calculator | Evaluates math expressions |

## Project Structure

```
llm-agent/
├── agent/
│   ├── __init__.py
│   ├── tools.py       # Tool definitions (search, wikipedia, calculator)
│   └── executor.py    # Agent setup and execution
├── app.py             # Streamlit UI
├── requirements.txt
└── .gitignore
```

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/sidd-24/llm-agent
cd llm-agent
```

**2. Create and activate virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Get a free Groq API key**

Sign up at [console.groq.com](https://console.groq.com) and create an API key.

**5. Run the app**
```bash
streamlit run app.py
```

Paste your Groq API key in the sidebar and start asking questions.

## Example Questions

- Who is the CEO of SAP?
- What is LangChain?
- What is 15% of 3500?
- What is the GDP of Germany?
- Explain what a knowledge graph is