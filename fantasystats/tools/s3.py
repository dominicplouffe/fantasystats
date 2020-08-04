import boto3

s3 = boto3.client('s3')


def upload_to_s3(filepath, s3filepath, extra={}):

    s3.upload_file(filepath, 'fantasydataobj', s3filepath, ExtraArgs=extra)


def list_objects(key):
    return s3.list_objects(
        Bucket='fantasydataobj',
        Prefix=key
    )


def get_object(key):

    return s3.get_object(Bucket='fantasydataobj', Key=key)


def iter_key(key):

    res = boto3.resource('s3')
    bucket = res.Bucket('fantasydataobj')

    for elem in bucket.objects.all():
        if elem.key.startswith(key):
            yield {'key': elem.key, 'obj': get_object(elem.key)}
