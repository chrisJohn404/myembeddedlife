# Copyright 2012 Digital Inspiration
# http://www.labnol.org/
#dg
useLogger=False
import os
try:
	import webapp2
	import logging
	useLogger=True
except ImportError:
	useLogger=False
'''
Information about logging can be found here:
https://developers.google.com/appengine/articles/logging
'''

def log(data, level=1):
	if(useLogger):
		if(level==0): #having a hard time getting 'debug' log level to print out to google appengine console
			logging.debug(data)
		if(level==1):
			logging.info(data)
		if(level==2):
			logging.warning(data)
		if(level==3):
			logging.error(data)
		if(level==4):
			logging.critical(data)
	else:
		print 'lvl:',1,data