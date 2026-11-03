from transcript import load_transcript
from textSplitter import split_documents
from vector_store import create_vector_store, get_retriever, load_vector_store

from rag_chian import create_rag_chain
 

video_id=input("Enter youtube video id: ").strip()
vector_store=load_vector_store(video_id)
if vector_store is None:
    print("No existing transcript")
    print("extracting youtube transcript....")
    docs=load_transcript(video_id) 
    print("Splitting transcript intop chunks...")
    chunks=split_documents(docs)
    print("Creating vector database...")
    vector_store=create_vector_store(chunks, video_id)
else:
    print("using existing. vector  databse ")    
 
retriever=get_retriever(vector_store)
rag_chain = create_rag_chain()
while True:
   query = input("\nAsk a question about the video: ")
   if query.lower() =='exit':
       print("chat ended! Good bye..")
       break
   

   results = retriever.invoke(query)

   context = "\n\n".join(
    doc.page_content for doc in results
  )
   

   response = rag_chain.invoke({
    "context": context,
    "question": query,

  })

   print("\nAI Answer:")
   print(response)

 
