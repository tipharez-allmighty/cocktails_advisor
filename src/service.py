from .utils import parse_search_result, parse_chat_history
from .chromadb_utils import save_message_to_history
from .llm import generate_async_response
from .prompts import PROMPT


async def handle_response(message: str, client):
    collection_recipes = await client.get_or_create_collection("cocktails_recipes")
    collection_history = await client.get_or_create_collection("chat_history")

    search_recipes = await collection_recipes.query(query_texts=[message], n_results=5)
    search_collection_history = await collection_history.query(
        query_texts=[message], n_results=5
    )
    await save_message_to_history(text=message)
    query = format_prompt(message, search_recipes, search_collection_history)
    print(query)
    response = await generate_async_response(query)
    return response


def format_prompt(message: str, search_result: dict, message_history: dict):
    parsed_search_results = parse_search_result(search_result)
    parsed_history = parse_chat_history(message_history)
    return PROMPT.format(message, parsed_search_results, parsed_history)
