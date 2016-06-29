### python scripts dependencies
### py selenium browser package
### from selenium import webdriver

### py subprocess class package
import subprocess
### py textwrap class package
import textwrap
### py temp class package
import tempfile
### py user class package
import getpass
### py urllib2 class package
import urllib2
### py system class package
import sys
### py os class package
import os
### py regex
import re


### set localfile path
__filepath__ = os.path.dirname(os.path.realpath('__file__'))

### prints prettier strs
class String:
	### formatting 
	PURPLE = '\033[95m'
	CYAN = '\033[96m'
	DARKCYAN = '\033[36m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	END = '\033[0m'
	### regexp for matching "{{string}}"
	REG = "\{\{(?:(?:\w*|\s*)|(?:\d*|[$&+,\:\;\=\?@#\|'<>.^*\(\)%!-\/]))+\}\}"
	def concat (self, *args):
		return " ".join(args)
	def tag (self):
		return "{{" + self.object + "}}"
	### prints a multiple line string with formatting
	def line (self, width = 60):
		print '\n'.join(line.strip() for line in re.findall(r'.{1,'+ str(width) +'}(?:\s+|$)', self.__prcs__()) )
	### prints a single line formatted string
	def wrap (self):
		print self.__prcs__()
	### return entire formatted string using supplied styling
	def get (self, object = {}):
		### fetch returned processed object
		return self.__prcs__(object)
	### return substring/string with styling attached
	def __frmt__ (self, string, attributes):
		### iterate through attribute dict and try to match value to formatting
		for attribute in attributes:
			attr = getattr(self, str.upper(attributes[attribute]), None)
			if attr:
				string = attr + string + self.END
		### return formatted string
		return string
	### return string with {{}} removed and styling attached
	def __sbst__ (self, string, attributes = {}):
		### match {{str}} substring
		matches = re.findall(self.REG, string, re.DOTALL)
		### iterate through substrings
		for i in range(0, len(matches)):
			### replace "{{"" or "}}" from substrings
			substring = re.sub("{{|}}", "", matches[i])
			### replace matches[i] with dict
			matches[i] = {'original': substring, 'formatted': self.__frmt__(substring, attributes)}
		### iterate through matches again
		for i in range(0, len(matches)):
			### replace string with formatted text based on items in matches
			string = re.sub(matches[i]['original'], matches[i]['formatted'], string)
		### return string with formatting replacing any "{{" or "}}" that exists in original string
		return re.sub("{{|}}", "", string)
	### return formatted string or strings depending on config object supplied (list or dict)
	def __prcs__ (self, object = {}):
		### check if object isn't a default
		if not bool(object):
			### check if Class was give a constructor dict
			if self.object:
				### use constructor dict
				object = self.object
			else:
				### use a sample instead
				object = [{'str':'{{Sample}}', 'attr':{'color':'cyan'}}, {'str':'{{Text}}', 'attr':{'color':'purple'}}]
		### check if object is either a list or dict
		if type(object) is list:
			### temp list for holding formatted strings
			strs = []
			### iterate through items to be formatted
			for i in range(0, len(object)):
				### append formatted strings to temp list
				strs.append(self.__sbst__(object[i]['str'], object[i]['attr']))
			### return the complete string with formatting
			return " ".join(strs)
		else:
			### return the complete string with formatting
			return self.__sbst__(object['str'], object['attr'])
	### return the type of the object
	def __type__ (self):
		return type(self.object)
	### return the object supplied
	def __self__ (self):
		return self.object
	### constructor 
	### @object: 
		### [{'str':"{{string}}", 'attr':{'color':'red','style':'underline','weight':'bold'}}] 
		### or
		### {'str':'{{str}}', 'attr':{'color':'red'}}
	def __init__ (self, object = {}):
		self.object = object


### creates a responder class used to prompt people contextually
class Responder (String):
	### returns a string (optionally filtered) prefixed by the name of the responder
	def response (self, message = "destory all humans!", attr = {}):
		return (self.__name__() + self.seperator) + (" " + self.__msg__(message, attr))
	### private class for fetching the formatted string for the message part of ai response
	def __msg__ (self, message = "destroy all humans!", attr = {}):
		return self.get({'str': message, 'attr': attr})
	### private class for fetching and formatting the string that defines the ai's name
	def __name__ (self):
		return self.get({'str': '{{'+ self.name +'}}', 'attr': self.style})
	### constructor
	def __init__ (self, **kwargs):
		self.name = kwargs.pop('name', 'system')
		self.style = kwargs.pop('style', {'style':'underline','weight':'bold'})
		self.seperator = kwargs.pop('seperator', ':')	


### class wrapper for flexible selenium initialisations
class Browser:
	### exits defined selenium browser
	def exit (self):
		self.driver.exit()
	### quits the selenium browser session closing all windows
	def quit (self):
		self.driver.quit()
	### opens the defined self.url in the selenium browser
	def get (self, url = "https://www.google.com/"):
		if not self.url:
			self.url = url
		self.driver.get(self.url)
	### returns the object created from selenium
	def __self__ (self):
		return self.driver
	### constructor
	def __init__ (self, engine = "Chrome"):
		from selenium import webdriver
		self.driver = getattr(webdriver, engine, "Chrome")()
		self.url = ""


### class for recursive user prompts
class Request:
	### method for asking the user to input one of two provided options
	def open (self):
		### prompt user for input returning text submitted or NoneType if empty
		self.response = self.__prpt__()
		### return true if user input matches the supplied confirm string
		if self.response == self.confirm:
			return True
		### return false if the user input matches the supplied reject string
		elif self.response == self.reject:
			return False
		### prompt user that the supplied input wasn't considered valid
		else:
			print self.__resp__(String().concat("command", String({'str':String(str(self.response)).tag(),'attr':{'weight':'bold'}}).get(), "unrecognised"))
	
			### recall the function
			return self.open()
	### format the strings defining the options available for the user
	def __optn__ (self):
		return String({'str': String((self.confirm + "/" + self.reject)).tag(), 'attr':{'weight':'bold'}}).get()
	### prompt the user to input one of the supplied action contexts
	def __prpt__ (self):
		### request the user to input their text
		response = raw_input(self.__resp__((String().concat(self.prompt, self.__optn__()) + ": "))) or None
		### attempt to format the text to a uppercase string for easier comparison
		try:
			### return the uppercase string
			return str.upper(response)
		except:
			### return NoneType if unsuccessful
			return response
	### format a Responder response
	def __resp__ (self, string):
		return self.system.response(string)
	### constructor
	def __init__ (self, **kwargs):
		self.prompt = kwargs.pop("prompt", "please type either")
		self.confirm = str.upper(kwargs.pop("confirm", "yes"))
		self.reject = str.upper(kwargs.pop("reject", "no"))
		self.system = Responder()

		## print Request().open()


### generic package manage class
class Package:
	### return the fetched package or False
	def get (self):
		### attempt to locate the package
		return self.__rtrn__()
	### assign the package to class as import or None
	def __rtrn__ (self):
		self.package = self.__test__()
		if self.package:
			return self.package
		else:
			return False
	### test the existence of the package
	def __test__ (self):
		if not self.exe:
			try:
				return __import__(self.name)
			except:
				return False
		else:
			if not self.cmd:
				try:
					subprocess.call([String().concat(self.name, "2>/dev/null")], shell = True)
					return True
				except:
					return False
			else:
				try:
					subprocess.call(self.cmd, shell = True)
					return True
				except:
					return False
				
	
	### constructor
	def __init__ (self, name, source = None, exe = False, cmd = False):
		self.name = name
		self.source = source
		self.exe = exe
		self.cmd = cmd
		self.system = Responder()


### general class designed to install python modules
class Install:
	### attempt to fetch all packages
	def get (self):
		### assign empty or reduced list
		packages = self.__asgn__()
		### if list is empty assume all packages were found

		if not len(packages):

			### return True for handler
			return True
		### attempt to install the missing files
		else:
			### ask user if they would like to install the files dependencies
			print self.__resp__(String().concat(String({'str': String(str(len(packages)) + "/" + str(len(self.packages))).tag(), 'attr':{'color':'red','weight':'bold'}}).get(), "packages are missing"))
			### if user agrees attempt to install each package
			if Request(prompt = "attempt to install missing files?").open():
				for i in range(0, len(packages)):
					### install status will attempt to be changed from False to True during instal process
					self.__istl__(packages[i])

				### check the outcome of the install attempts
				for i in range(0, len(packages)):
					### if file package not installed, print solution
					if not packages[i]['installed']:
						### print the name of the package that wasn't able to be installed
						print self.__resp__(String().concat("package", String({'str': String(packages[i]['name']).tag(), 'attr':{'weight':'bold'}}).get(), "could not be installed"))
						### print the appropriate solution
						print self.__resp__("please download the package and install before running the program again")
						### if source is available print the URL
						if packages[i]['source']:
							print self.__resp__(String().concat("package available at", String({'str': String(packages[i]['source']).tag(), 'attr':{'style':'underline'}}).get()))
						### return false; break loop; this will terminate all checking instances
						### written with the assumption that you would not want your file to proceed running without all
						return False
				### return true if all files were installed
				return True
			### return false if user chose not to install packages
			return False

	### attempt to install the package through the supplied installer
	def __istl__ (self, package):
		### notify user that the package is attempting to be installed
		print self.__resp__(String().concat("trying to install", String({'str': String(package['name']).tag(), 'attr':{'weight':'bold'}}).get()))
		### try and call the supplied package installer
		if hasattr(package['installer'], '__call__'):

			### this is the response that comes back from the file installer!!!
			install_success = package['installer']()

			### if successfully installed set installed status from False to True
			if install_success:
				package['installed'] = True

			### send the entire package back with new data
			return package
		### notify user that a package installer wasn't provided for this package
		else:
			print self.__resp__(String().concat(String({'str': String(package['name']).tag(), 'attr':{'weight':'bold'}}).get(), "has no installer!"))
	### attempt to load the class package through Package.get() 		
	def __atmp__ (self, package):
		### return result
		return package.get()
	### reduce array if missing packages are found
	def __asgn__ (self):
		### iterate through self.supplied list
		for i in range(0, len(self.packages)):
			### attempt to import package through class method of get from "Package"
			self.packages[i]['installed'] = True if self.__atmp__(self.packages[i]['package']) else False
		### return reduced array
		return [pckg for pckg in self.packages if not self.packages[i]['installed']]
		
	### substitute array item to be a dict with a class instance
	def __pckg__ (self, packages):
		for i in range(0, len(packages)):

			if 'exe' not in packages[i]:
				packages[i].update({'exe': False})

			if 'cmd' not in packages[i]:
				packages[i].update({'cmd': False})

			packages[i]['package'] = Package(
				name = packages[i]['name'], 
				source = packages[i]['source'], 
				exe = packages[i]['exe'],
				cmd = packages[i]['cmd'])

		return packages
	### format a Responder response
	def __resp__ (self, string):
		return self.system.response(string)
	### constructor
	def __init__ (self, packages = []):
		self.packages = self.__pckg__(packages)
		self.system = Responder()


### creates either a temporary or permanently write file
class File:
	def append (self, string):
		self.file.seek(0, 2)
		self.file.write("\n")
		self.file.write(string)
		self.file.seek(0)
	### removes file instance from os directory
	def remove (self):
		os.remove(self.file.name)
	### returns the file entity
	def get (self):
		return self.file
	### returns the contents of a file if file
	def read (self, seeker = 0):
		self.file.seek(seeker)
		return self.file.read()
	### writes to file, optional seeker position
	def write (self, contents = 'print "Hello"', seeker = 0):
		if re.compile('[rwa]\+?', re.IGNORECASE).match(self.file.mode):
			self.file.seek(seeker)
			self.file.write(contents)
		else:
			print "file mode doesn't allow writing"
	def seek (self):
		self.file.seek(0)
	### creates file as a temporary file
	def __mktf__ (self):
		return tempfile.NamedTemporaryFile(suffix = self.ext, mode = self.mode, dir = self.filepath, delete = c)
	### creates file as a saved file
	def __mkfl__ (self):
		### update to allow file creation
		self.mode = "w+"
		return open(os.path.join(self.filepath, (self.name + self.ext)), self.mode)
	### select between temp or permanent file
	def __crte__ (self):
		file = None
		if self.temporary:
			file = self.__mktf__()
		else:
			file = self.__mkfl__()
		os.chmod(file.name, 0777)
		return file
	### add period to denote file extension if missing
	def __fext__ (self, ext):
		if re.compile('^\.\w+').match(ext):
			return ext
		else:
			return "." + ext
	### constructor
	def __init__ (self, name = "temporary", ext = "txt", temporary = True, mode = "r+", filepath = __filepath__):
		self.name = name
		self.ext = self.__fext__(ext)
		self.mode = mode
		self.filepath = filepath
		self.temporary = temporary
		self.file = self.__crte__()






### installer for pip.py package
def pip_install ():
	### read the contents of the pip downloads page
	def http_extract (http_page):
		### extract content
		contents = http_page.read()
		### if file contents found
		if contents:
			### read and return
			return __file__(contents)
		else:
			return None
	### attempt to connect to the url of python package page
	def http_connection ():
		try:
			return http_extract(urllib2.urlopen(urllib2.Request(url = "https://bootstrap.pypa.io/get-pip.py")))
		except:
			return None
	### attempt check if installed or download
	def __exec__ (temp):
		### attempt to call pip -V
		try:
			subprocess.check_call(["pip -V"], shell = True)
			return True
		except:
			try:
				### attempt to install as admin
				subprocess.call([String().concat("sudo", "python", temp.file.name)], shell=True)
				return True
			except:	
				return False
				
	### create temporary file
	def __file__ (content):
		temp = File(name = "get-pip", ext = "py", temporary = False)
	
		#regexp = re.compile(r'^DATA = b"""\n(.|\n)+"""', re.MULTILINE)
		#match = re.search(regexp, content)
		#string = "".join(match.group(0).split())
		#datastring = "".join(match.group(0).split())
		#print base64fix
		#content = re.sub(regexp, string, content)
		#print content

		### write file contents to tempfile
		temp.write(content)
		### close the file so it can be executed (this was the bain of my existence.)
		temp.file.close()

		### if file was successfully test or installed
		### remove file and exit installer
		if __exec__(temp):
			temp.remove()
			return True
		else:
			return None
	### attempt install
	def __main__ ():
		return http_connection()
	### return result
	return __main__()

### installer for Homebrew package manager
def brew_install ():
	### attempt check if installed or download
	def __exec__ ():
		try:
			subprocess.call(["brew -v"], shell = True)
			return True
		except:
			try:
				subprocess.call(['/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"'], shell = True)
				return True
			except:
				return False
	### attempt install
	def __main__ ():
		return __exec__()
	### return result
	return __main__()


def pip_package_install (package):
	import pip
	pip.main(['install', package])
	if __import__ (package):
		return True
	else:
		return False

def brew_package_install (package):
	try:
		subprocess.call([String().concat("brew", "ls", "--versions", package)], shell = True)
		return True
	except:
		try:
			subprocess.call([String().concat("brew", "install", package, "2>/dev/null")], shell = True)
			return True
		except:
			return False

def selenium_install ():
	return pip_package_install("selenium")

def chromedriver_install ():
	return brew_package_install("chromedriver")
 




def main (resp = Responder()):
	main_packages = [
	{'name':'pip','source':'https://bootstrap.pypa.io/get-pip.py', 'installer':pip_install},
	{'name':'brew', 'source':'http://brew.sh/', 'exe': True, 'installer':brew_install},
	{'name':'selenium','source':'https://pypi.python.org/pypi/selenium', 'installer':selenium_install},
	{'name':'chromedriver','source':'https://sites.google.com/a/chromium.org/chromedriver/', 'exe': True, 'cmd':'brew ls --versions chromedriver &> /dev/null', 'installer':chromedriver_install}]

	def __core__ (main_required):
		print resp.response("i'm checking installed files")

		for i in range(0, len(main_required)):
			main_required[i]['installed'] = Install([main_required[i]]).get()
			if not main_required[i]['installed']:
				return False
		return True

	def __hglg__ (browser):
		try:
			browser.driver.execute_script('document.querySelector("'+ browser.cssSelector +'").parentElement.style.boxShadow = "0px 0px 100px aquamarine";')
		except:
			pass
		#print browser.cssSelectorElement
		#try:
			#browser.driver.execute_script()

			#''

			#document.querySelector("#pt-cv-page-1").parentElement.style.boxShadow = "0px 0px 100px aquamarine";"0px 0px 100px aquamarine"

	def __sfrc__ (browser, attempted = False):
		raw_input('ell')

	def __slel__ (browser, attempted = False):
		if not attempted:
			print resp.response("i think that url's okay. what element should i try and find on the page?")
		
		browser.cssSelector = raw_input("please type a valid CSS: ") or None

		try:
			browser.cssSelectorElement = browser.driver.find_elements_by_css_selector(browser.cssSelector)
			__hglg__(browser)
			__sfrc__(browser)
		except:
			print resp.response("sorry! i couldn't find that for you..")
			if Request(prompt = "try again?").open():
				__slel__(browser, attempted = True)
			else:
				return False



	def __brws__ (browser, attempted = False):
		if not attempted:
			print resp.response("i'm going to open my own web-browser. what page should i go to?")
		browser.url = raw_input("please type a correct url: ") or None
		try: 
			browser.get()
			__slel__(browser)
		except:
			print resp.response("uh oh. there's something wrong with that url. try again?")
			if Request(prompt = "try again?").open():
				__brws__(browser, attempted = True)
			else:
				return False

	def __impt__ ():
		from selenium import webdriver
		__brws__(Browser(engine = "Chrome"))
	
	def __main__ ():
		if __core__(main_packages):
			print resp.response("looks like everything's here. nice!")
			__impt__()
		else:
			print resp.response("uh oh. i'm missing files. please install them before running again!")
			return False


	return __main__()

	
if __name__ == "__main__":
	main(resp = Responder(name = "dee"))

