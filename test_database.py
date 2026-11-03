
from database import (
    createTable,
    create_conversation,
    save_message,
    get_chat_history
)

createTable()

# Create conversation
conversation_id = create_conversation("J5_-l7WIO_w")

# Save messages
save_message(conversation_id, "human", "What is RAG?")
save_message(
    conversation_id,
    "ai",
    "RAG stands for Retrieval-Augmented Generation."
)

# Fetch history
history = get_chat_history(conversation_id)

print("Conversation ID:", conversation_id)

for message in history:
    print(message.type, ":", message.content)
