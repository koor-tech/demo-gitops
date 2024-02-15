from parliament import Context
from flask import Request
import os
import boto3
import tempfile

in_endpoint = "http://" + os.environ["INPUTS_BUCKET_HOST"]
in_bucket = os.environ["INPUTS_BUCKET_NAME"]
in_s3 = boto3.client('s3',
    endpoint_url=in_endpoint,
    aws_access_key_id=os.environ["INPUTS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["INPUTS_SECRET_ACCESS_KEY"])

out_endpoint = "http://" + os.environ["OUTPUTS_BUCKET_HOST"]
out_bucket = os.environ["OUTPUTS_BUCKET_NAME"]
out_s3 = boto3.client('s3',
    endpoint_url=in_endpoint,
    aws_access_key_id=os.environ["OUTPUTS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["OUTPUTS_SECRET_ACCESS_KEY"])


def main(context: Context):
    """ 
    Downloads an S3 file and outputs size
    """
    if context.cloud_event is None:
        return "A cloud event is required", 400
    
    event_attributes = context.cloud_event.get_attributes()
    key = event_attributes['subject']
    print("Copying "+ key, flush=True)
    
    tf = tempfile.NamedTemporaryFile()
    
    in_s3.download_file(in_bucket, key, tf.name)
    ret = out_s3.upload_file(tf.name, out_bucket, key)
    return repr(ret), 200

