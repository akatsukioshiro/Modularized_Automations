# Modularized_Automations
Trying to develop standalone, GUI based coding experiences

## 1. Multithreading 
#### It is essentially able to successfully work due to (1), (2), (3), (4)
##### (1), (2) Shut the connection too soon throwing exception at (4)
##### (3) decides the TOTAL number of parallel threads possible

```python
def do_POST(self):
	self.send_response(200)
	self.send_header('Access-Control-Allow-Origin', '*')
	self.send_header('Content-type', 'text/html')					   
	self.end_headers()
	self.wfile.write(b'<html><head><meta charset=\'utf-8\'></head><body></body></html>')
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
	self.connection.close()  #------------------------------------------------------------- (1)
	self.finish()  #----------------------------------------------------------------------- (2)
	worker(json_output)
```
	
```python
class ThreadPoolMixIn(ThreadingMixIn):
	numThreads = 500  #-------------------------------------------------------------------- (3)
	allow_reuse_address = True
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
```
```python
def process_request_thread(self, request, client_address):
	try:
		try:
			self.finish_request(request, client_address)
		except ValueError:  #---------------------------------------------------------- (4)
			pass
	except Exception:
		self.handle_error(request, client_address)
	finally:
		self.shutdown_request(request)
```
