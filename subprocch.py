import subprocess
import os

def __test__(cmd):
	
	try:
		subprocess.call(cmd, stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)
		return True
	except OSError as e:
	    if e.errno == os.errno.ENOENT:
	        return False
	    else:
	        return False

print __test__(raw_input("cmd: "))