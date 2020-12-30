import json
from fantasystats.context import logger
from fantasystats.tools import s3
from fantasystats.services.mlb import parser

year = '2017'


def process_file(s3obj):

    logger.info('process_historical,%s' % s3obj['key'])
    content = s3obj['obj']['Body'].read()
    if len(content) == 0:
        return

    try:
        data = json.loads(content)
    except json.decoder.JSONDecodeError as e:
        print(e)
        return

    parser.process_data(data)


if __name__ == '__main__':

    files = s3.iter_key('mlb/files/%s' % year)

    for f in files:
        process_file(f)
