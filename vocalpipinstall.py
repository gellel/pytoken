class Pips (String):
	### attempt to install self if required as well as pip packages
	def install (self):
		if self.installed:
			### process pip packages
			self.__process__()
	### attempt to install single or multiple pips
	def __process__ (self):
		### confirm is pips is an instance of a list
		if type(self.pips) is list:
			### confirm that list is not empty
			if bool(self.pips):
				### iterate over the length of the list of pip items
				for i in range(0, len(self.pips)):
					### confirm that the list index instance is a dictionary
					if type(self.pips[i]) is dict:
						### confirm that the dictionary item is not empty
						if bool(self.pips[i]):
							### attempt to install item
							self.__ispackage__(self.pips[i])
		### otherwise confirm that pip is an instance of a dictionary
		elif type(self.pips) is dict:
			### confirm that the dictionary item is not empty 
			if bool(self.pips):
				### attempt to install item
				self.__ispackage__(self.pips)
	### attempt to install pip package and assign to global instance of module
	def __ispackage__ (self, package):
		### notify user that the system is checking that the pip package is installed on the OS
		#print self.system.response(self.concat("confirming PIP package", package['name'], "is installed."))
		### confirm that the item was found
		if self.__import__(package):
			self.package['installed'] = True
		else:
			self.package['installed'] = False
		

	### confirm that package python module can be imported
	def __import__ (self, package):
		### attempt to import package module
		try:
			### return class instance
			return importlib.import_module(package['import'])
		### handle exception error if package is not found
		except:
			### return False for error handling
			return False
	### assign imported module to global window variables
	def __globals__ (self, package):
		### confirm that module key exists in package dictionary (not all pips require classes)
		if 'module' in package:
			### confirm that corresponding window instance has a matching key
			if package['module'] in globals():
				### set global variable to the imported package
				globals()[package['module']] = self.__import__(package)
	### confirm that pip package manager is installed
	def __isinstalled__ (self):
		### notify user that system is checking that pip is installed
		print self.system.response("confirming PIP package manager is installed.")
		### confirm that subprocess was not able to run "pip" method
		if not Command(command = ["pip"]).process():
			### notify user that pip package manager is missing/not installed and that system will attempt to find file on the internet
			print self.system.response("PIP installer is missing. attempting to fetch file.")
			### set self instance of pip core to assumed location of pip python file
			self.pip_core = HTTPResource("https://bootstrap.pypa.io/get-pip.py").fetch()
			### confirm that pip core was retreived from the internet
			if not self.pip_core:
				### notify user that the file was downloaded and that system will attempt to install
				print self.system.response("successfully downloaded PIP core. attempting to install PIP.")
				### create temporary file
				self.pip_file =  File(name = "get-pip", ext = "py", temporary = False)
				### to write file the content fetched from website resource
				self.pip_file.write(self.pip_core)
				### close temporary file for loading into subprocess
				self.pip_file.close()
				### confirm that subprocess could run file
				if Command(command = [String().concat("sudo", "-H", "python", self.pip_file.file.name)], shell = True).process():
					### remove temporary file from system memory
					self.pip_file.remove()
					### notify user pip package manager was installed successfully
					print self.system.response("PIP was successfully installed. remember, PIP can be removed from your OS at any time but will be reinstalled upon running this file.")
			### if pip file was unable to be downloaded from the internet
			else:
				### notify user that pip file resource was not able to be fetched from supplied website
				print self.system.response("PIP could not be downloaded. if there is a stable internet connection, please download and install PIP manually.")
				### notify user that the pip file installation guide can be downloaded from source website
				print self.system.response(self.cconcat(["PIP installation guide is available at", " ", self.get({'str':self.tag('https://pip.pypa.io/en/stable/installing/'),'attr':{'style':'underline'}}), "."]))
				### return False for install success variable
				return False
		### if pip package manage subprocess call successfully ran pip
		else:
			### notify user that pip package manager is installed on OS
			print self.system.response("PIP package manager is installed on this operating system.")
		### return True for install success variable
		return True
	### constructor
	def __init__ (self, **kwargs):
		self.pips = kwargs.pop("pips", [])
		self.system = Responder()
		self.installed = self.__isinstalled__()