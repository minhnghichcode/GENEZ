import os
import requests
import time
import logging
from dotenv import load_dotenv
from pydub import AudioSegment
import io

load_dotenv()

def text_to_speech(text_input: str, voice_name: str, output_path: str, max_retries: int = 3, wait_time: int = 5) -> str:
    """
    Calls the thucchien.ai /audio/speech TTS API, handles WAV or MP3 responses,
    and saves the final output as a standardized MP3 file.
    """
    api_key = os.getenv("API_KEY")
    if not api_key:
        logging.error("API_KEY not found in environment variables.")
        raise ValueError("API_KEY not found in environment variables.")

    url = "https://api.thucchien.ai/audio/speech"
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        "model": "gemini-2.5-pro-preview-tts",
        "input": text_input,
        "voice": voice_name
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=90)
            response.raise_for_status()

            content_type = response.headers.get('Content-Type', '')
            
            # --- CRITICAL FIX: Handle both WAV and MP3 from API ---
            if 'audio/wav' in content_type or 'audio/mpeg' in content_type:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # Use pydub to load audio from memory, regardless of format
                audio_data = io.BytesIO(response.content)
                sound = AudioSegment.from_file(audio_data)
                
                # Export as a standardized MP3 file
                sound.export(output_path, format="mp3")

                logging.info(f"Successfully processed and saved audio to {output_path}")
                return output_path
            else:
                logging.error(f"TTS API returned non-audio content type: {content_type}. Body: {response.text[:200]}")
                return ""

        except requests.exceptions.HTTPError as e:
            if 500 <= e.response.status_code < 600 and attempt < max_retries - 1:
                logging.warning(f"Server error ({e.response.status_code}). Retrying in {wait_time}s... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
            else:
                logging.error(f"HTTP error: {e}. Body: {e.response.text}")
                return ""
        except Exception as e:
            logging.error(f"An unexpected error occurred while processing audio: {e}")
            return ""
            
    logging.error(f"Failed to get a valid response from TTS API after {max_retries} attempts.")
    return ""

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    test_text = "Xin chào, đây là một thử nghiệm chuyển văn bản thành giọng nói."
    test_voice = "Zephyr"
    test_output_path = "output/test_audio.mp3"
    
    text_to_speech(test_text, test_voice, test_output_path)
