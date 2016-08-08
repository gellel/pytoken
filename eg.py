#!/usr/bin/python
# -*- coding: utf-8 -*-
#sys.argv[1:]

###################################
### python scripts dependencies ###
###################################
### py subprocess class package
import subprocess
### py importlib class package
import importlib
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
### py datetime class package
import datetime
### py time class package
import time
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

###################################
### python dynamic dependencies ###
###################################
### py pip selenium webdriver class package
WEBDRIVER = None
### py pip bs4 class package
BS4 = None
### py file version
VERSION = 1.0


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
	REG = r"\{\{(?:[\w\s\d]*|[$&\+,\:\;\=\?@#\|'\<\>\.^\*\(\)%!-\/]*)*\}\}"
	### regexp for matching string.extname
	EXT = r"^.+\.{1}\w+$"
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
			substring = re.sub(r"{{|}}", "", matches[i])
			### replace matches[i] with dict
			matches[i] = {'original': substring, 'formatted': self.__format__(substring, attributes)}
		### iterate through matches again
		for i in range(0, len(matches)):
			### replace string with formatted text based on items in matches
			string = re.sub(matches[i]['original'], matches[i]['formatted'], string)
		### return string with formatting replacing any "{{" or "}}" that exists in original string
		return re.sub(r"{{|}}", "", string)
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





class JSON (String):
	### attempt to fetch formatted json from string or file
	def fetch (self, method = "strs"):
		### determine which method to operate
		return self.__method__(method)
	### determine method to parse json
	def __method__ (self, method):
		### format method string to match class function string pattern
		method = self.cconcat(["__", method, "__" ])
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
	def response (self, message = "destroy all humans!", attr = {}):
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
				match_string = re.sub(r"{{|}}", "", self.request[i])
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
		self.__sys__(self.concat("is", self.get({'str': self.tag(response), 'attr': {'weight': 'bold'}}), "the correct input for", self.cconcat([self.get({'str':self.response, 'attr':{'weight':'bold'}}), " "], "?") ))
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
		response = raw_input(self.__response__(self.concat(self.get({'str':self.prompt,'attr':{'weight':'bold'}}), self.cconcat([self.__option__(), " "], ":")))) or None
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
					### install status will attempt to be changed from False to True during install process
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
			self.file.write(str(contents))
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





class Folder (String):
	### create new folder
	def create (self):
		### confirm if folder has filepath
		if os.path.exists(self.path):
			### confirm if folder is to be created with timestamp in name
			if self.timestamp:
				### create datetime from supplied timestamp and stringify into formatted string
				dt = datetime.datetime.fromtimestamp(time.time()).strftime('%Y %m %d %H %M %S')
				### substitute spaces within timestamp
				dt = re.compile(r"\s+").sub("", dt)
				### set new temp path to the new folder path
				self.path = self.cconcat([self.path, dt], "_")
		### create new folder
		os.makedirs(self.path)
		### return path
		return self.path
	### constructor
	def __init__ (self, name = "gemini", timestamp = True, filepath = __filepath__):
		self.name = name
		self.filepath = filepath
		self.timestamp = timestamp
		self.path = self.cconcat([self.filepath, self.name], "/")





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




class CX (String):
	### produce formatted string for config.js entire container js object
	def container (self, tabs = ""):
		### return concatenated string forming the template object container
		return self.cconcat([tabs, "{", "\n", self.cconcat([tabs, "    "]), self.cconcat([self.__target__(), ","]), "\n", self.cconcat([tabs, "    "]), self.cconcat([self.__selector__(), ","]), "\n", self.cconcat([tabs, "    "]), self.cconcat([self.__template__(), ","]), "\n", self.frequency(self.cconcat([tabs, "    "])), "\n", tabs, "}"])
	### produce formatted string for config.js entire frequency js object
	def frequency (self, tabs = ""):
		### return concatenated string forming the template frequency object
		return self.cconcat([tabs, "frequency: {", "\n", self.cconcat([tabs, "    "]), self.cconcat([self.__first__(), ","]), "\n", self.cconcat([tabs, "    "]), self.__interval__(), "\n", tabs, "}"])
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
	### self to dict
	def __self__ (self):
		return self.__dict__
	### constructor
	def __init__ (self, **kwargs):
		self.partner = kwargs.pop("partner", "example")
		self.module = kwargs.pop("module", "instream")
		self.path = kwargs.pop("path", "https://www.example.com/path")
		self.target = kwargs.pop("target", "#example")
		self.selector = kwargs.pop("selector", "div")
		self.first = kwargs.pop("first", 1)
		self.interval = kwargs.pop("interval", 1)
		self.html = kwargs.pop("html", None)
		if not self.html:
			self.html = self.cconcat([self.cconcat(['<div id="gemini-ad-example" class="gemini-example-ad">', "\n"]), self.cconcat(["    ", '<div class="main-image row">', "\n"]), self.cconcat(["    ", "    ", '<figure>', "\n"]), self.cconcat(["    ", "    ", "    ", '<a href="{{headline}}" target="_blank">', "\n"]), self.cconcat(["    ", "    ", "    ", "    ", '<img src="{{#if secHqImage}}{{secHqImage}}{{else}}{{#if secImage}}{{secImage}}{{else}}{{image}}{{/if}}{{/if}}" alt="{{headline}}">', "\n"]), self.cconcat(["    ", "    ", "    ", '</a>', "\n"]), self.cconcat(["    ", "    ", '</figure>', "\n"]), self.cconcat(["    ", '</div>', "\n"]), self.cconcat(["    ", '<div class="main-headline row">', "\n"]), self.cconcat(["    ", "    ", '<h1>', "\n"]), self.cconcat(["    ", "    ", "    ", '<a href="{{headline}}" target="_blank">', "\n"]), self.cconcat(["    ", "    ", "    ", "    ", '{{headline}}', "\n"]), self.cconcat(["    ", "    ", "    ", '</a>', "\n"]), self.cconcat(["    ", "    ", '</h1>', "\n"]), self.cconcat(["    ", '</div>', "\n"]), self.cconcat(["    ", '<div class="main-sumamry row">', "\n"]), self.cconcat(["    ", "    ", '<p>', "\n"]), self.cconcat(["    ", "    ", "    ", "{{headline}}", "\n"]), self.cconcat(["    ", "    ", '</p>', "\n"]), self.cconcat(["    ", "    ", "{{#if source}}", "\n"]), self.cconcat(["    ", "    ", "    ", '<a href="{{#if adchoices_url}}{{adchoices_url}}{{else}}https://info.yahoo.com/privacy/au/yahoo/relevantads.html{{/if}}" target="_blank">', "\n"]), self.cconcat(["    ", "    ", "    ", "    ", '<span>Sponsored by {{source}}</span>', "\n"]), self.cconcat(["    ", "    ", "    ", '</a>', "\n"]), self.cconcat(["    ", "    ", "{{/if}}"]), "\n", self.cconcat(["    ", '</div>', "\n"]), self.cconcat(['</div>'])])





class Config (String):
	### produce javascript file and write to destination
	def js (self, tabs):
		### confirm if file has not been created
		if not hasattr(self, 'js_file'):
			### if file has no instance within class create file
			self.js_file = File(name = self.cconcat([self.partner, ".", "gemini"]), ext = "js", temporary = False, filepath = self.filepath)
			self.js_file.write(self.__js__(tabs))
			self.js_file.close()
		### return file instance
		return self.js_file
	def json (self):
		if not hasattr(self, 'json_file'):
			### if file has no instance within class create file
			self.json_file = File(name = self.cconcat([self.partner, ".", "gemini"]), ext = "json", temporary = False, filepath = self.filepath)
			self.json_file.write(self.__json__())
			self.json_file.close()
		### return file instance
		return self.json_file
	### produce entire config.js file string
	def create (self, **kwargs):
		file_type = kwargs.pop("file", "js")
		tabs = kwargs.pop("tabs", "")
		### return formatted container 
		if file_type is "js":
			return self.js(tabs)
		elif file_type is "json":
			return self.json()
		elif file_type is "both":
			return {'js': self.js(tabs), 'json': self.json()}
	def __comments__ (self):
		return self.cconcat(["/*", "\n", "\n", "************************", "\n", "***", " ", "config file help", " ", "***", "\n", "************************", "\n", "\n", "containers: this section refers to the number of ad templates to be included for this partner. each javascript object refers to a seperate template. the same template can be include multiple times.", "\n", "\n", "target: this refers to the parent container for the ad to be sent to. when assigning this section, you should aim to get your selector as close as you can to the desired location for the ad.", "\n", "\n", "selector: this is the element that gemini will try to match against within the target container. these should be direct child of the target container.", "\n", "\n", "template: refers to the HTML snippet that is assigned / associated with this particular placement. the template path provided here will be inserted into the taget container and repeated x number of times after the first position set. templates can be shared across multiple placements.", "\n", "\n", "first: represents the initial position within the target that ads will commence.", "\n", "\n", "interval: this is the index that tells gemini when the next ad unit should occur within the target container. this index pattern is counted after the first ad position and will occur until no more ads are available to be served.", "\n", "\n", "************************", "\n", "******* ", "end help", " *******", "\n", "************************", "\n", "\n", "*/" "\n\n"]) 
	### produce formatted string for config.js entire container js array
	def __container__ (self, tabs = ""):
		### return formatted string for javascript object with key of container and value of array with nested objects
		return self.cconcat([tabs, "containers: [", "\n", self.__templates__(tabs), "\n", tabs, "]"])
	### produce formatted string for config.js single or multiple objects formatted for js array
	def __templates__ (self, tabs = ""):
		templates_string = ""
		templates_len = len(self.templates)
		### iterate over the length of template containers to be concatenated
		for i in range(0, templates_len):
			### return container string generated from PX container method
			templates_string = self.cconcat([templates_string, self.templates[i].container(self.cconcat([tabs, "    "]))])
			### confirm if the iteration count is not the length of the list range
			if ((i + 1) is not templates_len):
				### if iteration is not the length format string to include a comma denoting a following item and breakline
				templates_string = self.cconcat([templates_string, ",", "\n"])
		### return concatenated singular or multiple formatted array type list of javascript objects
		return templates_string
	### produce formatted string for config.js entire container js array
	def __syndication__ (self, tabs = ""):
		### return concatenated string forming the id of the partner
		return self.cconcat([tabs, "syndication: {", "\n", self.cconcat([tabs, "    "]), "section: ", self.cconcat(['"', self.syndication, '"']), "\n", tabs, "}"])
	### produce completely formatted javascript file for use within browser
	def __js__ (self, tabs = ""):
		### return complete string for js file
		return self.cconcat([self.__comments__(), "\n", tabs, "(function () {", "\n", self.cconcat([tabs, "    "]), "new GeminiNative({", "\n", self.__container__(self.cconcat([tabs, "    ", "    "])), ",", "\n", self.__syndication__(self.cconcat([tabs, "    ", "    "])), "\n", self.cconcat([tabs, "    "]), "});", "\n", tabs, "})();"])
	def __json__ (self):
		templates = []
		for i in range(0, len(self.templates)):
			templates.append(self.templates[i].__self__())
		return json.dumps({'partner': self.partner, 'website': self.website, 'syndication': self.syndication, 'templates': templates})
	### constructor 
	def __init__ (self, **kwargs):
		self.partner = kwargs.pop("partner", "example")
		self.filepath = kwargs.pop("filepath", __filepath__)
		self.website = kwargs.pop("website", "https://www.example.com/")
		self.templates = kwargs.pop("templates", [CX()])
		self.syndication = kwargs.pop("syndication", "1234567")





class HX (String):
	### create all required files
	def all (self):
		### check selenium
		self.__start__()
		### create all required values
		self.__module__()
		self.__path__()
		self.__target__()
		self.__selector__()
		self.__first__()
		self.__interval__()
		self.__html__()
		### return formatted dict
		return self.container()
	### create and return dictionary from self
	def container (self):
		### return dict
		return self.__dict__
	### create the string required for defining the name of the module for the produced template
	def __module__ (self):
		### return the response string
		self.module = Set(request = self.concat("the", self.tag("module name"), "for this template"), response = self.concat("this template module")).open()['response']
	### create the URL string required for redirecting the browser to the correct location where the template HTML is situated
	def __path__ (self):
		### confirm if the template to be created is to be placed on the same destination as the base url
		if not Request(prompt = self.concat("does this module", self.cconcat(["(", self.module,")"]), "sit on the same page as the base url?")).open():
			### generate the subpath for the main url
			self.subpath = Set(request = self.concat("the sub path for", self.tag(self.path)), response = self.concat("for the sub path")).open()['response']
			### confirm if the subpath was defined
			if self.subpath:
				### confirm if the base url has a trailing "/"
				if re.compile(r"^.+\/$").match(self.path):
					### set the string to omit the trailing "/"
					self.path = self.path[:-1]
				### confirm if the sub path leads with a "/"
				if re.compile(r"^\/.+").match(self.subpath):
					### set the string to omit the leading "/"
					self.subpath = self.subpath[1:]
				### set the base url path for this template to be the include the sub path, joined by a "/"
				self.path = self.cconcat([self.path, self.subpath], "/")
				### redirect to new page
				self.browser.open(self.path)
	### create the string required to select the parent container for the ad units
	def __target__ (self):
		### return the css selector string
		self.target = Set(request = self.concat("the", self.tag("css selector"), "for the template's parent container"), response = self.concat("the parent css selector")).open()['response']	
		### confirm that the css selector can be found on the provided page
		if self.__element__("target", self.target, "html"):

			self.__highlight__(self.target, True)

			### confirm that the right HTML was located
			if not Request(prompt = "was the correct HTML element selected?").open():
				### recall function
				self.__target__()
		### if selenium failed to select find HTML on provided page
		else:
			### request to redefine the css selector and attempt to locate again
			if Request(prompt = "unable to find element. try again?").open():
				### recall function
				self.__target__()
	### create the string required to select the child container for the ad unit to emulate
	def __selector__ (self):
		### return the css selector string
		self.selector = Set(request = self.concat("the", self.tag("css selector"), "for the HTML to be copied"), response = self.concat("the", self.tag("HTML css selector"))).open()['response']
		### confirm that the parent selector was defined
		if self.target:
			### confirm that the css selector can be found on the provided page
			if self.__element__("selector", self.concat(self.target, self.selector), "html"):

				self.__highlight__(self.concat(self.target, self.selector))
				### confirm that the right HTML was located
				if not Request(prompt = "was the correct HTML element selected?").open():
					### recall function
					self.__selector__()
			### if selenium failed to select find HTML on provided page
			else:
				### request to redefine the css selector and attempt to locate again
				if Request(prompt = "unable to find element. try again?").open():
					### recall function
					self.__selector__()
	### create the string required to set the starting position of the ad template
	def __first__ (self):
		### return the starting string
		self.first = Set(request = self.concat("the", self.tag("starting position"), "for this template"), response = self.concat("the ad starting position")).open()['response']
	### create the string required to set the repetition position of the ad template
	def __interval__ (self):
		### return the interval string
		self.interval = Set(request = self.concat("the", self.tag("interval position"), "at which this template will repeat"), response = self.concat("the ad repetition interval")).open()['response']	
	### confirm that selenium instance has been started
	def __start__ (self):
		### call start function
		self.browser.start()
	### create the selenium html instance for selected element
	def __element__ (self, attribute = None, selector = None, html_attr = None):
		### confirm that a selector was provided as an argument
		if selector:
			### attempt to locate instance in self
			if hasattr(self, attribute):
				### confirm that attribute was provided for the HTML to be assigned to
				if html_attr:
					### set selenium HTML to retreived value from browser
					setattr(self, html_attr, self.browser.find(selector = selector))
					### return response for handler
					return getattr(self, html_attr)
	### highlight the selector if found on the page
	def __highlight__ (self, selector = None, clear = None):
		### confirm that CSS selector was provided
		if selector:
			### format supplied selector to javascript query selector method
			selector = self.cconcat(["document.querySelector", "(", '"', selector, '"',");"])

			if not clear:
				clear = ""
			else:
				clear = "if (!e.clientHeight) { var cf = document.createElement('div'); cf.style.clear = 'both'; e.appendChild(cf); }"

			### concatenate selector with javascript and include 
			selector = self.concat("var", "e", "=", selector, clear, "e.style.border = '2px solid #9ecaed'; e.style.boxShadow = '0 0 10px #9ecaed';")

			self.browser.exe(selector)

	### extract HTML code from selected element
	def __html__ (self, html_selection = "innerHTML"):
		### confirm that HTML instance exists
		if self.html:
			### retrieve attribute from selenium index and clean contents with selenium
			self.html = Soup(html = self.html.get_attribute(html_selection)).create()
	### constructor 
	def __init__ (self, **kwargs):
		self.name = kwargs.pop("name", "example")
		self.path = kwargs.pop("path", "https://www.example.com/")
		self.browser = kwargs.pop("browser", Browser())
		self.module = None
		self.target = None
		self.selector = None
		self.first = None
		self.interval = None
		self.html = None





class HTML (String):
	### produce html file and write to destination
	def handlebars (self, tabs = ""):
		### confirm if file has not been created
		if not hasattr(self, 'handlebars_file'):
			### if file has no instance within class create file
			self.handlebars_file = File(name = self.module, ext = "handlebars", temporary = False, filepath = self.filepath)
			self.handlebars_file.write(self.__code__(tabs))
			self.handlebars_file.close()
		### return file instance
		return self.handlebars_file
	### produce handlebars file and write to destination
	def create (self, **kwargs):
		file_type = kwargs.pop("file", "handlebars")
		tabs = kwargs.pop("tabs", "")
		### return formatted container 
		if file_type is "handlebars":
			return self.handlebars(tabs)
	### produce formatting hashes around titles
	def __formatter__ (self, string):
		return "".join(list('#' * len(string)))		
	### produce entire formatted HTML code for handlebars file including comments and markup
	def __code__ (self, tabs = ""):
		### return comments and html for inclusion within handlebars file
		return self.cconcat([self.__comments__(tabs), "\n", self.__html__()])
	### produce formatted comments for handlebars file
	def __comments__ (self, tabs = ""):
		### return formatted strings for inclusion within uncompiled handlebars file for all of the basic required fields
		return self.cconcat(["{{!--", "\n", "\n", self.__partner__(), "\n", "\n", self.__path__(), "\n", "\n", "### full list: https://git.corp.yahoo.com/aunz-webdev/gemini-native-templates ###", "\n", "### text within {{!-- --}} will not be included in compiled template ###", "\n", "\n", tabs, self.__clickurl__(), "\n", "\n", tabs, self.__headline__(), "\n", "\n", tabs, self.__image__(), "\n", "\n", tabs, self.__summary__(), "\n", "\n", tabs, self.__sponsored__(), "\n", "\n", "--}}", "\n", "\n"])
	### produce formatted HTML code for handlebars file
	def __html__ (self):
		### return formatted HTML for inclusion within uncompiled handlebars file
		return self.cconcat(["<!-- Yahoo! Gemini -->", "\n", self.html, "\n", "\n"])
	### produce formatted clickurl comment for handlebars file
	def __clickurl__ (self, tabs = ""):
		title_str = self.cconcat(["###", " ", "click out / exit url", " ", "###"])
		### return formatted string for inclusion within uncompiled handlebars file
		return self.cconcat([tabs, self.cconcat([tabs, self.__formatter__(title_str), "\n"]), self.cconcat([tabs, title_str, "\n"]), self.cconcat([tabs, self.__formatter__(title_str), "\n", "\n"]), self.cconcat([tabs, "{{clickUrl}}"])])
	### produce formatted headline comment for handlebars file
	def __headline__ (self, tabs = ""):
		title_str = self.cconcat(["###", " ", "primary ad headline", " ", "###"])
		### return formatted string for inclusion within uncompiled handlebars file
		return self.cconcat([tabs, self.cconcat([tabs, self.__formatter__(title_str), "\n"]), self.cconcat([tabs, title_str, "\n"]), self.cconcat([tabs, self.__formatter__(title_str), "\n", "\n"]), self.cconcat([tabs, "{{headline}}"])])
	### produce formatted image comment for handlebars file
	def __image__ (self, tabs = ""):
		title_str = self.cconcat(["###", " ",  "primary ad image", " ", "###"])
		### return formatted string for inclusion within uncompiled handlebars file
		return self.cconcat([tabs, self.cconcat([tabs, self.__formatter__(title_str), "\n"]), self.cconcat([tabs, title_str, "\n"]), self.cconcat([tabs, self.__formatter__(title_str), "\n", "\n"]), self.cconcat([tabs, "{{> gemini/image }}"])])
	### produce formatted name comment for handlebars file
	def __partner__ (self, tabs = ""):
		title_str = self.cconcat(["###", " ", "template created for partner:",  " ", self.partner, " ", "###"])
		### return formatted string for inclusion within uncompiled handlebars file
		return self.cconcat([tabs, self.cconcat([tabs, self.__formatter__(title_str), "\n"]), self.cconcat([tabs, title_str, "\n"]), self.cconcat([tabs, self.__formatter__(title_str)])])
	### produce formatted path comment for handlebars file
	def __path__ (self, tabs = ""):
		title_str = self.cconcat(["###", " ", "template website url path:",  " ", self.path, " ", "###"])
		### return formatted string for inclusion within uncompiled handlebars file
		return self.cconcat([tabs, self.cconcat([tabs, self.__formatter__(title_str), "\n"]), self.cconcat([tabs, title_str, "\n"]), self.cconcat([tabs, self.__formatter__(title_str)])])
	### produce formatted summary comment for handlebars file
	def __summary__ (self, tabs = ""):
		title_str = self.cconcat(["###", " ", "ad content summary", " ", "###"])
		### return formatted string for inclusion within uncompiled handlebars file
		return self.cconcat([tabs, self.cconcat([tabs, self.cconcat([tabs, self.__formatter__(title_str), "\n"]), self.cconcat([tabs, title_str, "\n"]), self.cconcat([tabs, self.__formatter__(title_str), "\n", "\n"])]), self.cconcat([tabs, "{{#if summary}}", "\n"]), self.cconcat([tabs, "    ", "{{summary}}", "\n"]), self.cconcat(["{{/if}}"])])
	### produce formatted sponsored by comment for handlebars file
	def __sponsored__ (self, tabs = ""):
		title_str = self.cconcat(["###", " ", "ad sponsored by", " ", "###"])
		### return formatted string for inclusion within uncompiled handlebars file
		return self.cconcat([self.cconcat([tabs, self.cconcat([tabs, self.__formatter__(title_str), "\n"]), self.cconcat([tabs, title_str, "\n"]), self.cconcat([tabs, self.__formatter__(title_str), "\n", "\n"]), tabs, "{{> gemini/sponsored color='#999' size='13px' }}", "\n"])])
	### constructor
	def __init__ (self, **kwargs):		
		self.module = kwargs.pop("module", "instream")
		self.partner = kwargs.pop("partner", "loremipsum")
		self.path = kwargs.pop("path", "https://www.loremipsum.com/home")
		self.filepath =  kwargs.pop("filepath", __filepath__)
		self.html = Soup(html = kwargs.pop("html", self.cconcat([self.cconcat(['<div id="gemini-ad-example" class="gemini-example-ad">', "\n"]), self.cconcat(["    ", '<div class="main-image row">', "\n"]), self.cconcat(["    ", "    ", '<figure>', "\n"]), self.cconcat(["    ", "    ", "    ", '<a href="{{headline}}" target="_blank">', "\n"]), self.cconcat(["    ", "    ", "    ", "    ", '<img src="{{> gemini/image }}" alt="{{headline}}">', "\n"]), self.cconcat(["    ", "    ", "    ", '</a>', "\n"]), self.cconcat(["    ", "    ", '</figure>', "\n"]), self.cconcat(["    ", '</div>', "\n"]), self.cconcat(["    ", '<div class="main-headline row">', "\n"]), self.cconcat(["    ", "    ", '<h1>', "\n"]), self.cconcat(["    ", "    ", "    ", '<a href="{{headline}}" target="_blank">', "\n"]), self.cconcat(["    ", "    ", "    ", "    ", '{{headline}}', "\n"]), self.cconcat(["    ", "    ", "    ", '</a>', "\n"]), self.cconcat(["    ", "    ", '</h1>', "\n"]), self.cconcat(["    ", '</div>', "\n"]), self.cconcat(["    ", '<div class="main-sumamry row">', "\n"]), self.cconcat(["    ", "    ", '<p>', "\n"]), self.cconcat(["    ", "    ", "    ", "{{headline}}", "\n"]), self.cconcat(["    ", "    ", '</p>', "\n"]), self.cconcat(["    ", "    ", "{{#if source}}", "\n"]), self.cconcat(["    ", "    ", "    ", '<a href="{{adchoices_url}}" target="_blank">', "\n"]), self.cconcat(["    ", "    ", "    ", "    ", '<span>Sponsored by {{source}}</span>', "\n"]), self.cconcat(["    ", "    ", "    ", '</a>', "\n"]), self.cconcat(["    ", "    ", "{{/if}}"]), "\n", self.cconcat(["    ", '</div>', "\n"]), self.cconcat(['</div>'])]))).create()






class Partner:
	### create all files
	def create (self):
		### produce the html files for the different ad templates
		self.__templates__()
		### produce the json and js files for the entire ad partner
		self.__config__()
	### create instances of the template strings and config objects
	def template (self, **kwargs):
		### append the name of the partner to the function arguments
		kwargs.update({'partner': self.name})
		### append the filepath of the parther to the function arguments
		kwargs.update({'filepath': self.filepath})
		### append the html to the list of files to produced
		self.html_context.append(HTML(**kwargs))
		#### append the config extension to the list of files to produce
		self.javascript_context.append(CX(**kwargs))
	### generate the config files for the new partner
	def __config__ (self):
		### create empty list for holding only the context extensions
		Config(partner = self.name, website = self.website, templates = self.javascript_context, syndication = self.syndication, filepath = self.filepath).create(file = "both")
	### generate the html/handlebars templates for the supplied ad positions
	def __templates__ (self):
		### iterate over length of html templates (HTML classes)
		for i in range(0, len(self.html_context)):
			### create handlebars files from supplied HTML class
			self.html_context[i].create(file = "handlebars")	
	### constructor
	def __init__ (self, **kwargs):
		self.name = kwargs.pop("name", "dee")
		self.filepath = kwargs.pop("filepath", __filepath__)
		self.website = kwargs.pop("website", "https://dee.robot")
		self.syndication = kwargs.pop("syndication", "0111001001101111011000100110111101110100")
		self.html_context = []
		self.javascript_context = []





class AI (String):
	ARG = r"^(?:[\.\-])*.{1}"
	AUTO = r"^auto(mated)?$"
	EDIT = r"^edit$"
	### main process handler
	def main (self):
		### attempt to process input context
		return self.__path__()
	### process argument string(s)
	def __path__ (self):
		### confirm that system arguments were supplied
		if not bool(self.actions):
			### if system arguments missing setup process to run as normal
			return self.__manual__()
		### should system arguments be found 			
		### attempt to match the first argument instance
		elif re.compile(self.ARG).match(self.actions[0]):
			### attempt to match automatically setup expression
			if re.compile(self.AUTO).match(self.actions[0]):
				### run program with automated setup
				return self.__automatic__(self.actions[1:])
		### failed to match with expression list
		### run program with BIOS setup
		return self.__manual__()
	### process automated start
	def __automatic__ (self, actions):
		### confirm that system arguments container an index
		if bool(actions):
			### create selenium instance
			B = Browser()
			### initialise selenium browser
			B.start()
			### iterate over indexes within system arguments
			for i in range(0, len(actions)):
				### attempt to convert json argument to python dictionary
				config = JSON(actions[i]).fetch()
				### confirm that JSON class returned dictionary instance
				if bool(config):
					### create Partner class instance for associated dictionary
					P = Partner(name = config['name'], website = config['website'], syndication = config['syndication'], filepath = Folder(name = config['name']).create())					
					
					print Responder().response(self.concat("setting up Gemini partner:", P.name))	
				
					### confirm that the supplied dictionary from json contained a list of templates to be constructed
					if bool(config['templates']):	
						### iterate over dictionaries within list
						for k in range(0, len(config['templates'])):
							### set template path to be the website of selenium browser
							B.website = config['templates'][k]['path']
							### open the provided url
							B.open()
							### attempt to find the HTML on the page
							config['templates'][k]['html'] = B.find(selector = self.concat(config['templates'][k]['target'], config['templates'][k]['selector']))
							### confirm that selenium instance returned code
							if bool(config['templates'][k]['html']):
								print Responder().response(self.concat("HTML template created:", config['templates'][k]['module']))	
								### assign innerHTML to the template constructor
								config['templates'][k]['html'] = config['templates'][k]['html'].get_attribute("innerHTML")
								### create config class
								P.template(**config['templates'][k])
							### HANDLER FOR ISSUE GETTING HTML
							else:
								print Responder().response(self.concat("cannot create HTML template:", config['templates'][k]['module']))	
								#print self.responder.response(self.concat("cannot create HTML template:", self.get({'str':self.tag(config['templates'][k]['module']),'attr':{'weight':'bold'}})))
						### produce status message for partner creation
						self.__details__(P)
						### produce all files
						P.create()
	### process manual start
	def __manual__ (self):
		### initialise selenium browser
		self.browser.start()
		### setup the partner
		self.__setup__()
	### main manual setup handler
	def __setup__ (self):
		### initialise partner class
		self.__partner__()
	### initialise partner class instance
	def __partner__ (self):
		### initialise partner class
		self.partner = Partner()
		### attempt to set the name of the partner being initialised
		self.__name__()
	### create the partner name for manual setup
	def __name__ (self):
		### prompt user to set the gemini partners name
		self.partner.name = Set(request = self.concat("the", self.tag("Gemini partner's name")), response = self.concat("the partner's name")).open()['response']
		### confirm that named response was sent
		if self.partner.name:
			### print newline
			print ""
			### proceed to set up gemini syndication id
			self.__syndication__()
	### create the partner id for manual setup
	def __syndication__ (self):
		### prompt user to set the gemini partners id
		self.partner.syndication = Set(request = self.concat(self.cconcat([self.partner.name, "'s"]), self.tag("Gemini ID")), response = self.concat(self.cconcat([self.partner.name, "'s"]), "Gemini ID")).open()['response']
		### confirm that id response was sent
		if self.partner.syndication:
			### print newline
			print ""
			### proceed to selenium initialisation
			self.__website__()
	### create base website to open selenium page
	def __website__ (self):
		### prompt user to set the gemini partners website address for selenium to open
		self.partner.website = Set(request = self.concat("the", self.tag("website address"), "for", self.partner.name), response = self.concat(self.cconcat([self.partner.name, "'s"]), "website address")).open()['response']
		### confirm that website response was sent
		if self.partner.website:
			### attempt to open selenium site
			self.browser.open(self.partner.website)
			### print newline
			print ""
			### proceed to set filepath
			self.__filepath__()
	### create filepath for local file storage
	def __filepath__ (self):
		### confirm whether user wishes to change from default path for file storage
		if not Request(prompt = self.concat("use the", self.tag("default name"), "for the storage folder", self.cconcat(["(", self.partner.name, ")", "?"]))).open():
			### prompt user to update the file path on their local system
			self.partner.filepath = Set(request = self.concat("the", self.tag("folder name"), "for file storage"), response = self.concat("the storage folder")).open()['response']
		### if not altered
		else:
			### set file path to be based on partner name
			self.partner.filepath = self.partner.name
		### create new folder if none exists or create timestamped folder 
		self.partner.filepath = Folder(name = self.partner.filepath).create()
		### print newline
		print ""
		### proceed to template setup
		self.__template__()
	### create templates for the partner site
	def __template__ (self):
		### create entire template
		self.partner.template(**HX(name = self.partner.name, path = self.partner.website, browser = self.browser).all())
		### print newline
		print ""
		### confirm if user wishes to create another template for the current partner
		if Request(prompt = self.concat("create another native template for", self.cconcat([self.partner.name, "?"]))).open():
			### print newline
			print ""
			### recall function and create new template
			self.__template__()
		### if user chose to not continue making templates
		else:
			### print newline
			print ""
			### proceed to create partner
			self.__create__()
	### produce all required files for created partner
	def __create__ (self):
		### finalise creation of partner files
		self.partner.create()

		self.__details__(self.partner)

		### confirm that user wishes to create another partner
		if Request(prompt = "create another partner?").open():
			### setup new partner file
			self.__setup__()
		else:
			print "\n\n"
			print self.get({'str':'{{PROGRAM COMPLETE}}','attr':{'color':'green'}})
			print "\n\n"

	def __details__ (self, partner):

		print "\n"
		print "Yahoo! Gemini partner created"
		print "-----------------------------"
		print "partner file name:", partner.name
		print "syndication ident:", partner.syndication
		print "templates created:", str(len(partner.html_context))
		print "\n\n"

	### constructor
	def __init__ (self, name = "dee", actions = sys.argv[1:]):
		self.responder = Responder(name = name)
		self.actions = actions
		self.partner = None
		self.browser = Browser()





class Browser (String):
	### find the HTML request on the opened webpage
	def find (self, **kwargs):
		### attempt to run the provided JavaScript method and CSS selector to locate HTML on the page
		try:
			### return the selenium instance of the located HTML
			return self.webdriver.execute_script(self.concat("return", self.cconcat([kwargs.pop("method", "document.querySelector"),"(", '"', kwargs.pop("selector", "body"), '"', ")", ";"])))
		### handle runtime error
		except:
			### return False for error handling
			return False
	### run flexible script from class inherited
	def exe (self, script):
		self.webdriver.execute_script(script)
	### open the provided webpage within selenium
	def open (self, website = None):
		### confirm that website argument was provided
		if website:
			### set self instance of website to argument
			self.website = website
		### confirm that self has website instance
		if self.website:
			### create instance of page within selenium
			self.webdriver.get(self.website)
	### initialise selenium browser
	def start (self):
		if not self.initialised:
			### create selenium instance
			self.webdriver = self.webdriver()
			### set boolean to prevent same instance restart
			self.initialised = True
	### exit selenium
	def quit (self):
		### close selenium instance
		self.webdriver.quit()
	### constructor
	def __init__ (self, website = None):
		self.website = website
		self.webdriver = WEBDRIVER.Chrome
		self.initialised = False




class Soup (String):
	### create the formatted and prettified code string
	def create (self):
		### edit the anchor tags
		self.__anchors__()
		### beautiful the HTML string
		self.__prettify__()
		### return indented HTML string provided from beautify
		return self.__indent__()
	### set all of the anchor tags to include macros
	def __anchors__ (self):
		### iterate over all available anchor tags and substitute values
		for anchor_tag in self.soup.select('a[href]'):
			anchor_tag["href"] = "{{clickUrl}}"
			anchor_tag["title"] = "{{headline}}"
			anchor_tag["target"] = "_blank"
	### beautify HTML string with BS4 formatting
	def __prettify__ (self):
		### use beautiful soup to seperate captured HTML into new lines
		self.prettify = self.soup.prettify()
		### return prettified string
		return self.prettify
	### encode or decode string
	def __stringcode__ (self, string):
		### confirm if string type is unicode
		if type(string) is unicode:
			### replace string components with ignorecase
			string = string.encode('ascii','ignore')
		### return string of type string
		return string
	### format prettified HTML string to include further four space indentation
	def __indent__ (self, indentation = "    "):
		### string to contain reformatted and reindented HTML
		self.unicodeHTML = ""
		### list of strings seperated by lines from bs4 prettified code
		self.splitlines = self.prettify.splitlines()
		### iterate over the length of the potential splitlines
		for i in range(0, len(self.splitlines)):
			### attempt to find strings that lead with any number of whitespace
			regexp = re.compile(r'^\s+').search(self.splitlines[i])	
			### confirm that regexp pattern was found
			if regexp is not None:
				### convert unicode string instance to normal string
				self.splitlines[i] = self.__stringcode__(self.splitlines[i])
				### set the split line string to the newly formatted string; replacing the leading space set by BS4 to indented tabs; also splitlines string starts from regexp capture group (leading whitespace)
				self.splitlines[i] = self.cconcat(["".join(list(indentation * len(regexp.group(0)))), self.splitlines[i][len(regexp.group(0)):]])
			### set indented string to include existing string as well as line string whether it was modified or not
			self.unicodeHTML = self.cconcat([self.unicodeHTML, self.splitlines[i]])
			### confirm that the iteration index is not the length of the list
			if (i + 1) is not len(self.splitlines):
				### add new line to the indented string
				self.unicodeHTML = self.cconcat([self.unicodeHTML, "\n"])
		### return new formatted string with indentation
		return self.unicodeHTML
	### constructor
	def __init__ (self, **kwargs):
		self.html = kwargs.pop("html", '<div><section><figure><img src="img-source.file"><figcaption><p>hello world</p></figcaption></figure></section></div>')
		self.soup = BS4.BeautifulSoup(self.html, "html.parser")





class Pips (String):
	### sudo remove all pip packages associated with program and pip
	### do not run this unless you want to actually remove pip itself and these packages
	def uninstall (self):
		### confirm that pip main is still available
		if self.__core__():
			### iterate over list of pip packages
			for i in range(0, len(self.pips)):
				### uninstall pip item as sudo with -H 
				self.__uninstall__(self.pips[i])
			### uninstall pip main core
			self.__uninstall__()
	### suo install pip package manager and pip dependencies
	def install (self):
		### confirm that pip main is installed
		if self.__core__():
			### iterate over list of pip packages
			for i in range(0, len(self.pips)):
				### install pip item
				self.__package__(self.pips[i])
		### confirm that all items including pip main was installed
		return self.__installed__()
	### handler for confirming that pip main or pip items are available
	def __installed__ (self):
		### confirm that pip main is or is not installed
		if not self.__isins__():
			### if not installed return False for error handler
			return False
		### if pip main in installed on system
		else:
			### iterate over list of pip packages
			for i in range(0, len(self.pips)):
				### confirm that pip package item is not installed
				if not self.__isins__(self.pips[i]):
					### return False for error handler
					return False
		### return True if BOTH pip core and all pip packages are available
		return True
	### check whether pip core or pip package is on system
	def __isins__ (self, package = None):
		### confirm that pip package dictionary was not supplied
		if not package:
			### check whether pip core is installed
			return self.__main__()
		### if pip package dictionary was supplied
		else:
			### check whether pip package item can be imported as module
			return self.__pip__(package)
	### installer for pip main
	def __core__ (self):
		### confirm that pip is not installed on the main system
		if not self.__isins__():
			### attempt to fetch pip main installer file from HTTP destination
			self.pip_core = HTTPResource("https://bootstrap.pypa.io/get-pip.py").fetch()
			### confirm if pip main installer file was retrieved from web resource
			if self.pip_core:
				### create new file instance as python file
				self.pip_file =  File(name = "get-pip", ext = "py", temporary = False)
				### write pip contents to new python file
				self.pip_file.write(self.pip_core)
				### close python file for use within subprocess
				self.pip_file.close()
				### attempt to run and install pip main
				if Command(command = [String().concat("sudo", "python", self.pip_file.file.name)], shell = True).process():
					### remove temporary file if installed correctly
					self.pip_file.remove()
					### return True for handler
					return True
			### return False if core failed to download or install
			return False
		### return True if pip core is instaled
		return True
	### installer for pip package from pip
	def __package__ (self, package):
		### install pip package using -H flag
		Command(command = [self.concat("sudo", "-H", "pip", "install", package['pip'])], shell = True).process()
		### return the result of the next import attempt
		return self.__isins__(package)
	### confirm that pip main is installed
	def __main__ (self):
		### return the result of the pip subprocess call
		return Command(command = ["pip"]).process()
	### attempt to assign pip package to import package module and possibly assign to global variable 
	def __pip__ (self, package):
		### attempt to assign to global variable if required
		return self.__global__(package)
	### confirm whether pip packge can be imported as a system module
	def __import__ (self, package = None):
		### attempt to import pip package into system
		try:
			### return imported package if found
			return importlib.import_module(package['import'])
		### handle exception error
		except:
			### return False if package could not be imported (assumed to be uninstalled)
			return False
	### set imported modules to global variables if required as system item
	def __global__ (self, package = None):
		### attempt to import package module into system
		package['sys'] = self.__import__(package)
		### confirm that pip package module was successfully imported into system
		if package['sys']:
			### confirm that package dictionary item has a global variable assignment requirement
			if 'module' in package:
				### confirm that instance name exists as global variable
				if package['module'] in globals():
					### assign imported system package to global window 
					globals()[package['module']] = package['sys']
					### return True for error handling
					return True
			### if package was successfully imported
			else:
				### return True
				return True
		### return False if package could not be imported or assigned to global variable
		return False
	### remove all requirements for this file
	def __uninstall__ (self, package = None):
		### confirm that package was not supplied 
		if not package:
			### uninstall pip main
			return Command(command = [self.concat("sudo", "-H", "pip", "uninstall", "pip"), 'y'], shell = True, stdout = None).process()
		### if pip package dictionary was supplied
		else:
			### uninstall pip package
			return Command(command = [self.concat("sudo", "-H", "pip", "uninstall", package['pip'])], shell = True, stdout = None).process()
	### constructor
	def __init__ (self, **kwargs):
		self.pips = kwargs.pop("pips", [{'name':'selenium', 'pip':'selenium', 'import':'selenium.webdriver', 'resource':'https://pypi.python.org/pypi/selenium', 'module': 'WEBDRIVER'}, {'name':'chromedriver', 'pip':'chromedriver_installer', 'import':'selenium.webdriver.chrome', 'resource':'https://pypi.python.org/pypi/chromedriver_installer'}, {'name':'beautifulsoup', 'pip':'beautifulsoup4', 'import':'bs4', 'resource':'https://pypi.python.org/pypi/bs4/0.0.1', 'module': 'BS4'}])
		self.status = self.__installed__()






class Main (String):

	def start (self):
		Command(command = ["clear"], shell = True, stdout = None).process()

		print self.cconcat([self.system.response(self.concat("starting program:", self.cconcat([self.get({'str':self.tag(str(__file__)),'attr':{'a':'bold'}}), "."]), "file version:", self.cconcat([self.get({'str':self.tag(str(globals()['VERSION'])),'attr':{'a':'bold'}}), "."])))])
		print self.cconcat([self.system.response(self.concat("checking file dependencies:", self.cconcat([self.__pipstatus__(), "."]))), "\n"])

		if not self.pip.status:
			self.safe = False

			print self.system.response(self.concat("program", self.get({'str':self.tag(__file__),'attr':{'a':'bold'}}), "has missing system files."))

			if Request(prompt = "install missing files?").open():
				
				if self.pip.install():
					self.safe = True
					print self.cconcat(["\n", self.system.response("program successfully installed all items."), "\n"])
				else:
					print self.cconcat(["\n", self.system.response("program failed to install all requirements."), "\n"])
			else:
				print self.cconcat(["\n", self.system.response("this program cannot function without these items."), "\n"])
				
		if self.safe:
			print self.cconcat([self.get({'str':'{{PROGRAM START}}','attr':{'a':'green'}}), "\n"])
			AI().main()
		else:
			print self.cconcat([self.get({'str':'{{PROGRAM ABORTED}}','attr':{'a':'red'}}), "\n"])
	### notification status on whether the program can run without installer
	def __pipstatus__ (self):
		### confirm whether pip package manager and dependencies were installed / available
		if self.pip.status:
			### create formatted string confirming that all files were installed
			return self.get({'str':'{{files installed}}','attr':{'a':'bold'}})
		### should package installer be missing
		else:
			### create formatted string confirming that some/all files are missing from system
			return self.get({'str':'{{files missing}}','attr':{'a':'bold'}})
	### constructor
	def __init__ (self):
		self.system = Responder()
		self.pip = Pips()
		self.safe = True
	


if __name__ == '__main__':
	
	Main().start()



