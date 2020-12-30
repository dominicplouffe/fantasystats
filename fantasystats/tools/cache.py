from fantasystats.context import REDIS, logger
from flask import request, Response


def memorize(func):
    def wrapper(*args, **kwargs):

        view = args[0]
        key = request.url.lower()
        key = key.replace('force_query=true', '')
        if key.endswith('?') or key.endswith('/'):
            key = key[0:-1]
        data = REDIS.get(key)
        if data is None or request.args.get(
            'force_query', 'false'
        ).lower() == 'true':
            logger.info('data not found or force query,%s' % key)
            res = func(*args, **kwargs)
            REDIS.set(key, res.get_data(), view.cache_time)
            return res

        return Response(
            data,
            mimetype="text/json",
            headers={'Access-Control-Allow-Origin': '*'},
            status=200
        )
    return wrapper
