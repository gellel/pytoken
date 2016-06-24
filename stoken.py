### dependencies
### $ brew 
### $ pip
### $ brew install python
### $ python get-pip.py
### $ pip install selenium
### $ pip install beautifulsoup4
### $ brew install chromedriver

### py dependencies
### selenium phantombrowser package
from selenium import webdriver
### py psuedo class package
from collections import namedtuple as Object 
### py textwrap class package
import textwrap
### py user class package
import getpass
### py os class package
import os
### py regex
import re

### set localfile path
__filepath__ = os.path.dirname(os.path.realpath('__file__'))

### class for formatting detailed response user strings 
class StringStyle:
	### @params
	### @string: "Stylise me"
	### @attributes: {'color':'colorname', (or) 'weight':'bold', (or) 'style':'underline'}
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
	### return dict
	def get_attr (self):
		return self.attributes
	### return str
	def get_format (self):
		return self.format
	### return str
	def get_string (self):
		return self.string
	### iterate through dict
	### attempt to match against CONSTs
	def format_string (self, string):
		for attribute in self.attributes:
			attr = getattr(self, str.upper(self.attributes[attribute]), None)
			if attr:
				string = attr + string + self.END
		return string
	### constructor
	def __init__ (self, **kwargs):
		self.attributes = kwargs.pop('attributes', {})
		self.string = kwargs.pop('string', '')
		self.format = self.format_string(self.string)
		
### highlight marked up elements (using {{str}}) and format
def formatted_string (string, attributes = {'color':'green'}):
	### @params
	### @string: "example str"
	### @attributes: {'color':'red'} or [{'color':'red'}, {'color':'green'}]
	### match {{ anystring or digit or specialcharacter repeated }}
	reg = "\{\{(?:(?:\w*|\s*)|(?:\d*|[$&+,\:\;\=\?@#\|'<>.^*\(\)%!-\/]))+\}\}"
	### find all matches of regular expression
	extracts = re.findall(reg, string, re.DOTALL)
	### iterate through extractions and apply styling
	for i in range(0, len(extracts)):
		substr = re.sub("{{|}}", "", extracts[i])
		attr = attributes
		### if list is supplied bind attr as i of list items
		if type(attributes) is list:
			attr = attributes[i]
		### replace str to be dict or original and styled text
		extracts[i] = {'original': substr, 'color': StringStyle(string = substr, attributes = attr).get_format()}
	### remove tags for easier match
	string = re.sub("{{|}}", "", string)
	### iterate through extracts and replace the substring with the coloured version
	for i in range(0, len(extracts)):
		string = re.sub(extracts[i]['original'], extracts[i]['color'], string)
	### return formatting string
	return string

### reusable function for building notifying message
def formatted_operator (operator, message = ""):
	### @params
	### @operator: "SYSTEM"
	### @message: "Hello Human!"
	### build out user response
	return concat_strings([formatted_string("{{"+ str.upper(operator) +"}}:", {'style':'underline'}), message])
	
### concatenate multiple strings by a defined seperator value
def concat_strings (strings, seperator = " "):
	### @params
	### @strings: ["example", "string"]
	### @sepeator: "," or " " by default
	string = ""
	### iterate through list of strings
	for i in range(0, len(strings)):
		### if this is the first iteration do not append leading space
		if i == 0:
			string = string + strings[i]
		else:
			string = string + seperator + strings[i]
	### return concate str
	return string

### print multiple lines of text to terminal, automatically wrapping orphans
def print_multiline (string, width = None):
	### @params
	### @string: "Hello world. Multiple line long text"
	### @width: 50 
	### create string list
	string_paragraph = textwrap.fill(string, width)
	### iterate through list or words
	for line in string_paragraph:
		### print line
		print line

### ask user to response in one of two methods or repeat command
def prompt_boolean (confirm = "YES", reject = "NO"):
	### @params
	### @confirm: "YES"
	### @reject: "NO"
	### build a system response string
	### build a formatted string with user options
	### concatenate strings
	string = concat_strings([
		formatted_operator("system", "Please enter either"), 
		formatted_string("{{"+ str.upper(confirm) +"}}/{{"+ str.upper(reject) +"}}: ", {'weight':'bold'})])
	### store user input in variable
	response = raw_input(string) or None
	### if user input is not entered prompt for a re-entry
	if response is None:
		print concat_strings([
			formatted_operator("system", formatted_string("User input was {{empty}}.", {'weight':'bold'})), 
			"Please try again."])
		### recursively call self
		return prompt_boolean(confirm, reject)
	else:
		### convert string to uppercase for easy comparison
		response = str.upper(response)
		### convert string options to uppercase for easy comparison
		confirm = str.upper(confirm)
		reject = str.upper(reject)
		### if user has entered fulltext confirm or shorthand "Y" (Yes)
		if response == confirm or response == "Y":
			return True
		### else if user has entered fulltext reject or shorthand "N" (No)
		elif response == reject or response == "N":
			return False
		### otherwise inform user that input wasn't understood and reprompt
		else:
			### create concate string with user input and the next command
			print concat_strings([
				formatted_operator("system", formatted_string("User input was {{"+ response +"}}.", {'weight':'bold'})), 
				"Command not recognised. Please try again."])
			### recursively call self
			return prompt_boolean(confirm, reject)


def prompt_none ():
	print formatted_operator("system", formatted_string("{{Empty}} input returned. Try again?", {'weight':'bold'}))


### ask the user to enter a URL for the later webrequest
def prompt_partnersite ():
	### notify user as DE to enter the website for the gemini partner
	print formatted_operator("de", formatted_string("Okay! What is the {{Gemini partner's}} website {{URL}}?", {'weight':'bold'}))
	### store the input a variable or None if no input received
	partnersite = raw_input(formatted_operator("system", formatted_string("Please enter the partners website {{URL}}: ", {'weight':'bold'}))) or None
	### send response to confirmation method for response evaluation
	return confirm_partnersite(partnersite)


### evaluates the returned data from function prompt_partnersite
def confirm_partnersite (partnersite):
	if partnersite is None:
		### notify user that their submission wasn't accepted
		prompt_none()
		### prompt users until they confirm or exit
		### if prompt_boolean returns true
		if prompt_boolean():
			### set the response to partnersite to the prompt
			partnersite = prompt_partnersite()
	### format string to include HTTP prefix
	else:
		if not re.match("^https?://", partnersite):
			partnersite = "https://" + partnersite
	### return either None type or string	
	return partnersite


### calls user prompt for partner website
def request_partnersite ():
	return prompt_partnersite()


### ask the user to enter a CSS selector for the extracting the HTML
def prompt_target (partnersite = "the webpage"):
	### notify user as DE to enter the CSS selector
	print formatted_operator("de", formatted_string("What {{HTML Element}} do you want me to grab from {{"+ partnersite +"}}?", {'weight':'bold'}))
	### store the input a variable or None if no input received
	csstarget = raw_input(formatted_operator("system", formatted_string("Please enter a {{CSS selector}}: ", {'weight':'bold'}))) or None
	### send response to confirmation method for response evaluation
	return confirm_target(csstarget, partnersite)

def confirm_target (csstarget, partnersite):
	if csstarget is None:
		### notify user that their submission wasn't accepted
		prompt_none()
		### prompt users until they confirm or exit
		### if prompt_boolean returns true
		if prompt_boolean():
			### set the response to csstarget to the prompt
			csstarget = prompt_target(partnersite)
	### return the CSS selector 
	return csstarget

def request_target (partnersite = "the webpage"):
	return prompt_target(partnersite)


### ask the user to specify a child to emulate or assume the first child element
def prompt_selector ():
	### notify user as DE to enter the optionally enter a selector
	print formatted_operator("de", formatted_string("Should I grab the {{first child}}? Or would you like to specify a {{selector}} yourself?", {'weight':'bold'}))

def request_selector ():
	return prompt_selector()




def open_webdriver ():
	webdriver = webdriver.Chrome()



partnersite = request_partnersite()

if partnersite:
	print formatted_string("{{"+ partnersite +"}}", {'color':'purple'})
	
	css_selector = request_target(partnersite)

	if css_selector:
		print formatted_string("{{"+ css_selector +"}}", {'color':'purple'})

		request_selector()

