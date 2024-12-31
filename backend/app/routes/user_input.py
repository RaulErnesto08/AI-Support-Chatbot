from pydantic import BaseModel
from app.utils.logging_config import setup_logger
from langchain_pinecone import PineconeVectorStore
from fastapi import APIRouter, Request, HTTPException
from app.utils.langchain_utils import setup_langchain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

router = APIRouter()
logger = setup_logger()
chatbot_chain = setup_langchain()

namespace = "faqs"
index_name = "chatbot"
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = PineconeVectorStore(index_name=index_name, embedding=embeddings, namespace=namespace)

chat_history = []

class UserInput(BaseModel):
    user_message: str

@router.post("/process-input")
async def process_input(request: Request):
    try:
        data = await request.json()
        user_message = data.get("message", "").strip()

        if not user_message:
            raise HTTPException(status_code=400, detail="Message cannot be empty.")

        # Query the Pinecone vector store
        results = vector_store.similarity_search(user_message, k=2)
        if not results:
            logger.warning("No relevant documents found in Pinecone.")
            raise HTTPException(status_code=404, detail="No relevant data found.")

        # Prepare the context for the prompt
        context = "\n".join([doc.page_content for doc in results])

        # Set up the prompt
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "{context}"),
            ("user", "{prompt}"),
        ])
        
        prompt = {
            "context": context,
            "prompt": user_message,
        }

        # Chat model and response generation
        model = ChatOpenAI()
        parser = StrOutputParser()
        chain = prompt_template | model | parser
        response_text = chain.invoke(prompt)

        # Update chat history
        chat_history.append({"role": "user", "content": user_message})
        chat_history.append({"role": "assistant", "content": response_text})

        # Log interactions
        logger.info(f"User: {user_message}")
        logger.info(f"Chatbot: {response_text}")

        return {"response": response_text}

    except HTTPException as http_exc:
        logger.error(f"HTTP error: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")