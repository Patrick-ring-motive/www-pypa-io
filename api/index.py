import asyncio
import sys
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import http.client
from api.src.xhttp import *
from api.src.excepts import *
from api.src.promises import *

env = 'test'
if sys.version_info.minor == 9:
  env = 'prod'

#print(env)

hostTarget = 'www.pypa.io'

class handler(BaseHTTPRequestHandler):  
  async def do_METHOD(request,data):
    try:
      request.hostTarget=hostTarget
      request.localhost = request.headers['Host']
      request.refererHost=request.localhost
      if request.headers['Localhost']:
        request.refererHost=request.headers['Localhost']
      response = await fetchResponse(request,hostTarget)
      resBody = await go(await promise(readResponseBody,[response]))
      request.send_response(response.status) 
      headers = response.getheaders()
      for header in headers:
        if header[0]=='Transfer-Encoding':
          continue
        if header[0]=='Connection':
          continue
        if header[0]=='Content-Length':
          continue
        try:
          request.send_header(header[0], header[1].replace(hostTarget,request.localhost,1))
        except:
          continue
      request.send_header('status','200')
      await endHeaders(request)
      await writeResponseBody(request,await resBody)
    except:
      request.send_response(200)
      request.send_header('Content-type', 'text/html')
      await endHeaders(request)
      await writeResponseBody(request,b'\x03\x04')
    request.wfile.flush()
    if hasattr(request,'localhost'):
      if env == 'test':
       request.wfile.close()
       closeRequest(request)
       none()
  def do_TRY(request,data):
    try:
      asyncio.run(request.do_METHOD(request))
    except:
      return
  def do_GET(request):
    return request.do_TRY(request)
  def do_POST(request):
    return request.do_TRY(request)
  def do_PUT(request):
    return request.do_TRY(request)
  def do_PATCH(request):
    return request.do_TRY(request)
  def do_HEAD(request):
    return request.do_TRY(request)
  def do_DELETE(request):
    return request.do_TRY(request)
  def do_CONNECT(request):
    return request.do_TRY(request)
  def do_TRACE(request):
    return request.do_TRY(request)
  def do_OPTIONS(request):
    try:
      asyncio.run(writeResponseBody(request,b'*'))
    except:
      return



