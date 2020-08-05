from flask import Flask
from flask_cors import CORS
import sys

from fantasystats.tools.converters import ObjectIDConverter
from fantasystats.api.base_view import BaseView
from fantasystats.api.mlb import mlb
from fantasystats.api.nhl import nhl

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)
app.url_map.converters['ObjectID'] = ObjectIDConverter
app.register_blueprint(mlb)
app.register_blueprint(nhl)
app.secret_key = '1qaz2wsx!'


class StatusView(BaseView):

    def dispatch_request(self):
        return self.write_json({'status': 'ok'})


app.add_url_rule(
    '/api/status',
    view_func=StatusView.as_view('/api/status')
)

if __name__ == "__main__":

    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9500
    app.run(debug=True, port=port, host='127.0.0.1')
