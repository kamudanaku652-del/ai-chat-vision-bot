#!/usr/bin/env python3
"""
AI Engine - Menggunakan Hugging Face API (Gratis)
"""

import os
import requests
import logging
from dotenv import load_dotenv
from PIL import Image
import io

load_dotenv()

logger = logging.getLogger(__name__)

# Hugging Face Models (Free!)
HF_API_URL = "https://api-inference.huggingface.co/models"

# Models
TEXT_GENERATION_MODEL = "gpt2"  # Model gratis untuk text
IMAGE_ANALYSIS_MODEL = "Salesforce/blip-image-captioning-base"  # Gratis image caption


def chat_with_ai(user_message: str, max_length: int = 100) -> str:
    """
    Chat dengan AI menggunakan Hugging Face
    
    Args:
        user_message: Pesan dari user
        max_length: Panjang maksimal response
    
    Returns:
        Response dari AI
    """
    try:
        # Jika pakai token HF (opsional)
        hf_token = os.getenv('HUGGING_FACE_API_TOKEN')
        headers = {}
        if hf_token:
            headers = {"Authorization": f"Bearer {hf_token}"}
        
        # Prompt engineering sederhana
        prompt = f"Q: {user_message}\nA:"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": max_length + len(prompt.split()),
                "do_sample": True,
                "temperature": 0.7,
                "top_p": 0.9
            }
        }
        
        response = requests.post(
            f"{HF_API_URL}/{TEXT_GENERATION_MODEL}",
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                text = result[0].get('generated_text', '')
                # Clean up prompt dari response
                answer = text.replace(prompt, '').strip()
                return answer if answer else "Maaf, tidak bisa generate response. Coba pertanyaan lain!"
            return "Maaf, format response tidak sesuai."
        elif response.status_code == 503:
            return "⏳ Model sedang loading (gratis tier). Tunggu sebentar, coba lagi dalam 10 detik!"
        else:
            logger.error(f"API Error: {response.status_code} - {response.text}")
            return f"❌ Error: {response.status_code}. Coba lagi nanti!"
            
    except requests.exceptions.Timeout:
        return "⏱️ Timeout. Jaringan kamu lambat atau API sedang busy. Coba lagi!"
    except Exception as e:
        logger.error(f"Error in chat_with_ai: {e}")
        return f"❌ Error: {str(e)}"


def analyze_image(image_path: str, question: str = None) -> str:
    """
    Analisis gambar menggunakan AI
    
    Args:
        image_path: Path ke gambar
        question: Pertanyaan tentang gambar (opsional)
    
    Returns:
        Analisis/caption gambar
    """
    try:
        # Baca gambar
        if not os.path.exists(image_path):
            return "❌ File gambar tidak ditemukan."
        
        with open(image_path, 'rb') as img_file:
            image_data = img_file.read()
        
        # Validasi format
        try:
            img = Image.open(io.BytesIO(image_data))
            if img.size[0] > 1024 or img.size[1] > 1024:
                img.thumbnail((1024, 1024))
                img_buffer = io.BytesIO()
                img.save(img_buffer, format='JPEG')
                image_data = img_buffer.getvalue()
        except Exception as e:
            logger.warning(f"Image validation warning: {e}")
        
        hf_token = os.getenv('HUGGING_FACE_API_TOKEN')
        headers = {}
        if hf_token:
            headers = {"Authorization": f"Bearer {hf_token}"}
        
        # Image captioning
        response = requests.post(
            f"{HF_API_URL}/{IMAGE_ANALYSIS_MODEL}",
            data=image_data,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                caption = result[0].get('generated_text', 'Tidak bisa analyze gambar')
                
                # Jika ada pertanyaan spesifik
                if question and question != "Apa yang ada di gambar ini?":
                    caption += f"\n\n📝 Untuk pertanyaan '{question}':\n"
                    # Generate jawaban dengan context gambar
                    answer = chat_with_ai(f"Gambar menunjukkan: {caption}. Pertanyaan: {question}")
                    caption += answer
                
                return caption
            return "Maaf, format response tidak sesuai."
        elif response.status_code == 503:
            return "⏳ Model sedang loading (gratis tier). Tunggu 10-20 detik, coba lagi!"
        else:
            logger.error(f"Image API Error: {response.status_code}")
            return f"❌ Error analyzing image: {response.status_code}"
            
    except requests.exceptions.Timeout:
        return "⏱️ Timeout. Coba lagi dengan gambar yang lebih kecil!"
    except Exception as e:
        logger.error(f"Error in analyze_image: {e}")
        return f"❌ Error: {str(e)}"


def get_model_status() -> dict:
    """
    Check status models
    """
    try:
        hf_token = os.getenv('HUGGING_FACE_API_TOKEN')
        headers = {}
        if hf_token:
            headers = {"Authorization": f"Bearer {hf_token}"}
        
        models = {
            'text_generation': TEXT_GENERATION_MODEL,
            'image_analysis': IMAGE_ANALYSIS_MODEL
        }
        
        status = {}
        for name, model in models.items():
            try:
                resp = requests.head(
                    f"{HF_API_URL}/{model}",
                    headers=headers,
                    timeout=5
                )
                status[name] = "✅ Online" if resp.status_code == 200 else "⚠️ Loading"
            except:
                status[name] = "❓ Unknown"
        
        return status
    except Exception as e:
        logger.error(f"Error checking model status: {e}")
        return {"error": str(e)}
