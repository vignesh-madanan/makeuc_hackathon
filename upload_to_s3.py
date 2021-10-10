import boto3
import os
from botocore.exceptions import NoCredentialsError

ACCESS_KEY = os.getenv('ASIAQVTFHZQ2ZBDAMCIQ')
SECRET_KEY = os.getenv('87qC2oPTsz+KiGFa9u0JWRgjKh91/cXzavhNdx8M')

print(ACCESS_KEY, SECRET_KEY)
s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                    aws_secret_access_key=SECRET_KEY)

def upload_to_aws(local_file, bucket, s3_file):

    try:
        s3.upload_file(local_file, bucket, s3_file, ExtraArgs={'ACL':'public-read'})
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


#uploaded = upload_to_aws('local_file', 'bucket_name', 's3_file_name')
