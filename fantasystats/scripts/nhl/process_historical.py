import json
from fantasystats.context import logger
from fantasystats.tools import s3
from fantasystats.services.nhl import parser

year = '20192020'


def process_file(s3obj):

    logger.info('process_historical,%s' % s3obj['key'])
    content = s3obj['obj']['Body'].read()
    if len(content) == 0:
        return

    try:
        data = json.loads(content)
    except json.decoder.JSONDecodeError as e:
        e)
        return

    parser.process_data(data)


if __name__ == '__main__':

    files=s3.iter_key('nhl/files/%s' % year)

    for f in files:
        process_file(f)
