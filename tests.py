### python scripts dependencies
### py selenium browser package
##from selenium import webdriver
### py textwrap class package
import textwrap
### py user class package
import getpass
### py system class package
import sys
### py os class package
import os
### py regex
import re

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
	def get (self):
		self.driver.get(self.url)
	### returns the object created from selenium
	def __self__ (self):
		return self.driver
	### constructor
	def __init__ (self, engine = "Chrome"):
		self.driver = getattr(webdriver, engine, "Chrome")()


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
			print self.system.response(String().concat("command", String({'str': String(self.response).tag(), 'attr':{'weight':'bold'}}).get(), "unrecognised"))
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
		try:
			return __import__(self.name)
		except:
			return None
	### constructor
	def __init__ (self, name, source):
		self.name = name
		self.source = source
		self.system = Responder()



class Install:

	def get (self):
		packages = self.__asgn__()

		if not len(packages):
			return True
		else:
			print self.system.response(String().concat(String({'str': String(str(len(packages)) + "/" + str(len(self.packages))).tag(), 'attr':{'color':'red','weight':'bold'}}).get(), "packages are missing"))

			if Request(prompt = "attempt to install missing files?").open():
				pass
			else:
				pass


	def __istl__ (self, package):
		print package

	def __atmp__ (self, package):
		return package.get()

	def __asgn__ (self):
		for i in range(0, len(self.packages)):
			self.packages[i]['installed'] = True if self.__atmp__(self.packages[i]['package']) else False

		return [pckg for pckg in self.packages if not self.packages[i]['installed']]
		

	def __pckg__ (self, packages):
		for i in range(0, len(packages)):
			packages[i] = {'package': Package(name = packages[i]['name'], source = packages[i]['source'])}
		return packages

	def __init__ (self, packages = []):
		self.packages = self.__pckg__(packages)
		self.system = Responder()


Install([
	{'name':'xeasy_install','source':'https://bootstrap.pypa.io/get-pip.py', 'installer': ''}, 
	{'name':'xselenium','source':'https://pypi.python.org/pypi/selenium'}
]).get()