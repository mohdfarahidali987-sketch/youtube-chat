
from dotenv import load_dotenv
import time
import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()


def get_embeddings():

    return GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )


def get_video_db_path(video_id):
    return os.path.join("vector_db", video_id)


def load_vector_store(video_id):

    db_path = get_video_db_path(video_id)

    index_file = os.path.join(db_path, "index.faiss")
    pickle_file = os.path.join(db_path, "index.pkl")

    if os.path.exists(index_file) and os.path.exists(pickle_file):

        print("Loading existing vector database...")

        embeddings = get_embeddings()

        vector_store = FAISS.load_local(
            db_path,
            embeddings,
            allow_dangerous_deserialization=True
        )

        print("Cached vector database loaded successfully!")

        return vector_store

    return None


def create_vector_store(chunks, video_id):

    embeddings = get_embeddings()

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

        if i + batch_size < len(chunks):
            time.sleep(65)

    db_path = get_video_db_path(video_id)

    os.makedirs(db_path, exist_ok=True)

    vector_store.save_local(db_path)

    print("Vector database created and saved successfully!")

    return vector_store


def get_retriever(vector_store):

    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
