from langchain.chains import ConversationalRetrievalChain
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from app.utils.pinecone_utils import init_pinecone
import os

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
        retriever=vector_store.as_retriever(),
        memory=memory
    )
