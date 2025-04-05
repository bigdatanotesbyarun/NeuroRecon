import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from langchain.document_loaders import PyPDFLoader
from langchain.schema import Document  

# ✅ Step 1: Configure Google Gemini API
GENAI_API_KEY = "AIzaSyDLsN1tJQWw00Eh57Rnw_tLLH5VfN5DFkk"
genai.configure(api_key=GENAI_API_KEY)

# ✅ Step 2: Initialize Chat Model
chat_model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GENAI_API_KEY)

# ✅ Step 3: Sample Knowledge Base
documents1 = [
    "LangChain helps developers build AI-powered applications.",
    "FAISS is an open-source library for efficient similarity search.",
    "Retrieval-Augmented Generation (RAG) improves chatbot accuracy by fetching relevant information.",
    "Google Gemini is an advanced AI model for generating human-like responses."
]

pdf_path = "/home/ubuntu/NeuroRecon/NeuroReconUI/1.pdf"  # Replace with actual PDF file path
loader = PyPDFLoader(pdf_path)
documents = loader.load()
text_data = [doc.page_content for doc in documents]  # Extract text

# ✅ Step 4: Convert Documents to Embeddings
text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=20)
text_data = " ".join([doc.page_content for doc in documents])  # Convert to a single string
docs = text_splitter.split_text(text_data)

# ✅ Step 5: Create Embeddings Using Google Generative AI
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GENAI_API_KEY)
doc_objects = [Document(page_content=chunk) for chunk in docs]
# ✅ Step 6: Store Embeddings in FAISS
#vector_store = FAISS.from_documents(docs, embeddings)
vector_store = FAISS.from_documents(doc_objects, embeddings) 

# ✅ Step 7: Initialize Conversation Memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# ✅ Step 8: Create the Conversational RAG Chain
conversation_chain = ConversationalRetrievalChain.from_llm(
    llm=chat_model,
    retriever=vector_store.as_retriever(),
    memory=memory
)

# ✅ Step 9: Django REST API Endpoint
@api_view(['POST'])
def get_chat_data(request):
    user_input = request.data.get("message", "")
    if not user_input:
        return Response({"error": "Message is required"}, status=400)

    # ✅ Process the chat message
    bot_reply = conversation_chain.invoke({
        "question": user_input,
        "chat_history": memory.load_memory_variables({})
    })

    # ✅ Extract the response
    
    if isinstance(bot_reply, list) and len(bot_reply) > 0:
           response_text=bot_reply[0].get('answer', 'No Answer available')
    elif isinstance(bot_reply, dict):
           response_text=bot_reply.get('answer', 'No Answer available')
    else:
         response_text="No Answer available"
    
    # ✅ Update chat memory
    memory.save_context({"input": user_input}, {"output": response_text})

     
    return Response({"response": response_text})