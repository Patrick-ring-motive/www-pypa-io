from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import http.client
import asyncio

from api.index import *

httpd = ThreadingHTTPServer(('', 8000), handler)
httpd.serve_forever()

