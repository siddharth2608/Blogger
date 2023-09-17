import os
import secrets
import pika
from aws_connections import *
from controllers import *
from werkzeug.utils import secure_filename
import controllers
import base64
import json
import uuid


def main():
	connection = pika.BlockingConnection(pika.URLParameters("amqps://vdmysoyb:UPUOLzZyoAzNBZ051hSYvK1HEOhbtQkI@armadillo.rmq.cloudamqp.com/vdmysoyb"))
	channel = connection.channel()
	channel.queue_declare(queue='image_queue')


	channel.basic_consume(queue='image_queue', on_message_callback=callback, auto_ack=True)
	channel.start_consuming()

def callback(ch, method, properties, body):
	S3_BUCKET = "bloggapp"
	data = json.loads(body)
	
	file = data["image_data"]
	imagedata = file.split(",")
	
	post_id = data["post_id"]
	print(post_id)
	url_lst=[]
	for st in imagedata:
		decoded_image_bytes = base64.b64decode(st)
		key = str(uuid.uuid4())
		stored_filename_url = upload_image_data_to_s3(decoded_image_bytes,key)
		url_lst.append(stored_filename_url)
	print(url_lst)
	csurl = ",".join(url_lst)
	data = {"post_id":post_id,"url":csurl}
	save_imageurl_in_posts(data)


if __name__ == '__main__':
    main()