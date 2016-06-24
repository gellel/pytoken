import re

class strstyle:
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
	### return entire formatted string using supplied styling
	def get (self, Object = {}):
		### fetch returned processed object
		return self.__process__(Object)
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
	def __process__ (self, Object = {}):
		### check if Object isn't a default
		if not bool(Object):
			### check if Class was give a constructor dict
			if self.StrObject:
				### use constructor dict
				Object = self.StrObject
			else:
				### use a sample instead
				Object = [{'str':'{{Sample}}', 'attr':{'color':'cyan'}}, {'str':'{{Text}}', 'attr':{'color':'purple'}}]
		### check if Object is either a list or dict
		if type(Object) is list:
			### temp list for holding formatted strings
			strs = []
			### iterate through items to be formatted
			for i in range(0, len(Object)):
				### append formatted strings to temp list
				strs.append(self.__substitute__(Object[i]['str'], Object[i]['attr']))
			### return the complete string with formatting
			return " ".join(strs)
		else:
			### return the complete string with formatting
			return self.__substitute__(Object['str'], Object['attr'])
	### return the type of StrObject supplied
	def __self__ (self):
		return type(self.StrObject)
	### constructor 
	### @StrObject: 
		### [{'str':"{{string}}", 'attr':{'color':'red','style':'underline','weight':'bold'}}] 
		### or
		### {'str':'{{str}}', 'attr':{'color':'red'}}
	def __init__ (self, StrObject = {}):
		self.StrObject = StrObject



class ai (strstyle):

	def response (self, message = "destory all humans!", attr = {}):
		return (self.__name__() + self.seperator) + (" " + self.__msg__(message, attr))

	def __msg__ (self, message = "destroy all humans!", attr = {}):
		return self.get({'str': message, 'attr': attr})

	def __name__ (self):
		return self.get({'str': '{{'+ self.name +'}}', 'attr': self.style})

	def __self__ (self):
		return self

	def __init__ (self, **kwargs):
		self.name = kwargs.pop('name', 'system')
		self.style = kwargs.pop('style', {'style':'underline','weight':'bold'})
		self.seperator = kwargs.pop('seperator', ':')



de = ai(name = "de", style = {'color':'darkcyan', 'weight':'bold'}, seperator = "")


print de.response("hi!")


#print strstyle([{ 'str': '{{Hello}}', 'attr': {'t':'red'} }, {'str': '{{World}}', 'attr': {'t':'blue'}}]).get()

#print strstyle().get()