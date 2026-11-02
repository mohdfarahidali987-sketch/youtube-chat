from transcript import load_transcript
from textSplitter import split_documents
from vector_store import create_vector_store, get_retriever
from rag_chian import create_rag_chain
video_id=input("Enter youtube video id: ").strip()
docs=load_transcript(video_id) 
 
 
chunks=split_documents(docs)
 

vector_store=create_vector_store(chunks)
 
retriever=get_retriever(vector_store)
 
rag_chain = create_rag_chain()

query = input("\nAsk a question about the video: ")

results = retriever.invoke(query)

context = "\n\n".join(
    doc.page_content for doc in results
)

response = rag_chain.invoke({
    "context": context,
    "question": query
})

print("\nAI Answer:")
print(response.content)

 
