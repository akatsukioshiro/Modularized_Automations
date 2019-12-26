# import http.server
#import socketserver

# PORT = 8668
# Handler = http.server.SimpleHTTPRequestHandler

# with socketserver.TCPServer(("", PORT), Handler) as httpd:
	# print("serving at port", PORT)
	# httpd.serve_forever()

import json
import os
import subprocess
from http.server import BaseHTTPRequestHandler,HTTPServer
#from socketserver import ThreadingMixIn
import socketserver
import threading
from queue import Queue
# main="""
# import subprocess
# """

class ThreadingMixIn:
	"""Mix-in class to handle each request in a new thread."""

	# Decides how threads will act upon termination of the
	# main process
	daemon_threads = False
	# If true, server_close() waits until all non-daemonic threads terminate.
	block_on_close = True
	# For non-daemonic threads, list of threading.Threading objects
	# used by server_close() to wait for all threads completion.
	_threads = None

	def process_request_thread(self, request, client_address):
		"""Same as in BaseServer but as a thread.
		In addition, exception handling is done here.
		"""
		try:
			try:
				self.finish_request(request, client_address)
			except ValueError:
				pass
		except Exception:
			self.handle_error(request, client_address)
		finally:
			self.shutdown_request(request)

	def process_request(self, request, client_address):
		"""Start a new thread to process the request."""
		t = threading.Thread(target = self.process_request_thread,
							 args = (request, client_address))
		t.daemon = self.daemon_threads
		if not t.daemon and self.block_on_close:
			if self._threads is None:
				self._threads = []
			self._threads.append(t)
		t.start()

	def server_close(self):
		super().server_close()
		if self.block_on_close:
			threads = self._threads
			self._threads = None
			if threads:
				for thread in threads:
					thread.join()

def worker(json_output):
	if(json_output["program"]=="python_1"):
		os.system('python.exe python_program.py "'+json_output["message"]+'"')
	elif(json_output["program"]=="notepad"):
		if(os.path.isfile(".\\Programs\\"+json_output["message"]+".py")!= True):
			f=open(".\\Programs\\"+json_output["message"]+".py","w+")
			f.write("")
			f.close()
		subprocess.call('notepad \".\\Programs\\'+json_output["message"]+'.py\"',shell=True)
		

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
		json_output=""
		json_output=json.loads(post_body.decode("utf-8"))
		self.connection.close() #VERY IMPORTANT FOR THREAD COUNT
		self.finish() #VERY IMPORTANT FOR THREAD COUNT
		worker(json_output)
		#self.connection.shutdown(1) #IS USEFUL AND NOT USEFUL AT THE SAME TIME, SINCE CONNECTION CLOSED, SHUTDOWN NOT NEEDED THROWS ERROR BUT NEEDED

# PORT = 8668

# handler = MyHandler

# server = HTTPServer(('', PORT), handler)
# server.serve_forever()


#class ThreadingSimpleServer(ThreadingMixIn,HTTPServer):
#	pass


class ThreadPoolMixIn(ThreadingMixIn):
	numThreads = 500 #total number of parallel threads allowed PARALLELY ACTIVE
	allow_reuse_address = True  # seems to fix socket.error on server restart
	def serve_forever(self):
		self.requests = Queue(self.numThreads)
		for x in range(self.numThreads):
			t = threading.Thread(target = self.process_request_thread)
			t.setDaemon(1)
			t.start()
		while True:
			self.handle_request()
		self.server_close()
	def process_request_thread(self):
		while True:
			ThreadingMixIn.process_request_thread(self, *self.requests.get())
	def handle_request(self):
		try:
			request, client_address = self.get_request()
		except socket.error:
			return
		if self.verify_request(request, client_address):
			self.requests.put((request, client_address))

class ThreadedServer(ThreadPoolMixIn, HTTPServer):
	pass
		
hostName = "localhost"
serverPort = 8668

if __name__ == "__main__":
	webServer = ThreadedServer((hostName, serverPort), MyHandler)
	#webServer.socket = ssl.wrap_socket(webServer.socket, keyfile='./privkey.pem',certfile='./certificate.pem', server_side=True)
	print("Server started http://%s:%s" % (hostName, serverPort))

	try:
		webServer.serve_forever()
	except KeyboardInterrupt:
		pass

	webServer.server_close()
	print("Server stopped.")