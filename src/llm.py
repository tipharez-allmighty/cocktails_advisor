import asyncio
import google.generativeai as genai
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
from .config import settings

model_embeddings = SentenceTransformer("all-MiniLM-L6-v2")
model_text = genai.GenerativeModel("gemini-2.0-flash-lite")

genai.configure(api_key=settings.GEMINI_API_KEY)


async def generate_async_response(user_message):
    chat = model_text.start_chat()
    response = await chat.send_message_async(user_message)
    return response.text


def get_local_embedding(text: str):
    return model_embeddings.encode(text).tolist()


async def get_embeddings(text: str):
    def embed():
        return get_local_embedding(text)

    result = await asyncio.to_thread(embed)
    return result
