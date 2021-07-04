from flask import request, jsonify
from datetime import datetime
import traceback


def handle_exceptions(app):

    @app.errorhandler(Exception)
    def all_exception_handler(error):

        data = None
        if request.data:
            data = dict(request.data)
        elif request.get_json(silent=True):
            data = request.get_json(silent=True)

        error_info = {
            'url': request.base_url,
            'headers': dict(request.headers),
            'params': dict(request.form),
            'args': dict(request.args),
            'data': data,
            'exception_date': int(datetime.utcnow().timestamp()),
            'exception': {
                'msg': str(error),
                'traceback': traceback.format_exc()
            }
        }

        return jsonify(error_info), 500
