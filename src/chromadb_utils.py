from datetime import datetime
import chromadb

from .llm import get_embeddings
from .utils import process_data


async def get_chromadb_client():
    return await chromadb.AsyncHttpClient(host="localhost", port=8000)


async def load_data(file_name: str):
    client = await get_chromadb_client()
    collection = await client.get_or_create_collection("cocktails_recipes")
    df = await process_data(file_name)
    documents = []
    metadatas = []
    embeddings = []
    ids = []
    
    existing_documents = await collection.count()
    if existing_documents > 0:
        print("Chroma DB already has data. Skipping data loading.")
        return
    print("Loading data into Chroma DB...")
    
    for index, row in df.iterrows():
        cocktail_name = row["name"]
        alcoholic = row["alcoholic"]
        category = row["category"]
        ingredients = row["ingredients"]

        metadata = {
            "name": cocktail_name,
            "alcoholic": alcoholic,
            "ingredients": ingredients,
            "category": category,
        }

        embedding_name = await get_embeddings(cocktail_name)
        embedding_ingredients = await get_embeddings(ingredients)

        documents.append(cocktail_name)
        metadatas.append(metadata)
        embeddings.append(embedding_name)
        ids.append(f"{index}_name")

        documents.append(ingredients)
        metadatas.append(metadata)
        embeddings.append(embedding_ingredients)
        ids.append(f"{index}_ingredients")

    await collection.upsert(
        documents=documents, metadatas=metadatas, embeddings=embeddings, ids=ids
    )


async def save_message_to_history(text: str):
    client = await get_chromadb_client()
    collection = await client.get_or_create_collection("chat_history")
    return await collection.upsert(
        documents=[text],
        embeddings=await get_embeddings(text),
        ids=["history_{}".format(datetime.now().timestamp())],
    )
