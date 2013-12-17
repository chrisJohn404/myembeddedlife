#!/usr/bin/env python
"""
This is a sitemap.xml file updater that scrapes the .yaml files to get a list of all the different pages google should parse
"""

from testPageLoader import getHomePageTest
import yaml
import xml.etree.ElementTree as ET

newFileName = 'sitemap2.xml'
mainDict = yaml.load(open('index-data.yaml','rb'))['mainDict']

sm = ET.parse('siteRequired/sitemap (2).xml')
root = sm.getroot()
for child in root:
	for el in child:
		print el.tag
#print "Test Finished"