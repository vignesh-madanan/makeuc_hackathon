import assemblyai
from rekognition_service.rekognition_image_detection import run_reko_on_s3
import requests

def run_stt(audio_url):
    aai = assemblyai.Client(token='043c865143e54ffa94a1c33c6960ab81')
    transcript = aai.transcribe(audio_url=audio_url)
    while transcript.status != 'completed':
        transcript = transcript.get()

    text = transcript.text
    return text

# run_stt('https://1hackathonbucket.s3.us-east-2.amazonaws.com/test_stt.mp3')

def run_stt_requests(audio_url):
    endpoint = "https://api.assemblyai.com/v2/transcript"
    json = {"audio_url": audio_url,"auto_highlights": True}

    headers = {
        "authorization": "043c865143e54ffa94a1c33c6960ab81",
        "content-type": "application/json"
    }

    response = requests.post(endpoint, json=json, headers=headers)

    return response.json()

def run_stt_resp(t_id):
    endpoint = f'https://api.assemblyai.com/v2/transcript/{t_id}'
    headers = {"authorization": "043c865143e54ffa94a1c33c6960ab81"}
    response = requests.get(endpoint, headers=headers)
    return response.json()
    
#op = run_stt_requests('https://1hackathonbucket.s3.us-east-2.amazonaws.com/test_stt.mp3')