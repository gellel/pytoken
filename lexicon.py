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




partials = {
	'action_notify_self': ["tell me", "notify me", "advise me"],
	'reference_name_location_other': ["elsewhere", "somewhere else", "to another place"]
}
fragments = {
	'action_attempt': ["try", "attempt"],
	'action_attempt_check': ["check", "see", "find out", "test"],
	'action_attempt_confirm_before': ["ok", "alright", "fine", "not a problem", "cool", "all-good"],
	'action_attempt_connect': ["open", "connect", "reach", "render"],
	'action_attempt_start': ["begin", "start"],
	'action_attempt_works': ["works", "processes", "computes"],
	'action_discovery': ["see", "find out", "test"],
	'action_working_creating': ["creating", "setting up", "working on", "putting together", "registering"],
	'action_save': ["store", "save", "commit", "place", "stash", "leave"],
	'action_search': ["search for", "look for", "locate", "find", "poke around for"],
	'action_want_perform': ["want to", "would like to"],
	'action_want_obtain': ["get", "find", "grab", "snatch", "pick up"],
	'reference_correct_decleration': ["correct", "right", "ideal", "desired", "new"],
	'reference_depend': ["need", "require"],
	'reference_name_code': ["code", "stuff", "files"],
	'reference_name_complete': ["ready", "compiled", "finished", "done"],
	'reference_name_directory': ["folder", "directory"],
	'reference_name_empty': ["empty", "blank", "undefined", "nameless"],
	'reference_name_file_single': ["file", "document"],
	'reference_name_file_plural': ["files", "documents"],
	'reference_name_html': ["DOM node", "HTML", "element", "code", "source"],
	'reference_name_html_element': ["node", "element", "container"],
	'reference_name_move': ["move", "place", "store", "relocate"],
	'reference_name_name': ["name", "title"],
	'reference_name_path': ["location", "path"],
	'reference_name_proceedure': ["method", "logic", "action"],
	'reference_name_reference': ["named", "called", "titled"],
	'reference_name_title': ["name", "title"],
	'reference_name_website': ["website", "webpage"],
	'reference_name_inclusive_or': ["we're", "you are", "we are", "you're"]
}
reference = {
	'it_is': ["it is", "it's"],
	'how': ["how is", "how's"],
	'what': ["what is","what's"],
	'when': ["when is", "when's"],
	'who': ["who is", "who's"],
	'i_will': ["i will", "i'll"]
}
end_fragments = {
	'end_action_understood': ["gotcha", "got it", "no problem", "neat", "i like the sound of it", "ok", "sure thing"],
	'end_fragment': ["right"]
}
mid_fragments = {
	'pause': ["uh", "uhh", "um--ah"]
}
start_fragments = {
	'greet': ["hi", "hello", "greetings", "yo", "hey", "heyheyhey", "what up", "what's up"],
	'pause': ["hm", "hmm", "mmm", "hmph", "ahh", "uh", "hmmm", "eeh"],
	'begin_fragment': ["ok", "right", "alright"],
	'follow_fragment': ["nice", "cool", "sure"]
}
punctuation = {
	'no_context': [".", "?", "!"],
	'period_end': ["."],
	'pause_break': ["--", ",", "..", "..."],
	'period_exclaim': [".", "!"],
	'period_trailing': [".", "..", "..."],
	'period_trailing_exclaim': ["!", ".", "..", "..."]
}


# key = {}, value = "test", pause = False, pause_at = None, attr = {}, optional = False)

class Lexicon:


	def get (self):
		return self.__package__()

	def __package__ (self):
		for i in range(0, len(self._object)):
			if type(self._object[i]) is tuple:
				if bool(self._object[i]):
					self._object[i] = self.__encode__(*self._object[i])

		return self.__construct__()

	def __encode__ (self, key = {}, value = "test", pause = False, pause_at = None, attr = {}, punctuate = None, optional = False):
		return {'key':key,'value':value,'pause':pause,'pause_at':pause_at,'punctuate':punctuate,'optional':optional}


	def __lexical__ (self, key, value):
		return key[value][random.randrange(len(key[value]))]

	def __process__ (self, _object):
		_object['formatted'] = self.__lexical__(_object['key'], _object['value'])
		
		if 'tag' in _object:
			if _object['tag']:
				if 'attr' in _object:
					if bool(_object['attr']):
						_object['formatted'] = String({'str':String(_object['formatted']).tag(),'attr':_object['attr']})
		if 'pause' in _object:
			if _object['pause']:

				pause_punctionation = self.__lexical__(punctuation, "pause_break")

				if random.randrange(0, 3) == 0:
					if 'pause_at' in _object:

						pause_string = self.__lexical__(mid_fragments, "pause")

						if _object['pause_at'] == 'before':
							if random.randrange(0, 2) == 0:
								_object['formatted'] = pause_string + pause_punctionation + " " + _object['formatted']
							else:
								_object['formatted'] = pause_string + " " + _object['formatted']

						elif _object['pause_at'] == 'after':
							if random.randrange(0, 2) == 0:
								_object['formatted'] = _object['formatted'] + " " + pause_string + pause_punctionation
							else:
								_object['formatted'] = _object['formatted'] + " " + pause_string

		if 'punctuate' in _object:
			if _object['punctuate']:		
				_object['formatted'] = _object['formatted'] + _object['punctuate']

		return _object['formatted']

	def __optional__ (self, _object):
		if 'optional' in _object:
			if _object['optional']:
				if random.randrange(0, 2) == 0:
					return False

		return True

	def __construct__ (self):
		constructed = []
		for i in range(0, len(self._object)):

			if type(self._object[i]) is dict:
				if self.__optional__(self._object[i]):
					constructed.append(self.__process__(self._object[i]))
			elif type(self._object[i]) is str:
				constructed.append(self._object[i])

		return " ".join(constructed)


	def __init__ (self, _object):
		self._object = _object




print Lexicon([
	(start_fragments, "greet", False, None, {}, Lexicon([(punctuation, "period_trailing_exclaim")]).get(), True),
	(reference, "what", True, "after"), "the", 
	(fragments, "reference_name_title"), "of the", 
	String({'str':"{{Gemini Partner}}",'attr':{'weight':'bold'}}).get(), 
	(fragments, "reference_name_inclusive_or"), 
	(fragments, "action_working_creating", False, None, {}, "?", False) 
]).get()

print Lexicon([
	"i",
	(fragments, "reference_depend", True, "before"),
	"a",
	(fragments, "reference_name_title"),
	"to",
	(fragments, "action_attempt_start"),
	"the buid process.",
	({'frustrated':["gah", "jeez", "bleh", "eesh"]}, "frustrated", False, None, {}, ".", True)
]).get()


#key = {}, value = "test", pause = False, pause_at = None, attr = {}, punctuate = None, optional = False

#print Lexicon(["please", (fragments, "action_save", False, None, {}, ".", False), ()]).get()

#print (fragments, "action_save", False, None, {}, False)


