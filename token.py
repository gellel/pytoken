## external dependency

## pip install beautifulsoup4
from bs4 import BeautifulSoup as beautifulsoup

## pip install selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

## python base
from collections import namedtuple as Object 
import urllib2
import urllib
import re
import os

## set filepath for storage of fetched files
__filepath__ = os.path.dirname(os.path.realpath('__file__'))

## create pseudo class
HTTP = Object('HTTP', 'URL RequestDelay Headers')
## instantiate user HTTP URL and HTTP Headers
HTTP = HTTP(URL = (raw_input("Please enter a URL:") or "https://www.google.com/"), RequestDelay = (raw_input("Please set a timeout for asset collection:") or 3), Headers = {
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
	'Accept-Encoding': 'none',
	'Accept-Language': 'en-US,en;q=0.8',
	'Connection': 'keep-alive'
})
## define the HTTP request with user URL and the provided headers
request = urllib2.Request(HTTP.URL, headers = HTTP.Headers)
## open the URL
response = urllib2.urlopen(request)
## parse the HTML text
HTML = response.read()
## close the connection so it doesn't tell us to go away
response.close()



## setup file names
__filename__ = "temp.html"
## setup file paths
__fullpath__ = __filepath__ + "/temp/"

## create or edit new file
file = open(__fullpath__ + __filename__, "wt")
## append HTML
file.write(HTML)
## close the file
file.close()

## initalise selenium phantom
browser = webdriver.Firefox()
## fetch local file
browser.get("file:///" + (__fullpath__ + __filename__))


#try:
#	WebDriverWait(browser, HTTP.RequestDelay).until()


#css_selector = raw_input("Type CSS container selector:") or None

#element_selector = raw_input("Type HTML child selector:") or None

