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


def str_random (str__object, key):
	return str__object[key][random.randrange(len(str__object[key]))]


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
	REG = "\{\{(?:[\w\s\d]*|[$&\+,\:\;\=\?@#\|'\<\>\.^\*\(\)%!-\/]*)*\}\}"
	def concat (self, *args):
		return " ".join(args)
	def tag (self):
		return "{{" + self._object + "}}"
	### prints a multiple line string with formatting
	def wrap (self, width = 60):
		print '\n'.join(line.strip() for line in re.findall(r'.{1,'+ str(width) +'}(?:\s+|$)', self.__process__()) )
	### prints a single line formatted string
	def line (self):
		print self.__process__()
	### return entire formatted string using supplied styling
	def get (self, _object = {}):
		### fetch returned processed _object
		return self.__process__(_object)
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
	### return formatted string or strings depending on config _object supplied (list or dict)
	def __process__ (self, _object = {}):
		### check if _object isn't a default
		if not bool(_object):
			### check if Class was give a constructor dict
			if self._object:
				### use constructor dict
				_object = self._object
			else:
				### use a sample instead
				_object = [{'str':'{{Sample}}', 'attr':{'color':'cyan'}}, {'str':'{{Text}}', 'attr':{'color':'purple'}}]
		### check if _object is either a list or dict
		if type(_object) is list:
			### temp list for holding formatted strings
			strs = []
			### iterate through items to be formatted
			for i in range(0, len(_object)):
				### append formatted strings to temp list
				strs.append(self.__substitute__(_object[i]['str'], _object[i]['attr']))
			### return the complete string with formatting
			return " ".join(strs)
		else:
			### return the complete string with formatting
			return self.__substitute__(_object['str'], _object['attr'])
	### return the type of the _object
	def __type__ (self):
		return type(self._object)
	### return the _object supplied
	def __self__ (self):
		return self._object
	### constructor 
	### @_object: 
		### [{'str':"{{string}}", 'attr':{'color':'red','style':'underline','weight':'bold'}}] 
		### or
		### {'str':'{{str}}', 'attr':{'color':'red'}}
	def __init__ (self, _object = {}):
		self._object = _object

### short lexical class
class LX:
	### return formatted self object
	def get (self, rtype = '__dict__'):
		return getattr(self, rtype)
	### return self as dictonary (to be integrated with class Lexicon)
	def __dict__ (self):
		return {'key':self.key, 'value':self.value, 'pause':self.pause,	'attr':self.attr, 'punctuate':self.punctuate, 'optional':self.optional}
	### format the provided object to the Lexicon readible format
	def __formatkey__ (self, _object):
		if type(_object) is dict:
			return _object
		elif type(_object) is list:
			### iterate over supplied list
			for i in range(0, len(_object)):
				### if instance is a Lexicon class get Lexicon data
				if isinstance(_object[i], Lexicon):
					_object[i] = _object[i].get()
			return {'t':_object}
		elif isinstance(_object, Lexicon):
			return {'t':[_object.get()]}
	def __formatrandom__ (self, _object):
		if type(_object) is dict:
			if not 'optional' in _object:
				_object['optional'] = 2
			if not 'punctuate' in _object:
				_object['punctuate'] = 2
		return _object
	### constructor
	def __init__ (self, **kwargs):
		self.key = self.__formatkey__(kwargs.pop('key', {'t':["test"]}))
		self.value = kwargs.pop('value', 't')
		self.pause = kwargs.pop('pause', None)
		self.attr = kwargs.pop('attr', {})
		self.punctuate = kwargs.pop('punctuate', None)
		self.optional = kwargs.pop('optional', False)

### produces concatenated string with random partial strings
class Lexicon:
	def pprint (self):
		get_str = self.get()
		### confirm if not empty returned string
		if not bool(re.search("^$", get_str)):
			### print returned string
			print get_str
	### return completely formatted string
	def get (self):
		### call packaging method to return string
		return self.__package__()
	### convert list of dict or single dict to string response
	def __package__ (self):
		### check if object type is a dictonary (assumes it is a single entity)
		if type(self._object) is dict:
			### return formatted
			return self.__construct__(self._object)
		### iterate over list item; evaluate all items but assume it will receive strings or dict
		elif type(self._object) is list:
			### temporary list to hold formatted or strings
			constructed = []
			### iterate over encapsulated objects
			for i in range(0, len(self._object)):
				### confirm type of item
				if type(self._object[i]) is dict:
					### check if the dict provided is an optional item
					if not self.__optional__(self._object[i]):
						### format string
						constructed.append(self.__construct__(self._object[i]))
				### assume other type supplied is a string
				elif not type(self._object[i]) is None:
					constructed.append(self._object[i])
			### return joined string, seperated by whitespace
			return " ".join(constructed)
	### confirm if dict item is to be evaluated
	def __optional__ (self, _object):
		if bool(_object['optional']) and type(_object['optional']) is int:
			_randvalue = random.randrange(0, _object['optional'])
			if _randvalue == 0:
				return True
			else:
				return False
		else:
			return False
	### convert dictionary to string 
	def __construct__ (self, _object):
		### retrieve unformatted string
		_object['original'] = self.__lexical__(_object['key'], _object['value'])
		### assign new string to dict item for formatting
		_object['formatted'] = _object['original']
		### return the substring from the supplied dict and key
		### apply string formatting if the dict supplied isn't empty
		if bool(_object['attr']):
			### replace formatted string with the prettified variant
			_object['formatted'] = String({'str':String(_object['formatted']).tag(),'attr':_object['attr']}).get()
		### confirm if the substring is to be punctuated with a english pause
		if _object['pause']:
			### format substring before main text
			pause_str = self.__lexical__({'t':["uh", "uhh", "um--ah", "err"]}, 't')
			### constructs for sentence
			if _object['pause'] == 'before':
				### determine if the string should include intenation lines
				if random.randrange(0, 3) == 0:
					punct_str = self.__lexical__({'t':["--", "..", "..."]}, 't')
					### include intenation
					_object['formatted'] = String().concat((pause_str + punct_str), _object['formatted'])
				else:
					_object['formatted'] = String().concat(pause_str, _object['formatted'])
			### constructs after sentence
			elif _object['pause'] == 'after':
				### determine if the string should include intenation lines
				if random.randrange(0, 3) == 0:
					punct_str = self.__lexical__({'t':["--", ",", "..", "..."]}, 't')
					### include intenation
					_object['formatted'] = String().concat(_object['formatted'], (pause_str + punct_str))
				else:
					_object['formatted'] = String().concat(_object['formatted'], pause_str)

		if len(_object['original']) == 0:
			_object['formatted'] = "".join(_object['formatted'].split())

		### confirm if the substring should be punctuated at the end of the string
		if _object['punctuate']:
			### allow dictonaries to be converted to substrings using self.__lexical__
			if type(_object['punctuate']) is dict:
				_object['punctuate'] = self.__lexical__(_object['punctuate'], 't')
			### allow lists to be converted to substrings using self.__lexical__
			elif type(_object['punctuate']) is list:
				_object['punctuate'] = self.__lexical__({'t': _object['punctuate']}, 't')
			### return string with punctuation
			return _object['formatted'] + _object['punctuate']
		### return substring without formatting	
		else:
			return _object['formatted']
	### retrieve string from substring list in dict with pseudo number generator from range of list length
	def __lexical__ (self, key, value):
		return key[value][random.randrange(len(key[value]))] 
	### construct dict from LX.get method or dict to LX then calling .get
	def __format__ (self, _object):
		if isinstance(_object, LX):
			return _object.get()
		elif isinstance(_object, Lexicon):
			return _object.get()
		elif type(_object) is dict:
			return LX(**_object).get()
		elif type(_object) is list:
			return LX(key = _object).get()
		else:
			return _object
	### process the object supplied to the constructor
	def __process__ (self, _object):
		## if object is a list iterate over all elements and attempt to format
		if type(_object) is list:
			for i in range(0, len(_object)):
				### replace instances with foramtted dict
				_object[i] = self.__format__(_object[i])
		else:
			### replace instances with formatted dict
			_object = self.__format__(_object)
		### return formatted dict
		return _object
	### constructor
	def __init__ (self, _object):
		self._object = self.__process__(_object)


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
	### returns the _object created from selenium
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
			### set the request_open _object to the connection point
			self.request_open = urllib2.urlopen(self.request__object)
		except:
			self.request_open = None
		### if request was successful read the content of the page
		if self.request_open:
			### return the read content
			return self.__content__()
		### return None if connection failed
		else:
			return None
	### construct the http request _object for fetching the webpage
	def __format__ (self):
		### confirm that the constructor has a URL
		if self.request_url:
			### check if the http headers dict is not empty
			if bool(self.request_headers):
				### if dict has at least one key pair value accept as http headers
				return urllib2.Request(self.request_url, urllib.urlencode(self.request_headers))
			else:
				### use standard http request _object
				return urllib2.Request(self.request_url)
		else:
			return None
	### constructor
	def __init__ (self, URL = None, headers = {}):
		self.request_url = URL
		self.request_headers = headers
		self.request__object = self.__format__()

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

	def __handlebars__(self):
		self.__dee__(String().concat("your handlebars files is ready. what do you want to call it?"))

		if self.__attr__("a template name", "your handlebars file", "handlebars_name"):
			self.handlebars_name = self.handlebars_name
		else:
			self.__dee__(String().concat("you didn't give it a name. i'll create a temporary one"))
			self.handlebars_name = self.name + "_temp"

		if not re.compile(".+\.{1}handlebars").match(self.handlebars_name):
			self.handlebars_name = self.handlebars_name + ".handlebars"

		self.__dee__(String().concat("your file is", str_random(dee_fragment, "self_reference_title"), String({'str':String(self.handlebars_name).tag(),'attr':{'color':'darkcyan','weight':'bold'}}).get() + "." ))


	def __edit__ (self):
		self.__dee__(String().concat((str_random(dee_fragment, "self_pause") + "."), str_random(dee_fragment, "self_i"), "can", str_random(dee_fragment, "act_try"), "to edit this for you.", (str_random(dee_fragment, "self_attempt") + "?")))

		if Request(prompt = String().concat("allow", self.deee.name, "to perform automatic edits?")).open():
			anchor_hyperlinks = self.soup.select('a[href]')

			#print anchor_hyperlinks, "\n"

			for anchor in anchor_hyperlinks:

				anchor["href"] = "{{clickUrl}}"
				anchor["title"] = "{{headline}}"
				anchor["target"] = "_blank"

				#print String().CYAN + anchor["href"] + String().END

			if Request(prompt = String().concat("do you want to review", self.deee.name + "'s", "edits?")).open():
				#print anchor_hyperlinks
				print "\n" + self.soup.prettify() + "\n"

	### notify user that they have HTML for review
	def __display__ (self):
		if 'BeautifulSoup' not in sys.modules:
			from bs4 import BeautifulSoup



		self.soup = BeautifulSoup(self.HTML.get_attribute("outerHTML"), "html.parser")

		if Request(prompt = "do you want to review the HTML snippet?").open():
			print "\n", (String().BLUE + self.soup.prettify() + String().END), "\n"

	### attempt to locate the child node of the parent
	def __node__ (self):
		### prompt user to choose a css selection method for the child node
		self.__dee__(String().concat((str_random(dee_fragment, "self_pause") + "."), "what", str_random(dee_fragment, "name_logic"), "should i use to", str_random(dee_fragment, "self_find"), "the child", str_random(dee_fragment, "name_html") + "?"))
		### prompt user to enter either automatic or manual
		if self.__attr__("automatic or manual", "method", "method", {'a':"automatic",'b':"manual"}):
			### notifer user that they have selected the automatic selection method
			if str.upper(self.method) == str.upper("automatic"):
				self.__dee__(String().concat(str_random(dee_fragment, "self_im"), "to", str_random(dee_fragment, "self_find"), "the", (str_random(dee_fragment, "name_html") + str_random(dee_punct, "self_end_all")) , (str_random(dee_complete, "proceed_end") + str_random(dee_punct, "self_end"))))
				### set the selection method to select a wildcard element that is the first child of the parent element
				self.Node = "> *:first-child"
			else:
				### prompt user to define their CSS selector
				self.__dee__(String().concat(str_random(dee_fragment, "self_reference_you_want"), "to try", str_random(dee_fragment, "self_find"), "the", str_random(dee_fragment, "name_html"), str_random(dee_fragment, "self_reference_you_self_end") + str_random(dee_punct, "self_end_all"), str_random(dee_complete, "proceed_end") + str_random(dee_punct, "self_end")))
				### prompt user to input their selector
				self.__attr__("a HTML/CSS selector", "HTML/CSS", "Node")

			### notify user that dee is attempting to find the provided css selector
			self.__dee__(String().concat(str_random(dee_complete, "act_attempt") + str_random(dee_punct, "self_end")))
			### handler any issues with the javascript execution
			try:
				### assign if the element was found on the page
				self.HTML = self.browser.driver.execute_script('return document.querySelector("'+ String().concat(self.CSSPath, self.Node) +'");')
			except:
				### assign None Type if there was an issue finding the node or an error occured
				self.HTML = None
			### if the HTML element was not found on the page
			if not self.HTML:
				### print error message stating that there was an issue locating the element
				self.__dee__(String().concat((str_random(dee_complete, "puzzled") + str_random(dee_punct, "self_end_all")), (str_random(dee_complete, "found_failure") + ".")))
				### prompt user if they wish to redefine their selector
				self.__dee__(String().concat("would you like to try again?"))
				### prompt user to resupply their CSS selector
				if Request().open():
					return self.__node__()
				else:
					self.__dee__(String().concat("we're giving up?", str_random(dee_complete, "frustrated") + "."))
					return False
			### if the HTML element was found on the page
			else:
				### notify user that the action was successful
				self.__dee__(String().concat(String({'str':String(str_random(dee_complete, "found_success") + str_random(dee_punct, "self_end")).tag(),'attr':{'color':'green','weight':'bold'}}).get(), str_random(dee_complete, "celebrate_combined") + str_random(dee_punct, "self_end")))
				return True

		### exit program
		else:
			### notify user that the input must been one or the other and that it will not work without a binary selection
			self.__dee__(String().concat(str_random(dee_fragment, "self_pause") + str_random(dee_punct, "self_end"), "sorry.", "i", str_random(dee_fragment, "self_attempt_unable"), str_random(dee_fragment, "self_find"), "anything without a selection method."))
			return False
	### attempt to locate the closets possible CSS element to the HTML target
	def __css__ (self):
		### prompt users to input a valid CSS selector
		self.__dee__(String().concat((str_random(dee_fragment, "self_pause") + "."), 
			str_random(dee_fragment, "self_what"), "the", String({'str':"{{CSS}}",'attr':{'weight':'bold'}}).get(), "selector for the", String({'str':"{{parent container}}",'attr':{'weight':'bold'}}).get(), "on this webpage?"))
		### request user to supply CSS selector for the selenium browser
		### fetch data through the generic response handler
		if self.__attr__("CSS selectors", "CSS selector", "CSSPath"):
			### notify user that 'dee' will try and locate the specified selector
			self.__dee__(String().concat( str_random(dee_complete, "attempt") + str_random(dee_punct, "self_end")))
			### assign attempted match the the self _object
			self.CSS = self.browser.driver.execute_script('return document.querySelector("'+ self.CSSPath +'");')
			### test if selenium found the requested element on the page
			if not self.CSS:
				### notify user that the browser was unable to locate the element on the page
				self.__dee__(String().concat(str_random(dee_fragment, "self_i"), str_random(dee_complete, "pause"), (str_random(dee_complete, "found_failure") + ".")))
				
				self.__dee__(String().concat(str_random(dee_fragment, "act_perform"), "to try again?"))
				### prompt user to resupply their CSS selector
				if Request().open():
					### recall function
					return self.__css__()
				else:
					return False
			### notify user that the element was found on the page
			else:
				### write success message
				self.__dee__(String().concat(String({'str':String(str_random(dee_complete, "found_success") + str_random(dee_punct, "self_end") ).tag(),'attr':{'color':'green','weight':'bold'}}).get()))
				return True
		### notify user that CSS selector is required 
		else:	
			### print error message to the user
			self.__dee__(String().concat((str_random(dee_complete, "frustrated") + str_random(dee_punct, "self_end")), str_random(dee_fragment, "self_i"), str_random(dee_fragment, "self_attempt_unable"), "target blank elements!"))
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
			self.__dee__(String().concat((str_random(dee_complete, "puzzled") + str_random(dee_punct, "self_end_all")), "there's an {{issue}} reaching that webpage."), {'color':'red','weight':'bold'})
			self.__dee__(String().concat(str_random(dee_fragment, "self_attempt"), "try", str_random(dee_fragment, "self_attempt_difference"), "URL?"))
			### prompt user to retry the web request
			if Request().open():
				### close the selenium instance to prevent conflicts
				self.browser.quit()
				### recall process url
				self.__page__()
				### reinitalise selenium browser
				self.__browser__()
				### recall function
				return self.__fetch__()
			else:
				self.__dee__(String().concat("well. i'm not sure what caused that problem. try again later?"))
				return False
		else:
			self.__dee__(String().concat(str_random(dee_complete, "connect_success") + str_random(dee_punct, "self_end")))
			return True
	### attempt to create a selenium webdriver
	def __browser__ (self, attempted = False):
		### avoid priting out double status messages if required
		if not attempted:
			### print the action required by dee
			### notify user that the terminal might 'hang' if the request webpage takes awhile to load
			self.__dee__(String().concat(str_random(dee_fragment, "self_im"), "going to", str_random(dee_fragment, "act_try"), "to", str_random(dee_fragment, "self_website_open"), "that", str_random(dee_fragment, "name_website"), "for you."))
			self.__sys__(String().concat("** this terminal will wait for", self.deee.__name__(), "to finish loading the page", self.URL))
			self.__sys__("** if this is taking too long try stop the browser from loading, and the terminal should resume **")
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
	def __page__ (self):
		### request the user to input a valid url
		self.__dee__(String().concat((str_random(dee_fragment, "self_pause") + "."), str_random(dee_fragment, "self_what"), "the", String({'str':"{{website url}}",'attr':{'weight':'bold'}}).get(), "for", String({'str':String(self.name).tag(),'attr':{'color':'darkcyan','weight':'bold'}}).get() + "?"))
		### request user to supply the URL for the selenium browser
		### fetch data through the generic response handler
		if self.__attr__(String().concat(self.name + "'s",  "website URL"), "URL", "URL"):
			return True
		else:
			### print the issue to the user
			self.__dee__(String().concat((str_random(dee_complete, "frustrated") + str_random(dee_punct, "self_trailing")), str_random(dee_fragment, "self_i"), 
				str_random(dee_fragment, "self_require"), "a webpage url to operate any further.", str_random(dee_complete, "request"), "include one!"))
			return False
	### request the directory to save files
	def __dirs__ (self):
		### non corrupted file path (does not include string colour)
		path = str(self.dirs) + "/" + str(self.name)
		### edited file path (contains string colour)
		path_string = String({'str':String(str(self.dirs) + "/").tag(),'attr':{'weight':'bold'}}).get() + String({'str':String(str(self.name)).tag(), 'attr':{'color':'darkcyan','weight':'bold'}}).get()
		### request user to confirm whether the program can save the created files in the directory the script is being run from
		self.__dee__(
			Lexicon([
				LX(key = [
					Lexicon([
						LX(key = ["ok"], punctuate = ".", optional = 3),
						LX(key = [
							Lexicon([
								LX(key = ["next", "next steps"])
							]),
							Lexicon([
								LX(key = ["so"], punctuate = ",", optional = 5),
								LX(key = ["moving on"])
							])
						], punctuate = ".")
					])
				], optional = 4),

				LX(key = [
					Lexicon([
						LX(key = ["i'm going to", "i'm gonna"]),
						LX(key = ["create", "make", "build"]),
						LX(key = ["some files", "a couple of files"]),
						LX(key = ["for you and"]),
						LX(key = ["save them", "store them"]),
						LX(key = ["here", "in this directory", "in this folder", "in this location"], punctuate = ":")
					])
				])
			])
		)
		### print directory path
		self.__dee__(Lexicon([LX(key = [path_string])]))
		### confirm if the directory is ok to be written to
		self.__dee__(
			Lexicon([
				LX(key = ["is"]),
				LX(key = [
					Lexicon([
						LX(key = ["that the"]),
						LX(key = [
							Lexicon([
								LX(key = ["correct", "right"]),
								LX(key = ["working"], optional = 4),
								LX(key = ["directory", "folder", "path"])
							])
						], punctuate = "?")
					]),
					Lexicon([
						LX(key = ["this"]),
						LX(key = [
							Lexicon([
								LX(key = ["directory", "folder", "path"]),
								LX(key = ["ok"])
							]),
							Lexicon([
								LX(key = ["ok", "fine", "alright"])
							]),
							Lexicon([
								LX(key = ["the correct", "the right"]),
								LX(key = ["directory", "folder", "path"])
							])
						], punctuate = "?")
					])
				])
			])
		)
		
		### if the user does not allow the program to save in the selected directory, prompt for a change request
		if not Request().open():
			### print that path was acknowledged to be incorrect / changed
			self.__dee__(
				Lexicon([
					LX(key = [
						Lexicon([
							LX(key = ["oh"], punctuate = ["!", "."]),
							LX(key = ["sorry"], punctuate = ["!", "."], optional = 5)
						]),
						Lexicon([
							LX(key = ["my"]),
							LX(key = ["mistake", "bad"])
						]),
						Lexicon([
							LX(key = ["that's"]),
							LX(key = [
								Lexicon([
									LX(key = ["incorrect", "wrong", "not right"])
								]),
								Lexicon([
									LX(key = ["not what you"]),
									LX(key = ["wanted", "wanted to use"])
								])
							], punctuate = "?")
						])
					], optional = 6),
					LX(key = [
						Lexicon([
							LX(key = ["ok", "alright"])
						]),
						Lexicon([
							LX(key = ["no problem", "not a problem"])
						])
					], punctuate = ".", optional = 5),

					LX(key = [
						Lexicon([
							LX(key = ["please"]),
							LX(key = ["type", "write", "input"]),
							LX(key = ["the new", "the updated", "the adjusted"]),
							LX(key = ["path", "directory", "folder", "destination"], punctuate = ".")
						]),
						Lexicon([
							LX(key = ["what is", "what's"]),
							LX(key = ["the"]),
							LX(key = ["uhh"], punctuate = [",", "..", "--"], optional = 6),
							LX(key = ["new", "updated", "correct"]),
							LX(key = ["path", "directory", "folder", "destination"], punctuate = "?")
						]),
						Lexicon([
							LX(key = ["what do you want to", "what would you like to"]),
							LX(key = ["change", "alter", "update"]),
							LX(key = ["the new path to", "the path to"], punctuate = "?")
						])
					])
				])
			)
			### print change directory response

			### request user to supply the folder path for the generated files
			### fetch data through the generic response handler
			if self.__attr__("your new {{Full Folder Path}}", "the {{folder path}}", "dirs"):
				### print that path has been updated to the new directory 
				self.__dee__(
					Lexicon([
						LX(key = [
							Lexicon([
								LX(key = ["ok", "alright", "cool"], punctuate = ",", optional = 3),
								LX(key = ["your"]),
								LX(key = [
									Lexicon([
										LX(key = ["folder", "folder path"])
									]),
									Lexicon([
										LX(key = ["file path"])
									])
								]),
								LX(key = ["has been", "was"]),
								LX(key = ["edit", "updated", "changed"])
							]),
							Lexicon([
								LX(key = ["you're the boss", "you got it", "got it"], punctuate = "."),
								LX(key = ["folder path", "directory"]),
								LX(key = ["edit", "updated", "changed"])
							]),
							Lexicon([
								LX(key = ["understood", "gotcha", "no problem", "got it"], punctuate = ["!","."]),
								LX(key = ["file path", "directory"]),
								LX(key = ["changed", "updated", "modified"])
							]),
							Lexicon([
								LX(key = ["cool", "alright", "nice"], punctuate = "."),
								LX(key = ["that's been"]),
								LX(key = [
									Lexicon([
										LX(key = ["changed", "edited", "replaced", "updated"]),
										LX(key = ["for you"], optional = 3)
									])
								], punctuate = ".")
							]),
							Lexicon([
								LX(key = ["ok"]),
								LX(key = ["changed", "fixed it", "updated"], punctuate = "."),
								LX(key = ["uhh, yeah"], punctuate = ","),
								LX(key = ["that's"]),
								LX(key = ["actually", "totally"]),
								LX(Key = ["the"]),
								LX(key = ["directory", "folder", "path"]),
								LX(key = ["i meant"])
							]),
							Lexicon([
								LX(key = ["okie dokie", "ok", "cool", "no problem", "no drama"]),
								LX(key = ["everything will"]),
								LX(key = ["go", "be stored", "be saved"]),
								LX(key = ["there"])
							])
						], punctuate = ".")
					])
				)
				### print newline to clean output
				print ""
				return True
			else:
				### print the issue to the user
				

				return False
			
		else:
			### keep the default storage path
			self.dirs = path
			### print that files will be created in the automatically generated folder path
			self.__dee__(
				Lexicon([
					LX(key = [
						Lexicon([
							LX(key = ["ok", "alright"], punctuate = ",", optional = 4),
							LX(key = ["i'll"]),
							LX(key = [
								Lexicon([
									LX(key = [
										Lexicon([
											LX(key = ["continue to"]),
											LX(key = ["store", "write", "create", "make"]),
											LX(key = ["files in the"]),
											LX(key = ["same", "current", "default"], attr = {'weight':'bold'}),
											LX(key = ["folder", "directory"])
										]),
										Lexicon([
											LX(key = ["keep on"]),
											LX(key = ["storing", "saving"]),
											LX(key = ["my"], optional = 5),
											LX(key = ["files", "code", "stuff"]),
											LX(key = [
												Lexicon([
													LX(key = ["in"]),
													LX(key = [
														Lexicon([
															LX(key = ["the"]),
															LX(key = ["selected", "predefined"], attr = {'weight':'bold'})
														]),
														Lexicon([
															LX(key = ["same", "current"], attr = {'weight':'bold'})
														])
													]),
													LX(key = ["folder", "directory", "area"])
												]),
												Lexicon([
													LX(key = ["there", "here"])
												])
											])
										])
									]),
									
								])
							], punctuate = ".")
						])
					])
				])
			)
			### print newline to clean output
			print ""

			return True

	### request the name of the partner page
	def __name__ (self):
		### print request to user
		### prompt name
		self.__dee__(
			Lexicon([
				### tplvl
				LX(key = [
					Lexicon([
						LX(key = ["firstly"], punctuate = ",")
					]),
					Lexicon([
						LX(key = ["first step", "here we go", "let's start"], punctuate = ".")
					]),
					Lexicon([
						LX(key = ["step"]),
						LX(key = [
							Lexicon([
								LX(key = ["one"], punctuate = ";")
							]),
							Lexicon([
								LX(key = ["uhh"], punctuate = ",", optional = 3),
								LX(key = ["uno"], punctuate = ","),
								LX(key = [
									Lexicon([
										LX(key = ["i"]),
										LX(key = ["guess", "think"]),
										LX(key = ["that's"]),
										LX(key = ["right", "correct"], punctuate = "?"),
										LX(key = ["anyway"], punctuate = ",")
									])
								], optional = 7)
							])
						])
					]),
					Lexicon([
						LX(key = [
							Lexicon([
								LX(key = ["let's"]),
								LX(key = ["get this started", "get started", "start", "do this", "go"], punctuate = ["!", "."])
							]),
							Lexicon([
								LX(key = ["alright", "ok"]),
								LX(key = ["time to make a partner"])
							]),
							Lexicon([
								LX(key = ["time to make a something"], punctuate = "?"),
								LX(key = ["ok", "alright", "neat", "cool"], punctuate = ".")
							])
						])
					])
				], optional = 6),
				### tplvl
				LX(key = [
					Lexicon([
						LX(key = ["what's", "what is"]),
						LX(key = ["the"]),
						LX(key = ["name", "title"]),
						LX(key = ["of the"]),
						LX(key = ["new"], optional = 3)
					])
				]),
				### tplvl
				LX(key = ["Gemini Partner"], attr = {'weight':'bold'}),
				LX(key = [
					Lexicon([
						LX(key = ["we're"]),
						LX(key = ["setting up", "creating", "building", "making"])
					])
				], punctuate = "?")
			])
		) 
		### request user to supply the name of the partner
		### fetch data through the generic response handler
		if self.__attr__("the {{Gemini partner's name}}", "the {{partner's name}}", "name"):
			### print the formulated partner
			### gemini partner name missing string
			self.__dee__(
				### name acceptance
				Lexicon([
					### subject
					LX(key = [
						### constructor
						Lexicon([
							LX(key = ["you're"]),
							LX(key = ["building", "creating", "setting up", "developing"]),
							LX(key = [self.name], attr = {'weight':'bold'})
						]),
						### constructor
						Lexicon([
							LX(key = ["the partner is"]),
							LX(key = ["going to be"], optional = 4),
							LX(key = ["titled", "named", "called"]),
							LX(key = [self.name], attr = {'weight':'bold'})
						]),
						### constructor
						Lexicon([
							LX(key = ["you're"]),
							LX(key = ["setting up", "building", "making"]),
							LX(key = ["content", "files", "code"]),
							LX(key = ["for"]),
							LX(key = [self.name], attr = {'weight':'bold'})
						])
					], punctuate = "."),
					### predicate
					LX(key = [
						### constructor
						Lexicon([
							LX(key = ["let's do it", "alright, neat", "cool beans", "nice, man", "nice"]),
						]),
						### constructor
						Lexicon([
							LX(key = ["strange", "interesting", "odd", "cool", "decent", "i hate the"]),
							LX(key = ["name"]),
							LX(key = ["but, whatever"], optional = 8)
						]),
						### constructor
						Lexicon([
							LX(key = ["i"]),
							LX(key = ["like it", "approve"])
						]),
						### constructor
						Lexicon([
							LX(key = ["gotcha", "got it", "you got it", "ok", "no problem"])
						])
					], punctuate = ".", optional = 4)
				])
			)
			### print newline to clean output
			print ""
			### continue proceedures 
			return True
		else:
			### print the issue to the user	notifying that a string was not provided
			self.__dee__(
				### constructor
				Lexicon([
					### subject
					LX(key = [
						Lexicon([
							LX(key = ["so"], punctuate = ",", optional = 10),
							LX(key = [
								Lexicon([
									LX(key = ["it"]),
									LX(key = ["seems that", "appears that", "looks like"]),
									LX(key = ["you"])
								]),
								Lexicon([
									LX(key = ["you"])
								])
							]),
							LX(key = ["didn't"], attr = {'weight':'bold'}),
							LX(key = ["type", "enter", "write", "input"]),
							LX(key = ["a name for the"]),
							LX(key = ["Gemini Partner"], attr = {'weight':'bold'})
						])
					], punctuate = ".")
				])
			)
			### notify user to reattempt running the program
			self.__dee__(
				### constructor
				Lexicon([
					### subject
					LX(key = [
						Lexicon([
							LX(key = ["i use that name to"]),
							LX(key = [
								Lexicon([
									LX(key = ["process", "format"]),
									LX(key = ["my output"])
								])
							], punctuate = ".")
						])
					]),
					### predicate
					LX(key = [
						Lexicon([
							LX(key = ["so"], punctuate = ",", optional = 3),
							LX(key = ["that means you"]),
							LX(key = ["need to", "have to"]),
							LX(key = ["restart", "re-run"]),
							LX(key = ["my program file", "the program", "the script"], punctuate = "."),
							LX(key = ["sorry"], punctuate = [".", "..."], optional = 4)
						]),
						Lexicon([
							LX(key = ["because of that"], punctuate = ","),
							LX(key = ["can you please", "could you please"]),
							LX(key = ["restart", "re-run"]),
							LX(key = ["my program file", "the program", "the script"], punctuate = "?")
						])
					])
				])
			)
			### end process
			return False


	### assign attribute of class through input method
	def __attr__ (self, input_message, confirm_message, object_name, binary = {}):
		### attempt to set the attribute of the class
		def __setattribute__ ():
			### prompt user to input a string based on supplied criteria
			temp = raw_input(self.__sys__(String().concat("please enter", (String({'str': String(str(input_message)).tag(), 'attr': {'weight':'bold'}}).get() + ": ")), printt = False)) or None
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
			### optional handler for accepting binary responses
			elif bool(binary):
				### confirm is string matches one of two conditions
				if (str.upper(temp) == str.upper(binary['a'])) or ( str.upper(temp) == str.upper(binary['b'])):
					### handle change response
					return __changeattribute__(temp)
				else:
					### notify user that the input provided did not match either pattern
					self.__sys__(String().concat("input must match either", String({'str':"{{"+ binary['a'] +"}} or {{"+ binary['b'] +"}}",'attr':{'weight':'bold'}}).get()))
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
				setattr(self, object_name, temp)
				### return self _object
				return self
			### if the input entered was incorrect
			else:
				### prompt user to attempt to recall function and reset value
				if Request(prompt = "change value?").open():
					### recall primary function
					return __setattribute__()
		### return attribute
		return __setattribute__()

	def __lexicon__ (self, str__object, key):
		return str__object[key][random.randrange(len(str__object[key]))]

	def __grammar__ (self, responses):
		for i in range(0, len(responses)):
			if type(responses[i]) is dict:
				responses[i] = self.__lexicon__(responses[i]['key'], responses[i]['value'])


		return "".join(responses)
		

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
	def __dee__ (self, message, attr = {}, printt = True):
		if isinstance(message, Lexicon):
			message = message.get()
		if not bool(re.search("^$", message)):
			return self.__rop__(self.deee.response(message, attr), printt)
	### primary function handler for class
	def __main__ (self):
		if self.__name__():
			if self.__dirs__():
				if self.__page__():
					if self.__browser__():
						if self.__fetch__():
							if self.__css__():
								if self.__node__():
									if self.__display__():
										if self.__edit__():
											self.__handlebars__()
	### return self _object
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

