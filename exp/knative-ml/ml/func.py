from parliament import Context
from flask import Request
import os
import boto3

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
    ret = in_s3.list_objects(Bucket=in_bucket)
    return repr(ret), 200

