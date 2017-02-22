# -*- coding: utf-8 -*-


import flask
import requests

app = flask.Flask(__name__)


@app.route('/<path:url>')
def proxy(url):
    request = requests.get(url, stream=True, data=flask.request.args)
    response = flask.Response(flask.stream_with_context(request.iter_content()),
                              content_type=request.headers['content-type'])
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':
    app.debug = True
    app.run()
