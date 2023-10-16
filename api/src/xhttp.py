import asyncio
import sys
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import http.client
from api.src.xpy import *

def closeRequest(request):
  if 'close' in request.close:
    none()
async def endHeaders(request):
  return request.end_headers()
async def readResponseBody(res):
  return res.read()
async def writeResponseBody(req,body):
  return req.wfile.write(body+b'\x03\x04')
async def readRequest(req,length):
  if length < 5:
    return b''
  return req.rfile.read(length)
async def connectClient(host):
  return http.client.HTTPSConnection(host)
async def connectRequest(connection, requestCommand, requestPath, requestBody, requestHeaders):
  return connection.request(requestCommand, requestPath, body=requestBody, headers=requestHeaders)
async def connectResponse(connection):
  return connection.getresponse()
async def connectClose(connection):
  connection.close()
async def streamDetach(stream):
  stream.detach()
async def fetchResponse(req,host):  
  connection = await connectClient(host)
  reqHeaders = {}
  reqBody = None
  for header in req.headers:
    if header == 'Connection':
      continue
    if header == 'Transfer-Encoding':
      continue
    reqHeaders[header] = req.headers[header].replace(req.localhost,req.hostTarget)
  requestBodyLength = req.headers['Content-Length']
  if (req.rfile.readable() and requestBodyLength):  
    reqBody = await readRequest(req,int(requestBodyLength));
    if len(reqBody) < 5:
      reqBody = None
  await connectRequest(connection, req.command, req.path, reqBody, reqHeaders)
  res = await connectResponse(connection)
  return res