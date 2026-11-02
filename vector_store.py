
from dotenv import load_dotenv
import time
import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()


def create_vector_store(chunks):

    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

    batch_size = 20
    vector_store = None

    for i in range(0, len(chunks), batch_size):

        batch = chunks[i:i + batch_size]

        print(f"Processing chunks {i+1} to {i+len(batch)}")

        if vector_store is None:
            vector_store = FAISS.from_documents(
                documents=batch,
                embedding=embeddings
            )
        else:
            vector_store.add_documents(batch)

        # Wait between batches to reduce rate-limit errors
        if i + batch_size < len(chunks):
            time.sleep(65)

    vector_store.save_local("vector_db")

    print("Vector database created successfully!")

    return vector_store


def get_retriever(vector_store):

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )

    return retriever
