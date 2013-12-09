#!/usr/bin/env python
"""
This is a unit-test file for testing the yaml site indexing feature
"""

'''
Google Handler Testing:
https://developers.google.com/appengine/docs/python/tools/handlertesting

Google Unit Testing:
https://developers.google.com/appengine/docs/python/tools/localunittesting
'''
from testPageLoader import getHomePageTest
import unittest


print "Starting Test"
if(getHomePageTest()):
	print "!!ERROR!! - getHomePageTest"
else:
	print "All Tests Pass"
#print "Test Finished"