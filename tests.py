import re

class strstyle:
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
	REG = "\{\{(?:(?:\w*|\s*)|(?:\d*|[$&+,\:\;\=\?@#\|'<>.^*\(\)%!-\/]))+\}\}"

	def get (self, Object = {}):
		return self.__process__(Object)
	
	def __format__ (self, string, attributes):
		for attribute in attributes:
			attr = getattr(self, str.upper(attributes[attribute]), None)
			if attr:
				string = attr + string + self.END
		return string

	def __substitute__ (self, string, attributes = {}):
		matches = re.findall(self.REG, string, re.DOTALL)

		for i in range(0, len(matches)):
			substring = re.sub("{{|}}", "", matches[i])
			matches[i] = {'original': substring, 'formatted': self.__format__(substring, attributes)}

		for i in range(0, len(matches)):
			string = re.sub(matches[i]['original'], matches[i]['formatted'], string)

		return re.sub("{{|}}", "", string)

	def __process__ (self, Object = {}):
		if not bool(Object):
			if self.StrObject:
				Object = self.StrObject
			else:
				Object = [{'str':'{{Sample}}', 'attr':{'color':'cyan'}}, {'str':'{{Text}}', 'attr':{'color':'purple'}}]
		
		if type(Object) is list:
			strs = []
			for i in range(0, len(Object)):
				strs.append(self.__substitute__(Object[i]['str'], Object[i]['attr']))
			return " ".join(strs)
		else:
			return self.__substitute__(Object['str'], Object['attr'])

	def __self__ (self):
		return type(self.StrObject)

	def __init__ (self, StrObject = {}):
		self.StrObject = StrObject



class ai (strstyle):

	def response (self, message = "Sample Text"):
		return (self.__name__() + self.seperator) + (" " + self.__msg__(message))

	def __msg__ (self, message = "Sample Text"):
		return message

	def __name__ (self):
		return self.get({'str': '{{'+ self.name +'}}', 'attr': self.style})

	def __self__ (self):
		return self

	def __init__ (self, **kwargs):
		self.name = kwargs.pop('name', 'system')
		self.style = kwargs.pop('style', {'style':'underline','weight':'bold'})
		self.seperator = kwargs.pop('seperator', ':')



de = ai(name = "de", style = {'color':'darkcyan', 'weight':'bold'})


{'name': 'de', 'style': {'color':'darkcyan','weight':'bold'}}

print de.response()

#print strstyle([{ 'str': '{{Hello}}', 'attr': {'t':'red'} }, {'str': '{{World}}', 'attr': {'t':'blue'}}]).get()

#print strstyle().get()