from boto3 import session
from botocore.config import Config

from shop_app.settings import settings


session_s3 = session.Session()

s3 = session_s3.client(
    's3',  
    endpoint_url=f"https://{settings.host_minio}:{settings.port_minio_2}",
    aws_access_key_id=settings.minio_user, 
    aws_secret_access_key=settings.minio_password,
    config=Config(signature_version='v4')
)
