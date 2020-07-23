import re
import json
import logging
from bson import ObjectId
from flask import Response
from flask.views import View
from datetime import datetime, timedelta
from fantasystats.tools.converters import JSONEncoder


class BaseView(View):
    def __init__(self):
        now_date = datetime.now() - timedelta(hours=5)
        self.now_date = datetime(now_date.year, now_date.month, now_date.day)

        self._data = dict()
        self._data['now_date'] = self.now_date,
        self._data['strip_html'] = self.strip_html,
        self._data['cut_text'] = self.cut_text,
        self._data['enumerate'] = enumerate

    def write_json(self, data, status_code=200):
        result = {
            'data': data,
            'status': status_code
        }
        return Response(
            json.dumps(result, cls=JSONEncoder),
            mimetype="text/json",
            headers={'Access-Control-Allow-Origin': '*'},
            status=status_code
        )

    def strip_html(self, content):
        try:
            content = content.decode('utf-8')
        except Exception as e:
            logging.info(e)
            pass

        content = re.sub('<[^>]*>', ' ', content)
        content = re.sub('&[^;]+;', ' ', content)

        return content

    def cut_text(self, content, length):

        words = content.split(' ')
        new_content = []
        new_content_length = 0
        for w in words:
            new_content.append(w)
            new_content_length += len(w)

            if new_content_length >= length:
                break

        return ' '.join(new_content)
