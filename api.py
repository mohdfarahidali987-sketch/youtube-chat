
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re

from transcript import load_transcript
from textSplitter import split_documents
from vector_store import (
    create_vector_store,
    get_retriever,
    load_vector_store
)
from rag_chian import create_rag_chain


app = FastAPI(title="YouTube AI Assistant API")


# CORS configuration for browser extension development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    video_id: str
    question: str


class ChatResponse(BaseModel):
    answer: str


@app.get("/")
def home():
    return {
        "message": "YouTube AI Assistant API is running!"
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "youtube-rag"
    }


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    video_id = request.video_id.strip()
    question = request.question.strip()

    # Validate YouTube video ID
    if not re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid YouTube video ID"
        )

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    try:
        # 1. Check existing FAISS database
        vector_store = load_vector_store(video_id)

        # 2. Create database only if cache is unavailable
        if vector_store is None:

            print("Creating a new vector database...")

            docs = load_transcript(video_id)
            chunks = split_documents(docs)

            if not chunks:
                raise ValueError("No transcript chunks found")

            vector_store = create_vector_store(
                chunks,
                video_id
            )

        else:
            print("Using cached vector database!")

        # 3. Retrieve relevant chunks
        retriever = get_retriever(vector_store)
        results = retriever.invoke(question)

        if not results:
            return ChatResponse(
                answer="No relevant information found in this video."
            )

        context = "\n\n".join(
            doc.page_content for doc in results
        )

        # 4. Generate answer using existing RAG chain
        rag_chain = create_rag_chain()

        response = rag_chain.invoke({
            "context": context,
            "question": question
        })

        answer = (
            response.content
            if hasattr(response, "content")
            else response
        )

        # Handle Gemini content-block responses
        if isinstance(answer, list):
            answer = " ".join(
                item.get("text", "")
                for item in answer
                if isinstance(item, dict)
            )

        return ChatResponse(answer=str(answer))

    except HTTPException:
        raise

    except Exception as error:
        print("RAG Error:", error)

        raise HTTPException(
            status_code=500,
            detail="Failed to generate answer"
        )
