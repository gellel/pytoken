### python scripts dependencies
### py selenium browser package
### from selenium import webdriver
#http://selenium-python.readthedocs.io/api.html

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
### py urllib class pacakge
import urllib
### py random class package
import random
### py system class package
import sys
### py os class package
import os
### py regex
import re

###
dee_strs = {
	'attempt':  	["let's give it a shot","computing it", "scanning it like a robot","attempting it","here i go","let me try that out","triangulating"],
	'greeting': 	["hi","hello","hi-there","what-up","what's up","hayy","hey-ya","hey-youu"],
	'frustrated': 	["hey", "dude","c'mon","man","really","for-realll"],
	'pause': 		["hmm","mmm","hmph","uhh","uhh-huhh","thinking"],
	'problem': 		["uhh-oh","eek","whoops","not good","sorry","err","mmmm","damn"],
	'start': 		["ok","alright","okokok","ready", "cool", "neat","let's go","inizio","all-set"],
	'error':		["i can't do that","that is not ok","we have to try that again","not sure what happened"],
	'absent':		["wasn't able to","couldn't","was unable to","didn't","tried but was unable to"],
	'what':			["what is", "what's", "so--what's"],
	'puzzled':		["uhh","errr","umm","so--uhh"],
	'require':		["need","require","--need--","--require--"],
	'request':		["would you please","please","can you please","could you","would you","you need to","you gotta","can you"],
	'confirm':		["you got it","sure thing","alright","done","consider it done","--tada--","whatever you say","sorted"],
	'try':			["will attempt to","am going to try to","will try to","am going to try to","will attempt to try to"],
	'store':		["save","store","package","place","send"],
	'check':		["is that ok?","is that fine?","that's ok, right?","it's not a problem --right?"],
	'semote':		["**exhale**","**sigh**", ""],
	'located':		["nailed it","aced it","found it","gotcha","bam--found it","yewww. got it","i found it","looks like it's there","right where it was supposed to be","too easy. got it","stay ez; i found it"]
}

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
	def wrap (self, width = 60):
		print '\n'.join(line.strip() for line in re.findall(r'.{1,'+ str(width) +'}(?:\s+|$)', self.__process__()) )
	### prints a single line formatted string
	def line (self):
		print self.__process__()
	### return entire formatted string using supplied styling
	def get (self, object = {}):
		### fetch returned processed object
		return self.__process__(object)
	### return substring/string with styling attached
	def __format__ (self, string, attributes):
		### iterate through attribute dict and try to match value to formatting
		for attribute in attributes:
			attr = getattr(self, str.upper(attributes[attribute]), None)
			if attr:
				string = attr + string + self.END
		### return formatted string
		return string
	### return string with {{}} removed and styling attached
	def __substitute__ (self, string, attributes = {}):
		### match {{str}} substring
		matches = re.findall(self.REG, string, re.DOTALL)
		### iterate through substrings
		for i in range(0, len(matches)):
			### replace "{{"" or "}}" from substrings
			substring = re.sub("{{|}}", "", matches[i])
			### replace matches[i] with dict
			matches[i] = {'original': substring, 'formatted': self.__format__(substring, attributes)}
		### iterate through matches again
		for i in range(0, len(matches)):
			### replace string with formatted text based on items in matches
			string = re.sub(matches[i]['original'], matches[i]['formatted'], string)
		### return string with formatting replacing any "{{" or "}}" that exists in original string
		return re.sub("{{|}}", "", string)
	### return formatted string or strings depending on config object supplied (list or dict)
	def __process__ (self, object = {}):
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
				strs.append(self.__substitute__(object[i]['str'], object[i]['attr']))
			### return the complete string with formatting
			return " ".join(strs)
		else:
			### return the complete string with formatting
			return self.__substitute__(object['str'], object['attr'])
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
		return (self.__name__() + self.seperator) + (" " + self.__message__(message, attr))
	### private class for fetching the formatted string for the message part of ai response
	def __message__ (self, message = "destroy all humans!", attr = {}):
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
		### import the webdriver package if absent
		from selenium import webdriver
		### create a webdriver instance
		self.driver = getattr(webdriver, engine, "Chrome")()
		self.url = ""


### class for recursive user prompts
class Request:
	### method for asking the user to input one of two provided options
	def open (self):
		### prompt user for input returning text submitted or NoneType if empty
		self.response = self.__prompt__()
		### return true if user input matches the supplied confirm string
		if self.response == self.confirm:
			return True
		### return false if the user input matches the supplied reject string
		elif self.response == self.reject:
			return False
		### prompt user that the supplied input wasn't considered valid
		else:
			print self.__response__(String().concat("command", String({'str':String(str(self.response)).tag(),'attr':{'weight':'bold'}}).get(), "unrecognised"))
			### recall the function
			return self.open()
	### format the strings defining the options available for the user
	def __option__ (self):
		return String({'str': String((self.confirm + "/" + self.reject)).tag(), 'attr':{'weight':'bold'}}).get()
	### prompt the user to input one of the supplied action contexts
	def __prompt__ (self):
		### request the user to input their text
		response = raw_input(self.__response__((String().concat(self.prompt, self.__option__()) + ": "))) or None
		### attempt to format the text to a uppercase string for easier comparison
		try:
			### return the uppercase string
			return str.upper(response)
		except:
			### return NoneType if unsuccessful
			return response
	### format a Responder response
	def __response__ (self, string):
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
		return self.__find__()
	### assign the package to class as import or None
	def __find__ (self):
		self.package = self.__test__()
		if self.package:
			return self.package
		else:
			return False
	### test the existence of the package
	def __test__ (self):
		### check if class is to be run as a import or executable script
		if not self.exe:
			### try import the required package
			try:
				__import__(self.name)
				### return True if asset can be imported
				return True
			except:
				### return False if unable to manage import
				return False
		### operate as a command subprocess
		else:
			### set a temp variable for simplier subprocess caller
			cmd = self.name
			### check if user wishes to put in a more complex command
			if self.cmd:
				### set the class command as the temp variable
				cmd = self.cmd
			### attempt to run the subprocess
			return Command(command = cmd).process()
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
		packages = self.__assign__()
		### if list is empty assume all packages were found
		missing = [package for package in self.packages if not package['installed']]
		### check if list missing is not an empty list 
		if not len(missing):
			### return True for handler
			return True
		### attempt to install the missing files
		else:
			### ask user if they would like to install the files dependencies
			print self.__response__(String().concat(String({'str': String(str(len(missing)) + "/" + str(len(self.packages))).tag(), 'attr':{'color':'red','weight':'bold'}}).get(), "packages are missing"))
			### if user agrees attempt to install each package
			if Request(prompt = "attempt to install missing files?").open():
				for i in range(0, len(packages)):
					### install status will attempt to be changed from False to True during instal process
					self.__install__(packages[i])
				### check the outcome of the install attempts
				for i in range(0, len(packages)):
					### if file package not installed, print solution
					if not packages[i]['installed']:
						### print the name of the package that wasn't able to be installed
						print self.__response__(String().concat("package", String({'str': String(packages[i]['name']).tag(), 'attr':{'weight':'bold'}}).get(), "could not be installed"))
						### print the appropriate solution
						print self.__response__("please download the package and install before running the program again")
						### if source is available print the URL
						if packages[i]['source']:
							print self.__response__(String().concat("package available at", String({'str': String(packages[i]['source']).tag(), 'attr':{'style':'underline'}}).get()))
						### return false; break loop; this will terminate all checking instances
						### written with the assumption that you would not want your file to proceed running without all
						return False
				### return true if all files were installed
				return True
			### return false if user chose not to install packages
			return False
	### attempt to install the package through the supplied installer
	def __install__ (self, package):
		### notify user that the package is attempting to be installed
		print self.__response__(String().concat("trying to install", String({'str': String(package['name']).tag(), 'attr':{'weight':'bold'}}).get()))
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
			print self.__response__(String().concat(String({'str': String(package['name']).tag(), 'attr':{'weight':'bold'}}).get(), "has no installer!"))
	### attempt to load the class package through Package.get() 		
	def __attempt__ (self, package):
		### return result
		return package.get()
	### reduce array if missing packages are found
	def __assign__ (self):
		### iterate through self.supplied list
		for i in range(0, len(self.packages)):
			### attempt to import package through class method of get from "Package"
			self.packages[i]['installed'] = True if self.__attempt__(self.packages[i]['package']) else False
			### if package is determined to be installed print formatted package name
			if self.packages[i]['installed']:
				print self.__response__(String().concat(String({'str': String(self.packages[i]['name']).tag(), 'attr':{'weight':'bold'}}).get(), "is", String({'str':'{{installed}}','attr':{'color':'green','weight':'bold'}}).get()))
		### return reduced array
		return self.packages
	### substitute array item to be a dict with a class instance
	def __package__ (self, packages):
		for i in range(0, len(packages)):
			### add to dict if dict is absent of attribute 'exe'
			if 'exe' not in packages[i]:
				packages[i].update({'exe': False})
			### add to dict if dict is absent of attribute 'cmd'
			if 'cmd' not in packages[i]:
				packages[i].update({'cmd': False})
			### call "Package" class and initialise a dict key value with class instance
			packages[i]['package'] = Package(
				name = packages[i]['name'], 
				source = packages[i]['source'], 
				exe = packages[i]['exe'],
				cmd = packages[i]['cmd'])
		### return reformatted dict
		return packages
	### format a Responder response
	def __response__ (self, string):
		return self.system.response(string)
	### constructor
	def __init__ (self, packages = []):
		self.packages = self.__package__(packages)
		self.system = Responder()


### creates either a temporary or permanently write file
class File:
	### add new string to the end of the file
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
	### close the file
	def close (self):
		self.file.close()
	### sets seeker on the file
	def seek (self):
		self.file.seek(0)
	### creates file as a temporary file
	def __tempfile__ (self):
		return tempfile.NamedTemporaryFile(suffix = self.ext, mode = self.mode, dir = self.filepath, delete = c)
	### creates file as a saved file
	def __permfile__ (self):
		### update to allow file creation
		self.mode = "w+"
		return open(os.path.join(self.filepath, (self.name + self.ext)), self.mode)
	### select between temp or permanent file
	def __create__ (self):
		file = None
		if self.temporary:
			file = self.__tempfile__()
		else:
			file = self.__permfile__()
		os.chmod(file.name, 0777)
		return file
	### add period to denote file extension if missing
	def __fileext__ (self, ext):
		if re.compile('^\.\w+').match(ext):
			return ext
		else:
			return "." + ext
	### constructor
	def __init__ (self, name = "temporary", ext = "txt", temporary = True, mode = "r+", filepath = __filepath__):
		self.name = name
		self.ext = self.__fileext__(ext)
		self.mode = mode
		self.filepath = filepath
		self.temporary = temporary
		self.file = self.__create__()


### fetches a web resource
class HTTPResource:
	### request the resource
	def fetch (self):
		return self.__open__()
	### close the connection to the resource
	def close (self):
		self.request_open.close()
	### read and return the content of the webpage
	def __content__(self):
		self.request_content = self.request_open.read()
		self.close()
		return self.request_content
	### opens the supplied webpage with formatted headers through urllib2 
	def __open__ (self):
		### attempt to fetch the URL resource
		try:
			### set the request_open object to the connection point
			self.request_open = urllib2.urlopen(self.request_object)
		except:
			self.request_open = None
		### if request was successful read the content of the page
		if self.request_open:
			### return the read content
			return self.__content__()
		### return None if connection failed
		else:
			return None
	### construct the http request object for fetching the webpage
	def __format__ (self):
		### confirm that the constructor has a URL
		if self.request_url:
			### check if the http headers dict is not empty
			if bool(self.request_headers):
				### if dict has at least one key pair value accept as http headers
				return urllib2.Request(self.request_url, urllib.urlencode(self.request_headers))
			else:
				### use standard http request object
				return urllib2.Request(self.request_url)
		else:
			return None
	### constructor
	def __init__ (self, URL = None, headers = {}):
		self.request_url = URL
		self.request_headers = headers
		self.request_object = self.__format__()

### operates a subprocess for checking terminal commands
class Command:
	### return the result of the attempted command
	def process (self):
		return self.__exec__()
	### attempt to call function; uses either subprocess.call or subprocess.check_call
	def __exec__ (self):
		try:
			### return True if function ran
			self.function(self.command, stdout = self.stdout, stderr = self.stderr, shell = self.shell)
			return True
		### handle the subprocessor command error if command was found but not executabe
		except subprocess.CalledProcessError:
			return False
		### handle the subprocessor command error if command not found
		except OSError:
			return False
	### return the appropriate subprocess
	def __funct__ (self):
		return subprocess.call if self.shell else subprocess.check_call
	### constructor
	def __init__ (self, command = "", stdout = open(os.devnull, 'w'), stderr = subprocess.STDOUT, shell = False):
		self.command = command
		self.shell = shell
		self.stdout = stdout
		self.stderr = stderr
		self.function = self.__funct__()




class Partner:

	def __printHTML__ (self):
		print self.HTMLElement

	def __child__ (self):
		self.__dee__(String().concat((dee_strs['start'][random.randrange(len(dee_strs['start']))] + "."), "should be able to get the first-child element of", String({'str':String(self.CSSSelector).tag(),'attr':{'weight':'bold'}}).get()))
		self.__dee__(String().concat("should i attempt to locate that for you?"))

		if not Request().open():
			self.__dee__(String().concat((dee_strs['start'][random.randrange(len(dee_strs['start']))] + "."), "type out the CSS selector you want to use."))
			self.__attr__("HTML Element/CSS selector", "Element/CSS", "CSSChild")
		else:
			self.CSSChild = "> *:first-child"

		if hasattr(self, "CSSChild"):
		
			self.HTMLElement = self.browser.driver.execute_script('return document.querySelector("'+ String().concat(self.CSSSelector, self.CSSChild) +'");')

			if not self.HTMLElement:
				self.__dee__(String().concat((dee_strs['puzzled'][random.randrange(len(dee_strs['puzzled']))] + ".."), "i", dee_strs['absent'][random.randrange(len(dee_strs['absent']))], "find any CSS selector on the page that matched your pattern."))
				self.__dee__(String().concat("would you like to try again?"))
				if Request().open():
					return self.__child__()
				else:
					self.__dee__(String().concat((dee_strs['problem'][random.randrange(len(dee_strs['problem']))] + "."), "i", dee_strs['absent'][random.randrange(len(dee_strs['absent']))], "that. so i can't go any further without it."))
					return False
			else:
				self.__dee__(String(dee_strs['located'][random.randrange(len(dee_strs['located']))] + "!").tag(), {'color':'green','weight':'bold'})
				return True
		else:
			self.__dee__("hey! i need to use something man!")
			return False
		


	### attempt to locate the closets possible CSS element to the HTML target
	def __target__ (self):
		### prompt users to input a valid CSS selector
		self.__dee__(String().concat((dee_strs['start'][random.randrange(len(dee_strs['start']))] + "."), "what CSS selector should i use?"))
		### request user to supply CSS selector for the selenium browser
		### fetch data through the generic response handler
		if self.__attr__("CSS selectors", "CSS selector", "CSSSelector"):
			### notify user that 'dee' will try and locate the specified selector
			self.__dee__(String().concat(dee_strs['attempt'][random.randrange(len(dee_strs['attempt']))] + "."))
			### assign attempted match the the self object
			self.CSSPathElement = self.browser.driver.execute_script('return document.querySelector("'+ self.CSSSelector +'");')
			### test if selenium found the requested element on the page
			if not self.CSSPathElement:
				### notify user that the browser was unable to locate the element on the page
				self.__dee__(String().concat((dee_strs['puzzled'][random.randrange(len(dee_strs['puzzled']))] + ".."), "i", dee_strs['absent'][random.randrange(len(dee_strs['absent']))], "find any CSS selector on the page that matched your pattern."))
				self.__dee__("wanna try again?")
				### prompt user to resupply their CSS selector
				if Request().open():
					### recall function
					return self.__target__()
				else:
					return False
			### notify user that the element was found on the page
			else:
				### write success message
				self.__dee__(String(dee_strs['located'][random.randrange(len(dee_strs['located']))] + "!").tag(), {'color':'green','weight':'bold'})
				return True
		### notify user that CSS selector is required 
		else:	
			### print error message to the user
			self.__dee__(String().concat((dee_strs['frustrated'][random.randrange(len(dee_strs['frustrated']))] + "."), (dee_strs['puzzled'][random.randrange(len(dee_strs['puzzled']))] + "."), "i can't target an empty element like that!"))
			return False
	### fetch the webpage with the selenium webdriver
	def __fetch__(self):
		### use the user generated URL
		self.browser.get(self.URL)
		### test if the server returned 404; will only work if the DOMAIN does not exist, not a subpath on a page
		self.found = self.browser.driver.execute_script('return (function () { return new RegExp("server DNS address could not be found.", "gmi").test(document.body.innerText); }())')
		### if (as Chrome) the page returned the DNS error message, prompt the user to re-enter their provided URL
		if self.found:
			### print output to user
			self.__dee__(String().concat((dee_strs['problem'][random.randrange(len(dee_strs['problem']))] + "."), "something's {{wrong}} that webpage.."))
			self.__dee__("should we try another url?")
			### prompt user to retry the web request
			if Request().open():
				### close the selenium instance to prevent conflicts
				self.browser.quit()
				### recall process url
				self.__purl__()
				### reinitalise selenium browser
				self.__browser__()
				### recall function
				return self.__fetch__()
			else:
				return False
		else:
			return True
	### attempt to create a selenium webdriver
	def __browser__ (self, attempted = False):
		### avoid priting out double status messages if required
		if not attempted:
			### print the action required by dee
			### notify user that the terminal might 'hang' if the request webpage takes awhile to load
			self.__dee__(String().concat((dee_strs['start'][random.randrange(len(dee_strs['start']))] + "."), "i'm gonna try open", String({'str':String(self.URL).tag(),'attr':{'color':'darkcyan','weight':'bold'}}).get()))
			self.__sys__(String().concat("** this terminal will wait for", self.deee.__name__(), "to finish loading the page", self.URL))
			self.__sys__("** if this takes too long. try stop the browser from loading and the terminal should resume **")
		### attempt to initialise selenium webdriver
		try:
			### set the engine to be Google Chrome (FireFox not currently stable)
			self.browser = Browser(engine = "Chrome")
		except:
			self.browser = None
		### handler error as system if the webdriver package did not initalise
		if not self.browser:
			self.__sys__("there was an error creating the required item {{web-browser}}", {'color':'red','weight':'bold'})
			return False
		else:
			return True
	### request the url to access with selenium
	def __purl__ (self):
		### request the user to input a valid url
		self.__dee__(String().concat((dee_strs['start'][random.randrange(len(dee_strs['start']))] + "."), dee_strs['what'][random.randrange(len(dee_strs['what']))], "the URL for", String({'str':String(self.name).tag() + "?", 'attr':{'weight':'bold'}}).get()))
		### request user to supply the URL for the selenium browser
		### fetch data through the generic response handler
		if self.__attr__(String().concat(self.name + "'s",  "website URL"), "URL", "URL"):
			return True
		else:
			### print the issue to the user
			self.__dee__(String().concat("i", dee_strs['require'][random.randrange(len(dee_strs['require']))], "a page URL to do any of this!"))
			self.__dee__(String().concat(dee_strs['request'][random.randrange(len(dee_strs['request']))], "try again, but next time remember to input a website URL"))
			return False
	### request the directory to save files
	def __dirs__ (self):
		### non corrupted file path (does not include string colour)
		path = str(self.dirs) + "/" + str(self.name)
		### edited file path (contains string colour)
		path_string = String({'str':String(str(self.dirs) + "/").tag(),'attr':{'weight':'bold'}}).get() + String({'str':String(str(self.name)).tag(), 'attr':{'color':'darkcyan','weight':'bold'}}).get()
		### request user to confirm whether the program can save the created files in the directory the script is being run from
		self.__dee__(String().concat((dee_strs['start'][random.randrange(len(dee_strs['start']))] + "."), "i", dee_strs['try'][random.randrange(len(dee_strs['try']))], dee_strs['store'][random.randrange(len(dee_strs['store']))], "files here:", path_string))
		self.__dee__(String().concat(dee_strs['check'][random.randrange(len(dee_strs['check']))], "if not just tell me and i'll move it somewhere else."))
		### if the user does not allow the program to save in the selected directory, prompt for a change request
		if not Request().open():
			self.__dee__(String().concat((dee_strs['start'][random.randrange(len(dee_strs['start']))] + "."), dee_strs['what'][random.randrange(len(dee_strs['what']))], "the correct file path?"))
			### request user to supply the folder path for the generated files
			### fetch data through the generic response handler
			if self.__attr__("New full folder path", "Folder path", "dirs"):
				return True
			else:
				### print the issue to the user
				self.__dee__(String().concat((dee_strs['frustrated'][random.randrange(len(dee_strs['frustrated']))] + "!"), dee_strs['require'][random.randrange(len(dee_strs['require']))], "a place to", dee_strs['store'][random.randrange(len(dee_strs['store']))], "things.", dee_strs['semote'][random.randrange(len(dee_strs['semote']))]))
				return False
		else:
			### replace the defined path with the new user input
			self.dirs = path
			return True
	### request the name of the partner page
	def __name__ (self):
		### print request to user
		self.__dee__(String().concat((dee_strs['start'][random.randrange(len(dee_strs['start']))] + "."), dee_strs['what'][random.randrange(len(dee_strs['what']))], "the name of the {{Gemini Partner}} we're setting up?"), {'weight':'bold'})
		### request user to supply the name of the partner
		### fetch data through the generic response handler
		if self.__attr__("Gemini partners name", "Partners name", "name"):
			### print the formulated partner
			self.__dee__(String().concat("it's called", String({'str':String(self.name).tag(),'attr':{'color':'darkcyan','weight':'bold'}}).get() + ".", dee_strs['confirm'][random.randrange(len(dee_strs['puzzled']))] + "."))
			return True
		else:
			### print the issue to the user	
			self.__dee__(String().concat((dee_strs['puzzled'][random.randrange(len(dee_strs['puzzled']))] + "."), "i", dee_strs['require'][random.randrange(len(dee_strs['require']))], "a name to start the process."))
			self.__dee__(String().concat(dee_strs['request'][random.randrange(len(dee_strs['request']))], "try again, but with a name this time!"))
			return False
	### assign attribute of class through input method
	def __attr__ (self, input_message, confirm_message, attr):
		### attempt to set the attribute of the class
		def __setattribute__ ():
			### prompt user to input a string based on supplied criteria
			temp = raw_input(self.__sys__(String().concat("please enter", String({'str':String(str(input_message)).tag(),'attr':{'weight':'bold'}}).get()) + ": ", printt = False)) or None
			### confirm that the input was not None Type
			if not temp:
				### inform user that input was not considered valid
				self.__sys__(String().concat(
					String({'str':String(input_message).tag(),'attr':{'weight':'bold'}}).get(), "cannot be",
					String({'str':String(str(temp)).tag(),'attr':{'weight':'bold'}}).get()))
				### prompt user to reattempt input
				if Request(prompt = "try again?").open():
					### recall function
					return __setattribute__()
				else:
					### return None of second attempt was not requested
					return None
			### if type was not None confirm the input of the user
			else:
				return __changeattribute__(temp)
		### confirm whether typed input was intended
		def __changeattribute__ (temp):
			### print the previous input (defined in __setattribute__)
			self.__sys__(String().concat("is", String({'str':String(str(temp)).tag(),'attr':{'weight':'bold'}}).get(), "the correct value for", String({'str':String(confirm_message).tag() + "?",'attr':{'weight':'bold'}}).get()))
			### if input is correct set as class attribute
			if Request().open():
				### set attribute
				setattr(self, attr, temp)
				### return self object
				return self
			### if the input entered was incorrect
			else:
				### prompt user to attempt to recall function and reset value
				if Request(prompt = "change value?").open():
					### recall primary function
					return __setattribute__()
		### return attribute
		return __setattribute__()
	### return text (used for functions) or print text to console	
	def __rop__ (self, message = "Test", printt = True):
		### if printt 
		if printt:
			### print message to console
			print message
		### return formatted message
		return message
	### print message as "system"
	def __sys__ (self, message = "", attr = {}, printt = True):
		return self.__rop__(self.system.response(message, attr), printt)
	### print message as "dee"
	def __dee__ (self, message = "", attr = {}, printt = True):
		return self.__rop__(self.deee.response(message, attr), printt)
	### primary function handler for class
	def __main__ (self):
		self.__name__()
		self.__dirs__()
		self.__purl__()
		self.__browser__()
		self.__fetch__()
		self.__target__()
		self.__child__()
		self.__printHTML__()
	### return self object
	def __self__ (self):
		return self
	### constructor
	def __init__ (self, dirs = __filepath__, deee = Responder(name = "dee"), system = Responder()):
		self.dirs = dirs
		self.deee = deee
		self.system = system


### shared function for installing pip-main from url
def install_pip ():
	### check if pip command isn't available
	if not Command(command = ["pip"]).process():
		### create a temporary file to hold the contents of the main pip python file
		temp = File(name = "get-pip", ext = "py", temporary = False)
		### fetch the contents of the package from pip distribution url
		content = HTTPResource("https://bootstrap.pypa.io/get-pip.py").fetch()
		### check if the http resource was found
		if content:
			### write to the temporary file if the contents were found
			temp.write(content)
			### close the file so it can be interpreted by a subprocessor
			temp.close()
			### check if the pip installer was successful
			if Command(command = [String().concat("sudo", "-H", "python", temp.file.name)], shell = True, stdout = None).process():
				### cleanup the created file
				temp.remove()
				return True
			else:
				### leave the downloaded file incase the user wishes to run it manually
				return False
	### return True if the user already has pip installed
	else:
		return True


### shared function for uninstalling packages for pip
def pip_uninstall (package):
	### uninstall packages as sudo
	return Command(command = [String().concat("sudo", "-H", "pip", "uninstall", "package")], shell = True, stdout = None).process()

### shared function for installing packages for pip
def pip_install (package):
	### install the package as sudo
	return Command(command = [String().concat("sudo", "-H", "pip", "install", package)], shell = True, stdout = None).process()

### shared function for installing selenium
def install_selenium ():
	return pip_install("selenium")

### shared function for installing beautifulsoup4
def install_beautifulsoup4 ():
	return pip_install("beautifulsoup4")

### shared function for installing chromedriver
def install_chromedriver ():
	return pip_install("chromedriver_installer")

### installer for all required packages for program
def dependencies (system = Responder()):
	### list of the packages and where to access them from
	main_packages = [
	{'name':'pip','source':'https://bootstrap.pypa.io/get-pip.py', 'installer':install_pip},
	{'name':'bs4','source':'https://www.crummy.com/software/BeautifulSoup/bs4/download/', 'installer':install_beautifulsoup4},
	{'name':'selenium','source':'https://pypi.python.org/pypi/selenium', 'installer':install_selenium},
	{'name':'chromedriver_installer','source':'https://sites.google.com/a/chromium.org/chromedriver/', 'installer':install_chromedriver}]
	### attempt to install the required files automatically
	def attempt_installed (packages):
		### return the result of the installation
		return Install(packages).get()
	### confirm the required packages were successfully installed on the OS
	def confirm_installed (packages):
		### notify user that the program is checking for installed dependencies
		print system.response("checking installed packages")
		### check if the installed packages were loaded
		if attempt_installed(packages):
			### notify user of successful outcome
			print system.response("{{checks passed}}. all dependencies are installed", {'color':'green','weight':'bold'}), "\n"
			return True
		else:
			### notify user that the packages failed to install
			print system.response("{{checks failed}}. there a missing packages. program will not continue", {'color':'red','weight':'bold'})
			return False
	### return universal result of the installed packages
	return confirm_installed(main_packages)

### primary script operator function
def main ():
	### continue of all dependencies for Partner script were found
	if dependencies():
		### initialse partner script
		partner = Partner().__main__()
		###
		print ""

		if partner:
			return True
		else:
			return False
	else:
		return False

### initialise the python script
if __name__ == '__main__':
	### call main function
	main()

