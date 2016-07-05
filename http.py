import urllib2

class HTTPResource:

	def close (self):
		if self.response:
			self.response.close()
		return self

	def fetch (self):
		if self.__http__():
			return self.__read__()
		else:
			return None

	def __read__ (self):
		return self.response.read()

	def __http__ (self):
		try:
			self.response = urllib2.urlopen(self.request)
		except:
			self.response = None
		return self.response

	def __form__ (self):
		return urllib2.Request(url = self.request_URL, headers = self.request_headers)

	def __init__ (self, URL = "https://www.google.com/", headers = {}):
		self.request_URL = URL
		self.request_headers = headers
		self.request = self.__form__()


if __name__ == "__main__":

	print HTTPResource().fetch()