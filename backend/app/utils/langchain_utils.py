import os
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from app.utils.logging_config import setup_logger
from app.utils.pinecone_utils import init_pinecone
from langchain_pinecone import PineconeVectorStore
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain

logger = setup_logger()

def setup_langchain():
    # Initialize Pinecone
    pinecone_index = init_pinecone()

    # Initialize embeddings
    embeddings = OpenAIEmbeddings(
        api_key=os.getenv("OPENAI_API_KEY"), 
        model="text-embedding-3-small"
    )

    # Create a Pinecone vector store
    vector_store = PineconeVectorStore(index=pinecone_index, embedding=embeddings)

    # Initialize the ChatOpenAI model
    chat_model = ChatOpenAI(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        model_name="gpt-4o-mini",
        temperature=0.7
    )

    # Set up memory to use Pinecone for conversation history
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        input_key="question",
        output_key="answer"
    )

    # Setup the conversational retrieval chain
    return ConversationalRetrievalChain.from_llm(
        llm=chat_model,
        retriever=vector_store.as_retriever(namespace="faqs"),
        memory=memory
    )

def construct_langchain_prompt(context: str, user_message: str, chat_history: list) -> str:
    """Construct the prompt with updated rules for LangChain."""
    rules = (
        "You are an intelligent assistant trained to manage pizza orders and respond to user queries.\n"
        "Rules:\n"
        "1. If the user wants to create an order, ensure toppings, size, and name are provided. If missing, ask for the information.\n"
        "2. When you have all the user information to create an order, generate a random 6-digit 'order number', show it to the user and include it in the response.\n"
        "3. If the user wants to check, modify, or cancel an order, ensure an order number is provided. If missing, ask for it.\n"
        "4. If the query cannot be resolved due to missing details or complexity, escalate it by setting the intent to 'escalate_to_human'.\n"
        "5. Provide a concise and clear response to the user.\n"
        "6. For 'create_order', ensure all details (toppings, size, name) are present; otherwise, ask for missing info.\n"
        "7. For 'cancel_order', ensure an order number is provided; otherwise, ask for it.\n"
        "8. Use the chat history to provide accurate responses for intents like checking or modifying orders.\n"
        "9. Answer all the user queries with the relevant data.\n"
    )
    
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", f"{rules}\nContext:\n{context}"),
        *[(msg["role"], msg["content"]) for msg in chat_history],
        ("user", "{prompt}"),
    ])
    
    return prompt_template.invoke({"context": context, "prompt": user_message})
