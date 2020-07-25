import boto3

s3 = boto3.client('s3')


def upload_to_s3(filepath, s3filepath, extra={}):

    s3.upload_file(filepath, 'fantasydataobj', s3filepath, ExtraArgs=extra)
