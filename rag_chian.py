from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv
import os
load_dotenv()
parser=StrOutputParser()


def create_rag_chain():
    llm=ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.3
        )
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are a helpful YouTube video assistant.

            Answer the user's question using only the
            following video transcript context.

            Use the conversation history to understand
            follow-up questions and references.

            If the answer is not available in the context,
            clearly say that the video does not provide
            this information.

            Video Context:
            {context}
            """
        ),

        MessagesPlaceholder(variable_name="chat_history"),

        ("human", "{question}")
    ])

    return prompt|llm|parser