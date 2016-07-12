### python scripts dependencies
### py selenium browser package
### from selenium import webdriver
#http://selenium-python.readthedocs.io/api.html
import collections
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
	def __format__ (self, _object):
		if type(_object) is dict:
			return _object
		elif type(_object) is list:
			return {'t':_object}
	### constructor
	def __init__ (self, **kwargs):
		self.key = self.__format__(kwargs.pop('key', {'t':["test"]}))
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
					if self.__optional__(self._object[i]):
						### format string
						constructed.append(self.__construct__(self._object[i]))
				### assume other type supplied is a string
				elif not type(self._object[i]) is None:
					constructed.append(self._object[i])
			### return joined string, seperated by whitespace
			return " ".join(constructed)
	### confirm if dict item is to be evaluated
	def __optional__ (self, _object):
		if _object['optional']:
			### generate pseudo random number 
			if random.randrange(0, self._random['optional']) == 0:
				return False
		### if no optional paramater supplied return True
		return True
	### convert dictionary to string 
	def __construct__ (self, _object):
		### return the substring from the supplied dict and key
		_object['formatted'] = self.__lexical__(_object['key'], _object['value'])
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
				if random.randrange(0,  self._random['punctuation']) == 0:

					punct_str = self.__lexical__({'t':["--", "..", "..."]}, 't')
					### include intenation
					_object['formatted'] = String().concat((pause_str + punct_str), _object['formatted'])
				else:
					_object['formatted'] = String().concat(pause_str, _object['formatted'])
			### constructs after sentence
			elif _object['pause'] == 'after':
				### determine if the string should include intenation lines
				if random.randrange(0, self._random['punctuation']) == 0:
					punct_str = self.__lexical__({'t':["--", ",", "..", "..."]}, 't')
					### include intenation
					_object['formatted'] = String().concat(_object['formatted'], (pause_str + punct_str))
				else:
					_object['formatted'] = String().concat(_object['formatted'], pause_str)
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
	def __init__ (self, _object, _random = {'optional':2, 'punctuation': 2}):
		self._object = self.__process__(_object)
		self._random = _random



print "\n"

### gemini partner creation string
Lexicon([
	LX(key = ["hi", "hello", "yo", "hey", "heyheyhey", "what up"], punctuate = ["!","."], optional = True),
	["what's", "what is"],
	"the",
	["name", "title"],
	"of the",
	String({'str':"{{Gemini Partner}}",'attr':{'weight':'bold'}}).get(),
	["we're", "you are", "we are", "you're"],
	LX(key = ["creating", "setting up", "working on", "putting together", "registering"], punctuate = "?")
]).pprint()

### gemini partner name missing string
Lexicon([
	LX(key = ["dude", "man", "hey"], punctuate = "!", optional = True),
	"i",
	LX(key = ["need", "require"], pause = "before"),
	"a",
	["name", "title"],
	"to",
	["begin", "start"],
	"the build process."
]).pprint()

### gemini name entered string
Lexicon([
	LX(key = ["so"], punctuate = ["--", "..", ","], optional = True),
	LX(key = ["your new partner"], punctuate = ",", optional = True),
	"it's",
	["called", "named"],
	"thewhoot.",
	LX(key = ["got it", "gotcha", "no problem", "cool", "neat", "nice", "uh-huh"], punctuate = ".")

]).pprint()


print "\n"

### gemini save path
Lexicon([
	LX(key = ["so", "alright"], pause = 'after', punctuate = ",", optional = True),
	"i'm going to",
	["attempt", "try"],
	"to",
	["save", "store", "commit", "stash", "place"],
	["files", "code", "stuff"],
	"in this",
	LX(key = ["folder", "directory"], punctuate = "."),
	"is that",
	LX(key = ["alright", "ok", "fine", "cool"], punctuate = "?")
]).pprint()

### gemini save not allowed
Lexicon([
	LX(key = ["oops", "sorry", "alright"], pause = "after", punctuate = ["!", "...", "."], optional = True),
	LX(key = ["ok", "fine"], optional = True),
	["where's the", "what's the"],
	["new", "correct", "adjusted", "right"],
	LX(key = ["path", "directory"], punctuate = "?")

]).pprint()

### gemini save missing
Lexicon([
	"i",
	LX(key = ["can't"], pause = "before"),
	["store", "save"],
	["files", "code", "stuff"],
	"in",
	["an empty", "a blank", "a missing"],
	LX(key = ["directory"], punctuate = ["!", ".", "..."])
]).pprint()

### gemini save is ok
Lexicon([
	LX(key = ["alright", "cool"], punctuate = ".", optional = True),
	["check", "visit", "open"],
	"that",
	["folder", "directory"],
	"at the end.",
	"that's where i'll",
	["save", "store", "publish"],
	"everything."
]).pprint()	


print "\n"

### gemini partner website
Lexicon([
	LX(key = ["ok", "cool", "alright"], punctuate = ".", optional = True),
	"what's the URL for",
	"thewhoot?"
]).pprint()

### gemini partner website missing
Lexicon([
	LX(key = ["hmm"], punctuate = "..", optional = True),
	LX(key = ["well"], optional = True),
	LX(key = ["i"], pause = "after", optional = True), 
	"i can't",
	["function", "operate", "work"],
	"without a",
	LX(key = ["website", "webpage"], punctuate = "."),
	LX(key = ["ah well", "too bad"], punctuate = ".", optional = True)
]).pprint()

### gemini website open
Lexicon([
	LX(key = ["ok", "alright"], punctuate = ",", optional = True),
	"i'm going to",
	["attempt", "try"],
	"to",
	["reach", "open", "connect to", "access"],
	"that",
	["website", "webpage"],
	"for you."
]).pprint()


print "\n"

### css selector
Lexicon([
	LX(key = ["so", "right", "alright"], punctuate = [",", ".", "--"], optional = True),
	["what's", "what is"],
	"the CSS selector for the parent container on this",
	LX(key = ["webpage", "website"], punctuate = "?")
]).pprint()

### no selector supplied
Lexicon([
	LX(key = ["gah", "c'mon", "dude", "man"], punctuate = [".", "!"], optional = True),
	"i can't",
	["locate", "find", "fetch", "target", "select"],
	["blank", "missing", "undefined"],
	"HTML",
	LX(key = ["nodes", "elements"], punctuate = ["!", "."]),
	LX(key = ["sorry"], punctuate = [".", "..."], optional = True)

]).pprint()

### checking
Lexicon([
	LX(key = ["ok", "alrig"])
]).pprint()

print "\n"

#key = {}, value = 't', pause = False, pause_at = None, attr = {}, punctuate = "??", optional = False

