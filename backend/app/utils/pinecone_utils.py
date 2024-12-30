import os

from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

def init_pinecone():
    pinecone_client = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

    index_name = "chatbot"

    existing_indexes = [index.name for index in pinecone_client.list_indexes()]
    if index_name not in existing_indexes:
        pinecone_client.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region=os.getenv("PINECONE_ENVIRONMENT"))
        )

    return pinecone_client.Index(index_name)
