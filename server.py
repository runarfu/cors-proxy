# -*- coding: utf-8 -*-


import flask
import flask_cors
import requests

app = flask.Flask(__name__)

available_methods = [
    "GET",
    "HEAD",
    "POST",
    "PUT",
    "DELETE",
    "PATCH",
    "OPTIONS",
]


@app.route("/<path:url>", methods=available_methods)
@flask_cors.cross_origin(
    expose_headers="*",
    supports_credentials=True,
)
def proxy(url):
    print(flask.request.cookies)
    session = requests.Session()
    parameters = {
        **flask.request.args.to_dict(),
        **flask.request.form.to_dict(),
    }
    response = session.request(
        method=flask.request.method,
        url=url,
        stream=True,
        data=parameters,
        cookies=flask.request.cookies,
    )
    custom_response = flask.Response(
        flask.stream_with_context(response.iter_content()),
        content_type=response.headers["content-type"]
        if "content-type" in response.headers.keys()
        else None,
        status=response.status_code,
    )
    for cookie in session.cookies:
        custom_response.set_cookie(
            key=cookie.name,
            value=cookie.value,
            expires=cookie.expires,
        )
    return custom_response


@app.errorhandler(404)
def help_message(e):
    message = """
Usage:

/       Shows this help message
/<url>  Make a request to <url>

Source code : https://github.com/sehnryr/cors-proxy
    """.strip()

    response = flask.make_response(message, 400)
    response.mimetype = "text/plain"
    return response


@app.errorhandler(Exception)
def default(e):
    message = "The URL scheme is neither HTTP nor HTTPS"

    response = flask.make_response(message, 400)
    response.mimetype = "text/plain"
    return response


if __name__ == "__main__":
    app.debug = True
    app.run()
