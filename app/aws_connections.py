import boto3
import uuid
from io import BytesIO

s3 = boto3.client('s3',

	aws_access_key_id = 'AKIASIQVCOHQG3CZSOVE',
	aws_secret_access_key = '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',
	region_name = 'us-east-1'
	)

ALLOWED_FILE_TYPES = {'png', 'jpg', 'jpeg'}
S3_BUCKET_NAME = 'bloggapp'
S3_EXPIRES_IN_SECONDS = 100

def get_file_type(filename): 
    return '.' in filename and filename.rsplit('.', 1)[1].lower()

def is_file_type_allowed(filename):
    return get_file_type(filename) in ALLOWED_FILE_TYPES

def upload_file_to_s3(file, provided_file_name):
    stored_file_name = f'{str(uuid.uuid4())}.{get_file_type(provided_file_name)}'
    image_stream = BytesIO(file)
    s3.upload_fileobj(image_stream, S3_BUCKET_NAME, stored_file_name,ExtraArgs={'ACL': 'public-read'})
    return stored_file_name

def upload_image_data_to_s3(image_byte,filename):
	s3.put_object(Bucket=S3_BUCKET_NAME, Key=filename, Body=image_byte, ContentType='image/jpeg')
	url =  f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{filename}"
	return url