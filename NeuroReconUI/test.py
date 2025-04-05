import google.generativeai as genai

def chat_with_rag():
    print("LangChain RAG Chatbot with Memory (type 'exit' to quit)")
    genai.configure(api_key="AIzaSyDLsN1tJQWw00Eh57Rnw_tLLH5VfN5DFkk")
    models=genai.list_models()
    for model in models:
        print(model.name)

# Run the chatbot
chat_with_rag()