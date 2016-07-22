#!/usr/bin/python
#sys.argv[1:]

###################################
### python scripts dependencies ###
###################################
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
### py json class package
import json
### py pwd class package
import pwd
### py system class package
import sys
### py os class package
import os
### py regex
import re

### script exe base file directory
__filepath__ = os.path.dirname(os.path.realpath('__file__'))

class String:
	### formatting options
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
	### regexp for matching string.extname
	EXT = "^.+\.{1}\w+$"
	### concatenate multiple arguments by string character
	def cconcat (self, strlist, character = ""):
		return character.join(filter(None, strlist))
	### concatenate multiple arguments to a single string
	def concat (self, *args):
		return " ".join(filter(None, args))
	### wrap string in constructor with formatting syntax
	def tag (self, context = None):
		if (type(context) is str) and (not hasattr(self, context)):
			self.context = context
		return "{{" + self.context + "}}"
	### prints a multiple line string with formatting
	def wrap (self, width = 60):
		print '\n'.join(line.strip() for line in re.findall(r'.{1,'+ str(width) +'}(?:\s+|$)', self.__process__()) )
	### prints a single line formatted string
	def line (self):
		print self.__process__()
	### return entire formatted string using supplied styling
	def get (self, context = {}):
		### fetch returned processed context
		return self.__process__(context)
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
	### return formatted string or strings depending on config context supplied (list or dict)
	def __process__ (self, context = {}):
		### check if context isn't a default
		if not bool(context):
			### check if Class was give a constructor dict
			if self.context:
				### use constructor dict
				context = self.context
			else:
				### use a sample instead
				context = [{'str':'{{Sample}}', 'attr':{'color':'cyan'}}, {'str':'{{Text}}', 'attr':{'color':'purple'}}]
		### check if context is either a list or dict
		if type(context) is list:
			### temp list for holding formatted strings
			strs = []
			### iterate through items to be formatted
			for i in range(0, len(context)):
				### append formatted strings to temp list
				strs.append(self.__substitute__(context[i]['str'], context[i]['attr']))
			### return the complete string with formatting
			return self.concat(strs)
		else:
			### return the complete string with formatting
			return self.__substitute__(context['str'], context['attr'])
	### return the type of the context
	def __type__ (self):
		return type(self.context)
	### return the context supplied
	def __self__ (self):
		return self.context
	### constructor 
	def __init__ (self, context = {}):
		self.context = context


class JSON:
	### attempt to fetch formatted json from string or file
	def fetch (self, method = "strs"):
		### determine which method to operate
		return self.__method__(method)
	### determine method to parse json
	def __method__ (self, method):
		### format method string to match class function string pattern
		method = String().cconcat(["__", method, "__" ])
		### confirm if self has the method defined within self
		if hasattr(self, method):
			### call found function
			return getattr(self, method)(self.context)
	### attempt to parse json from string
	def __strs__ (self, context):
		### attempt to call json load as string method
		try:
			### return formatted json as dict
			return json.loads(context)
		### handle exception error for failing to load json
		except:
			### return False type for error handling
			return False
	### attempt to call json loads as string method
	def __file__ (self, context):
		### attempt to load supplied file instance as context argument
		try:
			### attempt to load string path / file instance
			with open(context) as file:
				### attempt to load file contents as json
				try:
					return json.load(file)
				### handle exception error for failing to parse json
				except:
					### return False type for error handling
					return False
		### handle exception error for failing to open file in context
		except:
			### return False type for error handling
			return False
	### constructor
	def __init__ (self, context = '{"example":"json"}'):
		self.context = context




class List:
	### fetch index of list item
	def index (self, index = 0):
		### attempt to fetch and return list item without error if out of range
		try:
			### return list item
			return self.context[index]
		### handle exception
		except:
			### return False for possible evaluator
			return False
	### constructor
	def __init__ (self, context = []):
		self.context = context



class Lexicon (String):
	### return lexical text
	def create (self):
		### format context object
		return self.__format__()
	### return string from random selection
	def __lexical__ (self, key, value):
		return key[value][random.randrange(len(key[value]))]
	### return formatted string based on LX configuration
	def __construct__ (self, context):
		### obtain random string
		context['formatted'] = self.__lexical__(context['key'], context['value'])
		### format string with colours, weight, underline if attr dictionary 
		if bool(context['attr']):
			### call String class
			context['formatted'] = self.get({'str': self.tag(context['formatted']), 'attr': context['attr']})
		### append string with puncutation
		if bool(context['punctuate']):
			### select from list of punctuation if supplied
			if type(context['punctuate']) is list:
				### obtain random punctuation from list
				context['punctuate'] = self.__lexical__({'t': context['punctuate']}, 't')
			### append punctuation to the formatted string
			context['formatted'] = (context['formatted'] + context['punctuate'])
		### return formatted string including optional punctuation
		return context['formatted']
	### return formatted string if random number generated was not considered a boolean
	def __optional__ (self, context):
		### if LX dict optional was set as false format string
		if not context['optional']:
			### return formatted string
			return self.__construct__(context)
		else:
			### if LX was provided a int or float attempt to run formatting
			if (type(context['optional']) is int) or (type(context['optional']) is float):
				### if number returned was equal to zero format string
				if not bool(random.randrange(int(context['optional']))):
					return self.__construct__(context)
		### return empty string if context dict did not pass optional
		return ""
	### return formatted string whether or not it was formatted
	def __process__ (self, context):
		processed = []
		### process a single item object
		if not type(context) is list:
			### check if single item was optionally formatted
			processed.append(self.__optional__(context))
		### process multiple objects
		else:
			### iterate over the context object
			for i in range(0, len(context)):
				### check if single item was optionally formatted
				processed.append(self.__optional__(context[i]))
		### return seperated string
		return " ".join(filter(None, processed))
	### return formatted instance as dictionary
	def __type__ (self, context):
		### process objects that are not list type
		if not type(context) is list:
			### process individual item
			if type(context) is dict:	
				### parse dictionary as named arguments to LX class
				context = LX(**context).create()
			### process items that are instances of classes LX or Lexicon
			elif isinstance(context, LX) or isinstance(context, Lexicon):
				### call class operator to return string or formatted dictionary
				context = context.create()
		### process items as list
		else:
			### parse list as the key to LX class and return formatted dictionary
			context = LX(key = context).create()
		### return formatted object
		return context
	### format self.object to be valid Lexicon data
	def __format__ (self):
		### process single item object
		if not type(self.context) is list:
			### format type object data
			self.context = self.__type__(self.context)
		### process multiple objects
		else:
			### iterate over object
			for i in range(0, len(self.context)):
				### format type object data
				self.context[i] = self.__type__(self.context[i])
		### process formatted data
		return self.__process__(self.context)
	### constructor
	def __init__ (self, context = {}):
		self.context = context



class LX:
	### return formatted dictionary from self
	def create (self):
		return self.__dict__
	### format key to be list
	def __format__ (self, key):
		### process single supplied object
		if not type(key) is list:
			### convert object type to be string 
			return self.__type__(key)
		else:
			### iterate list supplied as key
			for i in range(0, len(key)):
				### convert object type to be string 
				key[i] = self.__type__(key[i])
			### return valid dictionary object
			return {'t': key }
	### return formatted instance as string
	def __type__ (self, context):
		### process single object
		if not type(context) is list:
			### check if object is instance of Lexicon
			if isinstance(context, Lexicon):
				### process and return Lexical string
				context = context.create()
			### return formatted string
			return context
		### process multiple instances
		else:
			### iterate over objects
			for i in range(0, len(context)):
				### check if object is instance of Lexicon
				if isinstance(context[i], Lexicon):
					### process and return Lexical string
					context[i] = context[i].create()
			### return formatted string
			return context
	### constructor	
	def __init__ (self, **kwargs):
		self.key = self.__format__(kwargs.pop('key', {}))
		self.value = kwargs.pop('value', 't')
		self.attr = kwargs.pop('attr', {})
		self.punctuate = kwargs.pop('punctuate', None)
		self.optional = kwargs.pop('optional', False)



class Responder (String):	
	### returns a string (optionally filtered) prefixed by the name of the responder
	def response (self, message = "destory all humans!", attr = {}):
		### return formatted concatenated string
		return self.concat((self.__name__() + self.seperator), self.__message__(message, attr))
	### private class for fetching the formatted string for the message part of ai response
	def __message__ (self, message = "destroy all humans!", attr = {}):
		### call inherited class of string to format string
		return self.get({'str': message, 'attr': attr})
	### private class for fetching and formatting the string that defines the ai's name
	def __name__ (self):
		### encapsulate name of responder in formatting syntax, instantiate to String class
		return self.get({'str': String(self.name).tag(), 'attr': self.style})
	### constructor
	def __init__ (self, **kwargs):
		self.name = kwargs.pop('name', 'system')
		self.style = kwargs.pop('style', {'style':'underline','weight':'bold'})
		self.seperator = kwargs.pop('seperator', ':')



class Set (String):
	### return dictionary with returned response and boolean
	def open (self):
		### check if supplied request a string
		if type(self.request) is str:
			### format string to request for single entity type
			self.request_string = self.request
		### check if supplied request is a list
		elif type(self.request) is list:			
			### format message as a multiple option choice
			### concatenate request string
			self.request_string = self.cconcat(self.request, "/")
		else:
			### return response handler
			return {'bool': False, 'response': None}
		### prompt user to input the requested type
		return self.__prompt__()
	### evaluate user string against potential options
	def __compare__ (self):
		### if request type is a string
		if type(self.request) is str:
			### proceed to confirmation
			return self.__confirm__()
		### if request type is a list of mutliple sections
		elif type(self.request) is list:
			### iterate over list of options within supplied list
			for i in range(0, len(self.request)):
				### remove formatting from listed string
				match_string = re.sub("{{|}}", "", self.request[i])
				### compare if the supplied string is equal to the options within the list
				if str.upper(match_string) == str.upper(self.user):
					### if match is found proceed to confirmation
					return self.__confirm__(match_string)
			### if no match occurred notify user that their input wasn't found
			self.__sys__(self.concat("user input", self.get({'str': self.tag(str.upper(self.user)), 'attr':{'weight':'bold'}}), "did not match", self.request_string))
			### prompt user to reattempt selection
			if Request(prompt = "try again?").open():
				### recall user input handler
				return self.__prompt__()
			### if user selected to not continue
			else:
				### return response handler
				return {'bool': False, 'response': None}
	### confirm if the provided input was the correct selection
	def __confirm__ (self, response = None):
		### if string was not provided to function
		if not response:
			### set response string as the user string provided in single option conformation
			response = self.user
		### prompt user to confirm their inputted text
		self.__sys__(self.concat("is", self.get({'str': self.tag(response), 'attr': {'weight': 'bold'}}), "the correct value for", self.cconcat([self.get({'str':self.response, 'attr':{'weight':'bold'}}), " "], "?") ))
		### if user selected to keep input
		if Request().open():
			### return response handler
			return {'bool': True, 'response': response}
		### if user opted to not keep input
		else:
			### prompt user to change input
			if Request(prompt = "try again?").open():
				### recall user input handler
				return self.__prompt__()
			### if user did not choose to change input
			else:
				### return response handler
				return {'bool': False, 'response': None}
	### prompt user to input their desired value for setter	
	def __prompt__ (self):
		### print message asking user to input their desired value for the supplied options
		self.user = self.__input__(self.__sys__(self.concat(self.cconcat([self.concat("please enter", self.request_string), " "], ":")), False))
		### if returned input was empty or undefined
		if not self.user:
			### notify user that the required input cannot be empty or None type
			self.__sys__(self.get({'str': "user input cannot be {{NONE}}", 'attr':{'weight':'bold'}}))
			### prompt user to reattempt to declare their input
			if Request(prompt = "try again?").open():
				### recall function
				return self.__prompt__()
			### if user chose not to re-enter their selection
			else:
				### return response handler
				return {'bool': False, 'response': None}
		### if user supplied a string
		else:
			### compare provided string to possible ptions
			return self.__compare__()
	### print input for user
	def __input__ (self, string):
		### prompt user to input string
		return raw_input(str(string)) or None
	### return or print return the message as system
	def __sys__ (self, message, printed = True):
		### format string with formatting if required
		message = self.system.response(self.get({'str':message, 'attr': {'weight':'bold'}}))
		### print string 
		if printed:
			print message
		### return string
		return message
	### constructor 
	def __init__ (self, **kwargs):
		self.request = kwargs.pop('request', None)
		self.response = kwargs.pop('response', None)
		self.system = Responder()



class Request (String):
	### method for asking the user to input one of two provided options
	def open (self):
		### prompt user for input returning text submitted or NoneType if empty
		self.response = self.__prompt__()
		### confirm if response was equal to the confirmation string
		if self.response == self.confirm:
			### return true if user input matches the supplied confirm string
			return True
		### confirm if response was equal to the rejection string
		elif self.response == self.reject:
			### return false if the user input matches the supplied reject string
			return False
		### prompt user that the supplied input wasn't considered valid
		else:
			### concatenate string with formatting
			print self.__response__(self.concat("command", self.get({'str': self.tag(str(self.response)), 'attr':{'weight':'bold'}}), "unrecognised"))
			### recall the function
			return self.open()
	### format the strings defining the options available for the user
	def __option__ (self):
		### return formatted string with the supplied confirmation and rejection choices
		return self.get({'str': self.tag(self.cconcat([self.confirm, self.reject], "/")), 'attr':{'weight':'bold'}})
	### prompt the user to input one of the supplied action contexts
	def __prompt__ (self):
		### request the user to input their text
		response = raw_input(self.__response__(self.concat(self.prompt, self.cconcat([self.__option__(), " "], ":")))) or None
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



class Package:
	### return the fetched package or False
	def get (self):
		### attempt to locate the package
		return self.__find__()
	### assign the package to class as import or None
	def __find__ (self):
		### store result package test
		self.package = self.__test__()
		### confirm if supplied package was found or executed
		if self.package:
			### return True
			return self.package
		### package was unable to imported or executed
		else:
			### return False
			return False
	### test the existence of the package
	def __test__ (self):
		### check if class is to be run as a import or executable script
		if not self.exe:
			### try import the required package
			try:
				### attempt to import package name as python import
				__import__(self.name)
				### return True if asset can be imported
				return True
			### handle the error as an exception
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



class Install (String):
	### attempt to fetch all packages
	def all (self):
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
			print self.__response__(self.concat(self.get({'str': self.tag(self.cconcat([str(len(missing)), str(len(self.packages))], "/")), 'attr': {'color':'red','weight':'bold'}})))
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
						print self.__response__(self.concat("package", self.get({'str': self.tag(packages[i]['name']), 'attr':{'weight':'bold'}}), "could not be installed"))
						### print the appropriate solution
						print self.__response__("please download the package and install before running the program again")
						### if source is available print the URL
						if packages[i]['source']:
							print self.__response__(self.concat("packages available at", self.get({'str': self.tag(packages[i]['source']), 'attr':{'style':'underline'}})))
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
		print self.__response__(self.concat("trying to install", self.get({'str': self.tag(package['name']), 'attr':{'weight':'bold'}})))
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
			print self.__response__(self.concat(self.tag({'str': self.tag(package['name']), 'attr':{'weight':'bold'}}), "has no installer!"))
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
				print self.__response__(self.concat(self.get({'str': self.tag(self.packages[i]['name']), 'attr':{'weight':'bold'}}), "is", self.get({'str':'{{installed}}','attr':{'color':'green','weight':'bold'}})))
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



class File:
	### add new string to the end of the file
	def append (self, string):
		### move seeker to end of file
		self.file.seek(0, 2)
		### set new line in file
		self.file.write("\n")
		### write string to new line at end position
		self.file.write(string)
		### reset seeker
		self.file.seek(0)
	### removes file instance from os directory
	def remove (self):
		### remove file from defined path
		os.remove(self.file.name)
	### returns the file entity
	def get (self):
		### return file instance
		return self.file
	### returns the contents of a file if file
	def read (self, seeker = 0):
		### set seeker to defined position or beginning
		self.file.seek(seeker)
		### return contents of file
		return self.file.read()
	### writes to file, optional seeker position
	def write (self, contents = 'print "Hello"', seeker = 0):
		### confirm if file allows file to be written to
		if re.compile('[rwa]\+?', re.IGNORECASE).match(self.file.mode):
			self.file.seek(seeker)
			self.file.write(contents)
		else:
			### notify developer that their class file instance does not allow edits
			print "file mode doesn't allow writing"
	### close the file
	def close (self):
		### set file state to closed (required for revaluating script files)
		self.file.close()
	### sets seeker on the file
	def seek (self):
		### resets seeker position for reading
		self.file.seek(0)
	### creates file as a temporary file
	def __tempfile__ (self):
		### create named temporary file
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



class HTTPResource:
	### request the resource
	def fetch (self):
		return self.__open__()
	### close the connection to the resource
	def close (self):
		self.request_open.close()
	### read and return the content of the webpage
	def __content__(self):
		### set the contents of class instance to the content of HTTP resource
		self.request_content = self.request_open.read()
		### close connection
		self.close()
		### return contents
		return self.request_content
	### opens the supplied webpage with formatted headers through urllib2 
	def __open__ (self):
		### attempt to fetch the URL resource
		try:
			### set the request_open object to the connection point
			self.request_open = urllib2.urlopen(self.request_object)
		except:
			### set the request_open object to None type
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
			### if headers not provided as dict
			else:
				### use standard http request _object
				return urllib2.Request(self.request_url)
		else:
			### return None type
			return None
	### constructor
	def __init__ (self, URL = None, headers = {}):
		self.request_url = URL
		self.request_headers = headers
		self.request_object = self.__format__()



class Command:
	### return the result of the attempted command
	def process (self):
		return self.__exec__()
	### attempt to call function; uses either subprocess.call or subprocess.check_call
	def __exec__ (self):
		try:
			### initialise selected subprocess method from __funct__
			self.function(self.command, stdout = self.stdout, stderr = self.stderr, shell = self.shell)
			### return True if function ran
			return True
		### handle the subprocessor command error if command was found but not executabe
		except subprocess.CalledProcessError:
			### return False if function failed
			return False
		### handle the subprocessor command error if command not found
		except OSError:
			### return False if function failed
			return False
	### return the appropriate subprocess
	def __funct__ (self):
		### use call for observing terminal ouput; use check call for confirming silent response
		return subprocess.call if self.shell else subprocess.check_call
	### constructor
	def __init__ (self, command = "", stdout = open(os.devnull, 'w'), stderr = subprocess.STDOUT, shell = False):
		self.command = command
		self.shell = shell
		self.stdout = stdout
		self.stderr = stderr
		self.function = self.__funct__()


class PX (String):
	### produce formatted string for config.js entire container js object
	def container (self, container = {'pre':'','ind':''}, frequency = {'pre':'','ind':''}):
		return self.cconcat([container['pre'], "{", "\n", container['ind'], "    ", self.__target__(), "\n", container['ind'], "    ",  self.__selector__(), ",", "\n", container['ind'], "    ",  self.__template__(), ",", "\n", container['ind'], self.frequency(**frequency), "\n", container['pre'], "}"])
	### produce formatted string for config.js entire frequency js object
	def frequency (self, pre = "", ind = ""):
		return self.cconcat([pre, "frequency: {", "\n", "    ", ind, self.__first__(), ",", "\n", "    ", ind, self.__interval__(), "    ", "\n", pre, "}"])
	### produce formatted string for config.js first ad position
	def __first__ (self):
		### return concatenated string forming the first ad position
		return self.concat("first:", str(self.first))
	### produce formatted string for config.js ad repetition interval
	def __interval__ (self):
		### return concatenated string forming the repeated ad position
		return self.concat("interval:", str(self.interval))
	### produce formatted string for config.js child selector
	def __selector__ (self):
		### return concatenated string forming the path the child container
		return self.concat("selector:", self.cconcat(['"', self.selector, '"']))
	### produce formatted string for config.js target selector
	def __target__ (self):
		### return concatenated string forming the path the parent container
		return self.concat("target:", self.cconcat(['"', self.target, '"']))
	### produce formatted string for config.js template path
	def __template__ (self):
		### return concatenated string forming the path the handlebars template
		return self.concat("template:", self.cconcat(['"', self.cconcat([self.partner, "/", self.module, "/", self.module]), '"']))
	### constructor
	def __init__ (self, **kwargs):
		self.partner = kwargs.pop("partner", "example")
		self.module = kwargs.pop("module", "instream")
		self.target = kwargs.pop("target", "#example")
		self.selector = kwargs.pop("selector", "div")
		self.first = kwargs.pop("first", 1)
		self.interval = kwargs.pop("interval", 3)



print PX().container({'pre':'','ind':''}, {'pre':'    ', 'ind': '    '})


class Partner (String):
	### produce formatted string array for config.js
	def __push__ (self):
		pass
		#return 'containers: [\n    \n]' 
	### produce formatted string object for config.js
	def __item__ (self):
		### return formatted string with four space indentation for individual containers pathing to gemini templates
		pass
	### produce formatted config file
	def __config__ (self):
		pass
	### constructor 
	def __init__ (self, **kwargs):
		self.name = kwargs.pop("name", None)
		self.url = kwargs.pop("website", None)




class Dee (String):
	ARG = "^(?:[\.\-])*.{1}"
	AUTO = "^auto(mated)?$"
	EDIT = "^edit$"
	### main process handler
	def main (self):
		### attempt to process input context
		return self.__process__()
	### process edited start
	def __edit__ (self, actions):
		pass
	### process automated start
	def __automatic__ (self, actions):
		pass
	### process manual start
	def __manual__ (self):
		pass
	### process argument string(s)
	def __process__ (self):
		### confirm that system arguments were supplied
		if not bool(self.actions):
			### if system arguments missing setup proccess to run as normal
			return self.__manual__()
		### should system arguments be found 			
		### attempt to match the first argument instance
		elif re.compile(self.ARG).match(self.actions[0]):
			### attempt to match automatically setup expression
			if re.compile(self.AUTO).match(self.actions[0]):
				### run program with automated setup
				return self.__automatic__(self.actions[1:])
			### attempt to match edited setup expression
			elif re.compile(self.EDIT).match(self.actions[0]):
				### run program with edited setup
				return self.__edit__(self.actions[1:])
		### failed to match with expression list
		### run program with BIOS setup
		return self.__manual__()
	### constructor
	def __init__ (self, name = "dee", actions = sys.argv[1:]):
		self.responder = Responder(name = name)
		self.actions = actions
		self.partners = []




if __name__ == '__main__':
	pass
	#f = File(name = "myconfig", ext = "js", temporary = False)
	#f.write(Partner().__item__())
	#f.close()
	

	#print Dee().main()