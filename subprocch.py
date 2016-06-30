import subprocess
import os

"""
def __test__(cmd):
	cmd = cmd.split()
	
	try:
		subprocess.call(cmd, stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)
		return True
	except OSError as e:
	    if e.errno == os.errno.ENOENT:
	        return False
	    else:
	        return False

print __test__(raw_input("cmd: "))

#print subprocess.call(['brew', 'ls', '--versions', 'chromedriver'], stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)

#print subprocess.call(["brew ls --versions chromedriver"], stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)

#print subprocess.call('pip install chromedriver', stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)
#print subprocess.call(['pip', 'show', 'chromedriver'], stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)
"""
cmd = raw_input('cmd')
cmd = cmd.split()
try:
    subprocess.check_call(cmd, stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)
    print True
except subprocess.CalledProcessError:
    print False
except OSError:
    print False