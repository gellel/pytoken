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
		from selenium import webdriver

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
		if not self.exe:
			try:
				__import__(self.name)
				return True
			except:
				return False
		else:
			cmd = self.name
			if self.cmd:
				cmd = self.cmd
			try:
			    subprocess.check_call(cmd, stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)
			    return True
			except subprocess.CalledProcessError:
			    return False
			except OSError:
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

			if self.packages[i]['installed']:
				print self.__response__(String().concat(String({'str': String(self.packages[i]['name']).tag(), 'attr':{'weight':'bold'}}).get(), "is", String({'str':'{{installed}}','attr':{'color':'green','weight':'bold'}}).get()))

		#print len(self.packages)
		### return reduced array
		return self.packages
		
	### substitute array item to be a dict with a class instance
	def __package__ (self, packages):
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
	def __response__ (self, string):
		return self.system.response(string)
	### constructor
	def __init__ (self, packages = []):
		self.packages = self.__package__(packages)
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





class Partner:

	def __child__ (self):
		self.__dee__("now, should i grab the first child element for your match?")

		if Request().open():

			#print dir(self.CSSPathElement)
			self.CSSChild = self.browser.driver.execute_script('return document.querySelector("'+ self.CSSSelector +' > *:first-child");')

			print self.CSSChild.get_attribute('innerHTML')

		else:
			pass

	def __target__ (self):
		self.__dee__("ok. what is the CSS target?")

		if self.__attr__("CSS selectors", "CSS selector", "CSSSelector"):

			self.CSSPathElement = self.browser.driver.execute_script('return document.querySelector("'+ self.CSSSelector +'");')

			if not self.CSSPathElement:
				self.__dee__("i couldn't find that CSS element")
				self.__dee__("want to try something else?")

				if Request().open():
					return self.__target__()
				else:
					return False

			return True

		else:	
			self.__dee__("i can't target a blank element!")
			return False

	def __fetch__(self):
		self.browser.get(self.URL)

		self.found = self.browser.driver.execute_script('return (function () { return new RegExp("server DNS address could not be found.", "gmi").test(document.body.innerText); }())')

		if self.found:
			self.__dee__(String().concat("hmm. something's {{wrong}} the webpage.."))
			self.__dee__("should we try another url?")

			if Request().open():
				self.browser.quit()
				self.__purl__()
				self.__browser__()
				return self.__fetch__()
			else:
				return False
		else:
			return True

	def __browser__ (self, attempted = False):
		if not attempted:
			self.__dee__(String().concat("ok. i'm gonna try open", String({'str':String(self.URL).tag(),'attr':{'color':'darkcyan'}}).get()))
			self.__sys__(String().concat("** this terminal will wait for", self.deee.__name__(), "to finish loading the page", self.URL))
			self.__sys__("** if this takes too long. try stop the browser from loading and it should resume **")
		try:
			self.browser = Browser(engine = "Chrome")
		except:
			self.browser = None
		if not self.browser:
			self.__sys__("there was an error creating the required item {{web-browser}}", {'color':'red','weight':'bold'})
			return False
		else:
			return True

	def __purl__ (self):
		self.__dee__(String().concat("ok. what is the url for", String({'str':String(self.name).tag(), 'attr':{'weight':'bold'}}).get()) + "?")
		if self.__attr__(String().concat(self.name + "'s",  "website URL"), "URL", "URL"):
			return True
		else:
			self.__dee__("no URL. really? so. how do i get things then?")
			return False

	def __dirs__ (self):
		path = str(self.dirs) + "/" + str(self.name)
		path_string = String({'str':String(str(self.dirs) + "/").tag(),'attr':{'weight':'bold'}}).get() + String({'str':String(str(self.name)).tag(), 'attr':{'color':'blue','weight':'bold'}}).get()

		self.__dee__(String().concat("alright. now, i'm gonna try save stuff here:", path_string))
		self.__dee__("is that cool?")

		if not Request().open():
			self.__dee__("ok. what do you wanna change it to?")
			if self.__attr__("New full folder path", "Folder path", "dirs"):
				return True
			else:
				self.__dee__("cmon! how can i do this without a place to save your things?")
				return False
		else:
			self.dirs = path
			return True

	def __name__ (self):
		self.__dee__("ok. first. what's the name of the gemini partner?")

		if self.__attr__("Gemini partners name", "Partners name", "name"):
			return True
		else:	
			self.__dee__("i need a name! please do it again, with a name!")
			return False

	def __attr__ (self, input_message, confirm_message, attr):
		def __setattribute__ ():
			temp = raw_input(self.__sys__(String().concat("please enter", String({'str':String(str(input_message)).tag(),'attr':{'weight':'bold'}}).get()) + ": ", pprint = False)) or None
			if not temp:
				self.__sys__(String().concat(
					String({'str':String(input_message).tag(),'attr':{'weight':'bold'}}).get(), "cannot be",
					String({'str':String(str(temp)).tag(),'attr':{'weight':'bold'}}).get()))
				if Request(prompt = "try again?").open():
					return __setattribute__()
				else:
					return None
			else:
				return __changeattribute__(temp)

		def __changeattribute__ (temp):
			self.__sys__(String().concat("is", String({'str':String(str(temp)).tag(),'attr':{'weight':'bold'}}).get(), "the correct value for", String({'str':String(confirm_message).tag() + "?",'attr':{'weight':'bold'}}).get()))
			if Request().open():
				setattr(self, attr, temp)
				return self
			else:
				if Request(prompt = "change value?").open():
					return __setattribute__()

		return __setattribute__()
			
	def __rop__ (self, message = "Test", pprint = True):
		if pprint:
			print message
		return message

	def __sys__ (self, message = "", attr = {}, pprint = True):
		return self.__rop__(self.system.response(message, attr), pprint)

	def __dee__ (self, message = "", attr = {}, pprint = True):
		return self.__rop__(self.deee.response(message, attr), pprint)

	def __main__ (self):
		self.__name__()
		self.__dirs__()
		self.__purl__()
		self.__browser__()
		self.__fetch__()
		self.__target__()
		self.__child__()
	
	def __self__ (self):
		return self

	def __init__ (self, dirs = __filepath__, deee = Responder(name = "dee"), system = Responder()):
		self.dirs = dirs
		self.deee = deee
		self.system = system



Partner().__main__()