# import http.server
import socketserver

# PORT = 8668
# Handler = http.server.SimpleHTTPRequestHandler

# with socketserver.TCPServer(("", PORT), Handler) as httpd:
    # print("serving at port", PORT)
    # httpd.serve_forever()

import json
import os
import subprocess
from http.server import BaseHTTPRequestHandler,HTTPServer

class MyHandler(BaseHTTPRequestHandler):
	def do_OPTIONS(self):           
		self.send_response(200, "ok")       
		self.send_header('Access-Control-Allow-Origin', '*')                
		self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
		self.send_header("Access-Control-Allow-Headers", "X-Requested-With")        

	def do_GET(self):           
		self.send_response(200)
		self.send_header('Access-Control-Allow-Origin', '*')
		self.send_header('Content-type', 'text/html')                                    
		self.end_headers()
		with open('index.html') as htmlfile:
			self.wfile.write(str.encode(htmlfile.read()))
		self.connection.shutdown(1) 

	def do_POST(self):
		self.send_response(200)
		self.send_header('Access-Control-Allow-Origin', '*')
		self.send_header('Content-type', 'text/html')                       
		self.end_headers()
		self.wfile.write(b'<html><head><meta charset=\'utf-8\'></head><body></body></html>')
		#if(self.path == '/HI'):
		print("bye")
		print(self.client_address)
		print(self.server)
		print(self.request_version)
		print(self.headers)
		print(self.sys_version)
		print(self.MessageClass)
		print(self.rfile)
		print(int(self.headers.get('Content-Length')))
		content_len = int(self.headers.get('Content-Length'))
		post_body = self.rfile.read(content_len)
		print(post_body.decode("utf-8"))
		json_output=json.loads(post_body.decode("utf-8"))
		if(json_output["program"]=="python_1"):
			os.system('python.exe python_program.py "'+json_output["message"]+'"')
		elif(json_output["program"]=="notepad"):
			if(os.path.isfile(".\\Programs\\"+json_output["message"]+".py")!= True):
				f=open(".\\Programs\\"+json_output["message"]+".py","w+")
				f.write("")
				f.close()
			subprocess.call('notepad \".\\Programs\\'+json_output["message"]+'.py\"',shell=True)
		self.connection.shutdown(1) 

PORT = 8668

handler = MyHandler

server = HTTPServer(('', PORT), handler)
server.serve_forever()