from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os
load_dotenv


def create_rag_chain():
    llm=ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.3
        )
    prompt=PromptTemplate(
      template="""
        You are a helpful YouTube video assistant.

        Answer the user's question using only the
        following video transcript context.

        If the answer is not available in the context,
        clearly say that the video does not provide
        this information.

        Context:
        {context}

        Question:
        {question}

        Answer:
        """,
        input_variables=['context','question']
   )
    return prompt|llm