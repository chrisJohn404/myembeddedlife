# Copyright 2012 Digital Inspiration
# http://www.labnol.org/
#dg
import webapp2
import os
import logging

'''
Information about logging can be found here:
https://developers.google.com/appengine/articles/logging
'''

def log(data, level=1):
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