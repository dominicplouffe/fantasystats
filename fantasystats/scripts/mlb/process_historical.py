import os
import json
from fantasystats.services.mlb import parser

FILE_LOC = '/Users/dplouffe/projects/fantasystats/mlb/games/2019/'


def process_file(file_name):

    f = open('%s%s' % (FILE_LOC, file_name), 'r')
    content = f.read().encode('utf-8')
    f.close()

    try:
        data = json.loads(content)
    except json.decoder.JSONDecodeError:
        return

    parser.process_data(data)


if __name__ == '__main__':

    files = os.listdir(FILE_LOC)

    for f in files:
        process_file(f)
