#!"D:\STORE\0-Admin\Desktop\Chatbot-Osiris bkp\python.exe"
import sys
import cgi
import subprocess
sys.stdout.write("Content-Type: text/html")
sys.stdout.write("\n")
sys.stdout.write("\n")
form = cgi.FieldStorage()
subprocess.call("start cmd /k echo "+sys.argv[1], shell=True)# /k echo "+form.getvalue('Message'))
#subprocess.call("C:\\Program Files (x86)\\mRemoteNG\\PuTTYNG.exe -ssh "+form.getvalue('Message'))

 

 

