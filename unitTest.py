"""
This is a unit-test file for testing the yaml site indexing feature
"""
#!/usr/bin/env python

from testPageLoader import getHomePageTest
import unittest


print "Starting Test"
if(getHomePageTest()):
	print "Error-getHomePageTest"

print "Test Finished"