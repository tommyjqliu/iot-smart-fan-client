import boto3
import time
import requests
import subprocess


s3_client = boto3.client('s3')
transcribe_client = boto3.client('transcribe')

# Define variables
TIME_LISTENING = 10
num = 1
bucket_name = 'voice-recognition-iot1'
file_name = f'test{num}.wav'
s3_file_path = f's3://{bucket_name}/{file_name}'
transcription_job_name = 'testTranscriptionJob{num}'

# Upload to S3
def upload_to_s3(file_name, bucket_name):
    try:
        s3_client.upload_file(file_name, bucket_name, file_name)
        print(f'Successfully uploaded {file_name} to {bucket_name}')
    except Exception as e:
        print(f'Error uploading {file_name} to {bucket_name}: {e}')

# Starting a transcription
def start_transcription_job(job_name, s3_uri):
    try:
        response = transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': s3_uri},
            MediaFormat='wav',
            LanguageCode='en-US'
        )
        print(f'Successfully started transcription job: {job_name}')
    except Exception as e:
        print(f'Error starting transcription job: {e}')
# this will get the transcript text from the uri
def fetch_transcript(transcript_uri):
    response = requests.get(transcript_uri)
    if response.status_code == 200:
        transcript_json = response.json()
        transcript_text = transcript_json['results']['transcripts'][0]['transcript']
        return transcript_text
    else:
        raise Exception(f'Error fetching transcript: {response.status_code}')

# Check the status of the transcription job
def get_transcription_result(job_name):
    while True:
        response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
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
def countdown(seconds):
    for i in range(seconds, 0, -1):
        print("Start Listiening")
        print(f"Countdown: {i}")
        time.sleep(1)
    print("End Listiening")

# Start the 10-second countdown


if __name__ == '__main__':

    # Step 1: Recording the audio
    try:
        subprocess.run(["arecord", "-D", "plughw:1,0", f"--duration={TIME_LISTENING}", file_name], check=True)
        countdown(TIME_LISTENING + 2)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

    # Step 2: upload the file
    upload_to_s3(file_name, bucket_name)

    # Step 3: Start the transcription job
    start_transcription_job(transcription_job_name, s3_file_path)

    # Step 4: Wait for the transcription job to complete
    try:
        transcript_uri = get_transcription_result(transcription_job_name)
        # print(f'Transcription completed. Transcript URL: {transcript_uri}')
        # Step 5: Fetch the transcript(text) from the transcript URI
        transcript_text = fetch_transcript(transcript_uri)
        print(f'Transcript Text:  {transcript_text}')
    except Exception as e:
        print(f'Error getting transcription result: {e}')