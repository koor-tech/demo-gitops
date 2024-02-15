from parliament import Context
from flask import Request
import os
import boto3
 
def main(context: Context):
    """ 
    Downloads an S3 file and outputs size
    """
    return repr(os.environ), 200

