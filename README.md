
# AI Support Chatbot

## Project Description

The **AI Support Chatbot** is an interactive application designed to:
- Process **text inputs** and **voice messages** from users.
- Perform **sentiment analysis** on user inputs.
- Handle **task-oriented intents** such as creating or managing orders.
- Support **escalation to human agents** when required.
- Generate **voice-based responses** to user queries using OpenAI's Whisper and Text-to-Speech (TTS).

The project integrates:
- **LangChain**: For constructing and managing conversational prompts.
- **Pinecone**: As a vector database for storing and retrieving context.
- **OpenAI Whisper**: For speech-to-text transcription.
- **OpenAI GPT-4**: For generating conversational responses.
- **OpenAI Text-to-Speech**: For generating voice-based assistant replies.

The application has:
- **FastAPI**: As the backend for processing inputs and managing APIs.
- **Streamlit**: As the frontend for user interaction.

---

## Instructions to Run the Project

### 1. Prerequisites
- **Docker** and **Docker Compose** installed.
  - Installation guides:
    - [Docker Install](https://docs.docker.com/get-docker/)
    - [Docker Compose Install](https://docs.docker.com/compose/install/)

- Optional for Local Development:
  - Python 3.8 or later installed.

### 2. Clone the Repository
```bash
git clone https://github.com/RaulErnesto08/AI-Support-Chatbot.git
cd AI-Support-Chatbot
```

### 3. Environment Variables Configuration  
The project requires two `.env` files—one for the backend and one for the frontend.

1. Copy the example `.env` files and rename them:
   - Backend:
     ```bash
     cp backend/app/.env.example backend/app/.env
     ```
   - Frontend:
     ```bash
     cp frontend/.env.example frontend/.env
     ```

2. Open each `.env` file and fill in the required variables:

   **Example for Backend `.env`**:
   ```plaintext
   OPENAI_API_KEY="your_openai_api_key_here"
   PINECONE_API_KEY="your_pinecone_api_key_here"
   PINECONE_ENVIRONMENT="your_pinecone_env_here"
   ```

   **Example for Frontend `.env`**:
   ```plaintext
   OPENAI_API_KEY="your_openai_api_key_here"
   PINECONE_API_KEY="your_pinecone_api_key_here"
   PINECONE_ENVIRONMENT="your_pinecone_env_here"
   BACKEND_URL="http://127.0.0.1:8000"
   ```

---

## Run the Project with Docker

### 1. Build and Start Containers
Run the following command in the root directory of the project:
```bash
docker-compose up --build
```

### 2. Access the Application
- **Frontend (Streamlit)**: `http://localhost:8501`
- **Backend (FastAPI)**: `http://localhost:8000`

---

## Run the Project Locally (Without Docker)

### 1. Set Up a Virtual Environment
1. Create the virtual environment:
   ```bash
   python3 -m venv venv
   ```
2. Activate the environment:
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

### 2. Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### 3. Run the Backend (FastAPI)
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```
3. The backend will be available at `http://127.0.0.1:8000`.

### 4. Run the Frontend (Streamlit)
1. Navigate to the `frontend` directory:
   ```bash
   cd ../frontend
   ```
2. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```
3. The frontend will be available at `http://127.0.0.1:8501`.

---

## Features

- **Text and Voice Inputs**: The chatbot accepts text and voice inputs.
- **Sentiment Analysis**: Analyzes user sentiment using Hugging Face Transformers.
- **Intent Detection**: Supports task-specific intents like creating orders, checking orders, or escalating issues.
- **Voice Responses**: Generates audio replies for user queries.
- **Contextual Awareness**: Utilizes LangChain and Pinecone for context retrieval.
- **Chat History**: Retains the full conversation history for reference.

---

## To-Do Checklist

### Completed:
- [x] **Project Setup**:
  - Created the project structure for FastAPI (backend) and Streamlit (frontend).
- [x] **Voice Interaction**:
  - Integrated OpenAI Whisper for speech-to-text transcription.
  - Added text-to-speech functionality using OpenAI's API.
- [x] **Sentiment Analysis**:
  - Implemented Hugging Face Transformers for analyzing user sentiment.
- [x] **Task Automation**:
  - Built intents like "create_order" and "escalate_to_human."
  - Added mocked actions for testing.
- [x] **Backend-Frontend Integration**:
  - Enabled frontend to send audio files to the backend.
  - Displayed results (text and audio) in the frontend.
- [x] **Deployment**:
  - Containerized the application using Docker.
  - Tested the deployment locally.

---

