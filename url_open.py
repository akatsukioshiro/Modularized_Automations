import webbrowser
import os
import subprocess
subprocess.call("start /min cmd /k python.exe server_test.py",shell=True)
cwd = os.getcwd()
url = 'http://127.0.0.1:8668'
chrome_path = '\"'+cwd+'\GoogleChromePortable64\GoogleChromePortable.exe" %s'
chrome_path=chrome_path.replace("\\","/")
webbrowser.get(str(chrome_path)).open_new_tab(url)
