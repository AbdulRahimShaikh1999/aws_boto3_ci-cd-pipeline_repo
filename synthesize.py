import boto3
import os

# Read text from the file
with open('speech.txt', 'r') as file:
    text = file.read()

# Initialize Polly client
polly_client = boto3.client('polly', region_name='us-east-1')

# Synthesize speech
response = polly_client.synthesize_speech(
    Text=text,
    OutputFormat='mp3',
    VoiceId='Joanna'
)

# Save the audio stream to a local file
output_file = 'output.mp3'
with open(output_file, 'wb') as file:
    file.write(response['AudioStream'].read())

print("✅ Audio file created locally.")

# Initialize S3 client
s3_client = boto3.client('s3', region_name='us-east-1')

# Upload to S3 (bucket name from environment variable)
bucket_name = os.environ['S3_BUCKET']
s3_key = 'polly-audio/output.mp3'  # S3 key (path within bucket)

s3_client.upload_file(output_file, bucket_name, s3_key)

print(f"✅ Uploaded to s3://{bucket_name}/{s3_key}")
