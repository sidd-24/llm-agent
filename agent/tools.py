from langchain.tools import Tool
from duckduckgo_search import DDGS
import wikipedia
import numexpr as ne


def search_web(query: str) -> str:
    import time
    time.sleep(2)
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
        if not results:
            return "No results found."
        return "\n\n".join(
            f"Title: {r['title']}\nSnippet: {r['body']}" for r in results
        )
    except Exception as e:
        return f"Web search failed: {str(e)}. Try Wikipedia instead."


def search_wikipedia(query: str) -> str:
    try:
        summary = wikipedia.summary(query, sentences=3)
        return summary
    except wikipedia.DisambiguationError as e:
        return f"Ambiguous query. Try one of: {e.options[:5]}"
    except wikipedia.PageError:
        return "No Wikipedia page found for this query."


def calculate(expression: str) -> str:
    try:
        result = ne.evaluate(expression)
        return str(result)
    except Exception as e:
        return f"Calculation error: {str(e)}"


def get_tools() -> list:
    return [
        Tool(
            name="WebSearch",
            func=search_web,
            description="Useful for searching current information on the web. Input should be a search query.",
        ),
        Tool(
            name="Wikipedia",
            func=search_wikipedia,
            description="Useful for getting factual information about people, places, events, or concepts. Input should be a topic.",
        ),
        Tool(
            name="Calculator",
            func=calculate,
            description="Useful for solving math problems. Input should be a valid math expression like '2 ** 10' or '100 * 1.5'.",
        ),
    ]