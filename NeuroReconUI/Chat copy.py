import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter

# ✅ Step 1: Set Google Gemini API Key
GENAI_API_KEY = "AIzaSyDLsN1tJQWw00Eh57Rnw_tLLH5VfN5DFkk"
genai.configure(api_key=GENAI_API_KEY)

# ✅ Step 2: Initialize Google Geminiwhat Chat Model
chat_model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=GENAI_API_KEY)

# ✅ Step 3: Sample Knowledge Base (Documents)
documents = [
    "LangChain helps developers build AI-powered applications.",
    "FAISS is an open-source library for efficient similarity search.",
    "Retrieval-Augmented Generation (RAG) improves chatbot accuracy by fetching relevant information.",
    "Google Gemini is an advanced AI model for generating human-like responses."
]

# ✅ Step 4: Convert Documents to Embeddings
text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=20)
docs = text_splitter.create_documents(documents)

# ✅ Step 5: Create Embeddings Using Google Generative AI
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GENAI_API_KEY)

# ✅ Step 6: Store Embeddings in FAISS
vector_store = FAISS.from_documents(docs, embeddings)

# ✅ Step 7: Initialize Conversation Memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# ✅ Step 8: Create the Conversational RAG Chain
conversation_chain = ConversationalRetrievalChain.from_llm(
    llm=chat_model,
    retriever=vector_store.as_retriever(),
    memory=memory
)

# ✅ Step 9: Chat Function (Fix input keys issue)
def chat_with_gemini_rag():
    print("🔹 Gemini RAG Chatbot with Memory (type 'exit' to quit)")
    
    chat_history = []  # ✅ Initialize chat history

    while True:
        user_input = input("You: ")
        
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break

        # ✅ Fix: Pass correct input keys including `chat_history`
        bot_reply = conversation_chain.invoke({
            "question": user_input,
            "chat_history": chat_history  # ✅ Ensures no missing keys error
        })

        chat_history.append((user_input, bot_reply))  # ✅ Update chat history
        if isinstance(bot_reply, list) and len(bot_reply) > 0:
            print(f"Chatbot: {bot_reply[0].get('answer', 'No Answer available')}")
        elif isinstance(bot_reply, dict):
            print(f"Chatbot: {bot_reply.get('answer', 'No Answer available')}")
        else:
            print("Chatbot: No Answer available")

# ✅ Step 10: Run the Chatbot
chat_with_gemini_rag()