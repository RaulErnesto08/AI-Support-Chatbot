import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

def upload_txt_to_pinecone(directory_path, index_name, namespace):
    """Load text files from a directory, split them, and upload to Pinecone."""
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # Load documents from text files in the directory
    loader = DirectoryLoader(directory_path, glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()

    # Split documents into smaller chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    # Create or update the Pinecone index
    vector_store = PineconeVectorStore.from_documents(
        docs,
        embedding=embeddings,
        index_name=index_name,
        namespace=namespace
    )

    print(f"Successfully uploaded {len(docs)} text chunks to Pinecone in namespace '{namespace}'.")

if __name__ == "__main__":
    # Directory path where .txt files are located
    directory_path = os.path.join("data", "texts")

    # Pinecone index details
    index_name = "chatbot"
    namespace = "faqs"

    try:
        upload_txt_to_pinecone(directory_path, index_name, namespace)
    except Exception as e:
        print(f"An error occurred: {e}")
