import os
import asyncio
import pandas as pd


def read_csv_data(file_name: str):
    path = os.path.join("data", file_name)
    data = pd.read_csv(path)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    data = data[["name", "alcoholic", "category", "ingredients"]].dropna()
    return data


async def process_data(file_name: str):
    return await asyncio.to_thread(read_csv_data, file_name)


def parse_search_result(data: dict):
    result = ""

    if "metadatas" in data and "distances" in data:
        metadatas = data["metadatas"][0]
        distances = data["distances"][0]

        for idx, metadata in enumerate(metadatas):
            distance = distances[idx] if idx < len(distances) else "Unknown distance"

            name = metadata.get("name", "Unknown")
            alcoholic_category = metadata.get("alcoholic_category", "Unknown")
            ingredients = metadata.get("ingredients", "No ingredients available")

            result += (
                f"Drink: {name}, Category: {alcoholic_category}, "
                f"Ingredients: {ingredients}, Distance: {distance}\n"
            )

    return result


def parse_chat_history(data: dict):
    result = ""

    if "documents" in data and "distances" in data:
        documents = data["documents"][0]
        distances = data["distances"][0]

        for idx, document in enumerate(documents):
            distance = distances[idx] if idx < len(distances) else "Unknown distance"
            result += f"Document: {document}, Distance: {distance}\n"

    return result
