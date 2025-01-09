import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

open_ai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def save_audio_file(uploaded_file) -> Path:
    """Save uploaded audio file to disk."""
    audio_path = Path("audio.wav")
    with open(audio_path, "wb") as f:
        f.write(uploaded_file.file.read())
    return audio_path

def speech_to_text(audio_path: Path) -> str:
    """Convert speech to text using OpenAI Whisper."""
    with open(audio_path, "rb") as audio_file:
        transcription = open_ai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcription.text

def text_to_speech(answer: str) -> Path:
    """Convert text to speech and save the audio file in the 'uploads' folder."""
    uploads_dir = Path("../uploads")
    uploads_dir.mkdir(parents=True, exist_ok=True)

    speech_file_path = uploads_dir / "reply.wav"
    try:
        response = open_ai.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=answer
        )

        with open(speech_file_path, "wb") as f:
            f.write(response.content)

        return speech_file_path
    except Exception as e:
        raise RuntimeError(f"Error generating text-to-speech: {e}")