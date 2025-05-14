from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse

from .service import handle_response
from .config import settings
from .chromadb_utils import load_data, get_chromadb_client
from .schemas import Response


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    I'm using this lifespan function to load the dataset when the app starts up,
    so you don't have to do it manually.
    It makes things easier, especially for testing.
    However, this approach has its shortcomings, as it makes the startup process slower.
    But since this is mainly for testing and probably only gets run a couple of times,
    it seemed like the most convenient way to go.
    """
    await load_data(settings.DATASET_NAME)
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/api/chat", response_model=Response)
async def get_response(
    message: Response, client=Depends(get_chromadb_client)
) -> Response:
    response_message = await handle_response(message=message.text, client=client)
    return Response(text=response_message)


@app.get("/", response_class=FileResponse)
async def chat_page():
    return FileResponse("static/index.html", media_type="text/html")
