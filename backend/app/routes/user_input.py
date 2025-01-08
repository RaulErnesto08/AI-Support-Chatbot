from pydantic import BaseModel
from dotenv import load_dotenv
from app.utils.logging_config import setup_logger
from langchain_pinecone import PineconeVectorStore
from fastapi import APIRouter, Request, HTTPException
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

from app.utils.openai_utils import call_openai_formatter
from app.utils.langchain_utils import construct_langchain_prompt
from app.utils.actions_utils import perform_mocked_action, perform_escalation_action, analyze_sentiment_transformers

load_dotenv()
router = APIRouter()
logger = setup_logger()

namespace = "faqs"
index_name = "chatbot"
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = PineconeVectorStore(index_name=index_name, embedding=embeddings, namespace=namespace)
chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
parser = StrOutputParser()

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
        
        # Analyze sentiment
        sentiment = analyze_sentiment_transformers(user_message)
        logger.info(f"User sentiment: {sentiment}")

        # Retrieve context using LangChain and Pinecone
        results = vector_store.similarity_search(user_message, k=2)
        context = "\n".join([doc.page_content for doc in results]) if results else "No relevant documents found."

        # Generate response from LangChain
        langchain_prompt = construct_langchain_prompt(context, user_message, chat_history)
        langchain_response = chat_model | parser
        langchain_output = langchain_response.invoke(langchain_prompt)

        # Format response using OpenAI Formatter
        formatted_response = call_openai_formatter(langchain_output)

        # Perform action based on intent
        action_result = None
        if formatted_response["response_type"] == "intent":
            intent = formatted_response["intent"]

            if intent == "escalate_to_human":
                action_result = perform_escalation_action(formatted_response)
            else:
                action_result = perform_mocked_action(intent, formatted_response)


        # Update chat history
        chat_history.append({"role": "user", "content": user_message})
        chat_history.append({"role": "assistant", "content": formatted_response["content"]})
        
        print(f"Chat History: \n{chat_history}")

        return {
            "response": formatted_response["content"],
            "action_result": action_result,
            "order_details": formatted_response.get("order_details"),
            "sentiment": sentiment,
        }

    except Exception as e:
        logger.error(f"Error processing input: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")