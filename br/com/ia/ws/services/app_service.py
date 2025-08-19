import base64
import boto3
from botocore.client import Config
from io import BytesIO

class Service:
    def upload(self, data):
        s3 = boto3.client(
            "s3",
            endpoint_url="https://s3.tebi.io",
            aws_access_key_id="HJdpMbpvemObJDAC",
            aws_secret_access_key="dtgzo4WOBv5kOsd02mhAHdlBt7VxUqmBZZEDcqgm",
            config=Config(signature_version="s3v4")
        )
        user = data['user']
        uuid = data['uuid']
        bucket_path = str(user + "/" + uuid + "/original.jpg")
        #print(user, uuid, bucket_path)
        header, encoded = data['picture'].split(",", 1)
        file_bytes = base64.b64decode(encoded)
        file_obj = BytesIO(file_bytes)

        s3.upload_fileobj(
            Fileobj=file_obj,
            Bucket="app-ia",
            Key=bucket_path
        )

        # s3.upload_file(
        #     file_obj,   # arquivo que você tem no seu PC
        #     "app-ia",   # nome do bucket
        #     bucket_path # caminho/objeto no bucket
        # )

