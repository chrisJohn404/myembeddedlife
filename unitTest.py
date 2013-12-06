#!/usr/bin/env python
"""
This is a unit-test file for testing the yaml site indexing feature
"""

from testPageLoader import getHomePageTest
import unittest


print "Starting Test"
if(getHomePageTest()):
	print "Error-getHomePageTest"

print "Test Finished"