from django.shortcuts import render

# Create your views here.
import os
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from moviepy.editor import VideoFileClip
import whisper
from transformers import pipeline
import pymongo
from googletrans import Translator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get values from .env
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME")

# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]

# Load Whisper Model
whisper_model = whisper.load_model("base")

# Load Summarization Model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

UPLOAD_DIR = "uploaded_videos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def extract_audio(video_path):
    """
    Extract audio from video and save as WAV file.
    """
    try:
        clip = VideoFileClip(video_path)
        audio_path = video_path.replace('.mp4', '.wav')
        clip.audio.write_audiofile(audio_path)
        return audio_path
    except Exception as e:
        raise Exception(f"Error extracting audio: {e}")

def transcribe_audio(audio_path):
    """
    Convert audio to text using OpenAI Whisper.
    """
    try:
        result = whisper_model.transcribe(audio_path)
        return result['text']
    except Exception as e:
        raise Exception(f"Error transcribing audio: {e}")

def summarize_text(text):
    """
    Summarize extracted text.
    """
    try:
        summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
        print("Text summarized")
        return summary[0]['summary_text']
    except Exception as e:
        raise Exception(f"Error summarizing text: {e}")

# Initialize Translator
translator = Translator()

def translate_text(text, target_language="ta"):
    """
    Translate text to the target language (Tamil by default).
    """
    try:
        translation = translator.translate(text, dest=target_language)
        return translation.text
    except Exception as e:
        raise Exception(f"Error translating text: {e}")

@api_view(['POST'])
def upload_video(request):
    """
    Upload video, process it, and store metadata in MongoDB.
    """
    video = request.FILES.get('video')
    if not video:
        return JsonResponse({'error': 'No video uploaded'}, status=400)

    video_path = os.path.join(UPLOAD_DIR, video.name)
    with open(video_path, 'wb') as f:
        for chunk in video.chunks():
            f.write(chunk)

    try:
        audio_path = extract_audio(video_path)
        transcript = transcribe_audio(audio_path)
        summary = summarize_text(transcript)

        # Translate the summary to Tamil
        tamil_summary = translate_text(summary, target_language="ta")

        video_data = {
            "title": video.name,
            "video_path": video_path,
            "transcript": transcript,
            "summary": summary,
            "tamil_summary":tamil_summary
        }
        collection.insert_one(video_data)
        print("Summarized successfully")
        return JsonResponse({'message': 'Video processed successfully!', 'summary': summary,'tamil_summary':tamil_summary})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
