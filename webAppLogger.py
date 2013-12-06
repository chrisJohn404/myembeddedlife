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

def log(data):
	logging.debug(data)
	logging.info(data)
	logging.warning(data)
	logging.error(data)
	logging.critical(data)