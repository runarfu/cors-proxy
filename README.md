# cors-proxy
A Flask-based proxy adding Access-Control-Allow-Origin=* to all responses.

Usage:
Start the proxy with `$ python3 server.py`.
You can then access `http://127.0.0.1:5000/<URL>` for any `URL` and any HTTP method. The response content and return code will be forwarded.

Example: Access `https://jsonplaceholder.typicode.com/posts` with `http://127.0.0.1:5000/https://jsonplaceholder.typicode.com/posts`.
