# Cocktails Recommendation App

This is a FastAPI-based application that provides a chat interface for cocktail recommendations. It uses ChromaDB for managing embeddings and chat history.

## API Endpoints
POST /api/chat: Send a message to the chatbot and receive a response.
GET /: Serve the chat interface.

## Prerequisites

- ChromaDB
- FastAPI

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/tipharez-allmighty/cocktails_advisor.git
   cd cocktails_app
   
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   
4. Set up Gemini api key in .env file:
   ```bash
   GEMINI_API_KEY=xxx...

5. Running the Application
   
   Start the ChromaDB server:
     ```bash
     chroma run --path ./chroma_db
      ```
   Run the FastAPI application:
     ```bash
     uvicorn src.main:app --reload
