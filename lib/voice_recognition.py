import boto3
import time
import requests
import subprocess

class VoiceRecognition:
    def __init__(self, time_listening=10):
        self.s3_client = boto3.client('s3')
        self.transcribe_client = boto3.client('transcribe')
        self.bucket_name = 'voice-recognition-iot'
        self.time_listening = time_listening
        self.num = 1

    def record_audio(self):
        file_name = f'test{self.num}.wav'
        print(f'Starting to record audio for {self.time_listening} seconds...')
        subprocess.run(["arecord", "-D", "plughw:1,0", self.time_listening, file_name], check=True)
        return file_name

    def upload_to_s3(self, file_name):
        try:
            self.s3_client.upload_file(file_name, self.bucket_name, file_name)
            print(f'Successfully uploaded {file_name} to {self.bucket_name}')
        except Exception as e:
            print(f'Error uploading {file_name} to {self.bucket_name}: {e}')
    
    def start_transcription_job(self, file_name):
        s3_file_path = f's3://{self.bucket_name}/{file_name}'
        transcription_job_name = f'testTranscriptionJob{self.num}'
        try:
            response = self.transcribe_client.start_transcription_job(
                TranscriptionJobName=transcription_job_name,
                Media={'MediaFileUri': s3_file_path},
                MediaFormat='wav',
                LanguageCode='en-US'
            )
            print(f'Successfully started transcription job: {transcription_job_name}')
            return transcription_job_name
        except Exception as e:
            print(f'Error starting transcription job: {e}')

    def get_transcription_result(self, job_name):
        while True:
            response = self.transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
            status = response['TranscriptionJob']['TranscriptionJobStatus']
            if status in ['COMPLETED', 'FAILED']:
                break
            print('Transcription job status: ', status)
            time.sleep(10)  # Wait 10 seconds before checking again

        if status == 'COMPLETED':
            transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
            return transcript_uri
        else:
            raise Exception('Transcription job failed')

    def fetch_transcript(self, transcript_uri):
        response = requests.get(transcript_uri)
        if response.status_code == 200:
            transcript_json = response.json()
            transcript_text = transcript_json['results']['transcripts'][0]['transcript']
            return transcript_text
        else:
            raise Exception(f'Error fetching transcript: {response.status_code}')

    def countdown(self):
        for i in range(self.time_listening, 0, -1):
            print(f"Start Listening")
            print(f"Countdown: {i}")
            time.sleep(1)
        print("End Listening")

    def process_voice_recognition(self):

        file_name = self.record_audio()
        self.countdown()
        print(f'Audio recording complete: {file_name}')
        self.upload_to_s3(file_name)
        job_name = self.start_transcription_job(file_name)
        transcript_uri = self.get_transcription_result(job_name)
        transcript_text = self.fetch_transcript(transcript_uri).lower()
        self.num += 1
        
        print(f'Transcription: {transcript_text}')
        result = ""
        if "turn on" in transcript_text or "on" in transcript_text:
            result = "ON"
        elif "turn off" in transcript_text or "off" in transcript_text:
            result = "OFF"
        elif "speed up" in transcript_text or "up" in transcript_text:
            result = "UP"
        elif "speed down" in transcript_text or "down" in transcript_text:
            result = "DOWN"
        return result
    
    def on_close(self):
        pass
