import requests
import sqlite3
import uuid
from langchain_core.messages import HumanMessage, AIMessage
DB_NAME='youtube_ai_db'
def getConnection():
      connction=sqlite3.connect(DB_NAME,timeout=30)
      connction.row_factory=sqlite3.Row
      connction.execute('PRAGMA foreign_key=ON')
      return connction

def createTable(): 
      conn=getConnection()
      cursor=conn.cursor()

      cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT UNIQUE NOT NULL,
            video_id TEXT NOT NULL, 
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
       """)
      cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('human', 'ai')),
            content TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (conversation_id)
            REFERENCES conversations(conversation_id)
            ON DELETE CASCADE
        )
    """)
      
      conn.commit()
      conn.close()


def create_conversation(video_id: str):
    conversation_id = str(uuid.uuid4())

    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO conversations (conversation_id, video_id)
        VALUES (?, ?)
        """,
        (conversation_id, video_id)
    )

    conn.commit()
    conn.close()

    return conversation_id

def get_conversation(conversation_id: str):
    conn = getConnection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT conversation_id, video_id
            FROM conversations
            WHERE conversation_id = ?
        """, (conversation_id,))

        return cursor.fetchone()

    finally:
        conn.close()


def save_message(conversation_id: str, role: str, content: str):
    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO messages (conversation_id, role, content)
        VALUES (?, ?, ?)
        """,
        (conversation_id, role, content)
    )
    conn.commit()
    conn.close()

def get_chat_history(conversation_id: str):
    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT role, content
        FROM messages
        WHERE conversation_id = ?
        ORDER BY id ASC
        """,
        (conversation_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    chat_history = []

    for row in rows:
        if row["role"] == "human":
            chat_history.append(HumanMessage(content=row["content"]))
        elif row["role"] == "ai":
            chat_history.append(AIMessage(content=row["content"]))

    return chat_history
 


if __name__ == "__main__":
    createTable()
    print("Database and tables created successfully!")




