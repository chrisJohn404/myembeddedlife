#this file contains the
#import webapp2
import os
import yaml
#from google.appengine.api import users
import logging
import re


class webApplication(object):
	def __init__(self, configDict=None, DEBUG=False):
		self.debug = DEBUG
		self.preLoadedDict = False
		if(configDict == None):
			self.webSiteInfo = yaml.load(open('index.yaml', 'rb'))
		else:
			self.webSiteInfo = configDict
			self.preLoadedDict = True

	def populateUserName(self, userString):
		if(userString != None):
			self.webSiteInfo['currentUserName'] = 'Hello ' + str(userString) + "!"
		else:
			self.webSiteInfo['currentUserName'] = 'Log In'
		return

	def returnPageString(self, reqStr, userStr):

		templateLocation = ""

		#update the user-name string in the returned templateDictionary
		self.populateUserName(userStr)

		#open & return the proper .yaml parsed dictionary and template.html pointer/file
		if(reqStr != None):

			#Parse the desired path
			pathArray = re.split(r'/',reqStr)
			if(self.debug):
				print pathArray[1]

			#shorten the string passed by the request handlers
			reqStr = reqStr[1:len(reqStr)]

			#update the page-title string
			self.webSiteInfo['pageTitle'] = pathArray[1]

			#update the active-page sub-header
			if(self.preLoadedDict != True):
				self.webSiteInfo['activePage'] = "pre-loaded dict"
			else:
				self.webSiteInfo['activePage'] = reqStr

			#switch between main path's before starting to dig deaper into the .yaml mess
			if (pathArray[1] == 'Home'):
				self.webSiteInfo['mainTabList'][0]['selected']='true'
				templateLocation = str(self.webSiteInfo['mainTabList'][0]['template'])
			elif (pathArray[1] == 'Tutorials'):
				self.webSiteInfo['mainTabList'][1]['selected']='true'
				templateLocation = str(self.webSiteInfo['mainTabList'][1]['template'])
			elif (pathArray[1] == 'Projects'):
				self.webSiteInfo['mainTabList'][2]['selected']='true'
				templateLocation = str(self.webSiteInfo['mainTabList'][2]['template'])
			elif (pathArray[1] == 'Bookshelf'):
				self.webSiteInfo['mainTabList'][3]['selected']='true'
				templateLocation = str(self.webSiteInfo['mainTabList'][3]['template'])
			elif (pathArray[1] == 'AboutMe'):
				self.webSiteInfo['mainTabList'][4]['selected']='true'
				templateLocation = str(self.webSiteInfo['mainTabList'][4]['template'])
			else:
				self.webSiteInfo['mainTabList'][0]['selected']='true'
				templateLocation = str(self.webSiteInfo['mainTabList'][0]['template'])
		else:
			return None, "Home/home.html"			

		#return the required website-info dict allowing jinja to populate the  
		# template & the appropriate template-file location
		return self.webSiteInfo, templateLocation

	def fixDict(self, reqStr):
		if(reqStr != None):

			#Parse the desired path
			pathArray = re.split(r'/',reqStr)

			#switch between main path's before starting to dig deaper into the .yaml mess
			if (pathArray[1] == 'Home'):
				self.webSiteInfo['mainTabList'][0]['selected']=None
			elif (pathArray[1] == 'Tutorials'):
				self.webSiteInfo['mainTabList'][1]['selected']=None
			elif (pathArray[1] == 'Projects'):
				self.webSiteInfo['mainTabList'][2]['selected']=None
			elif (pathArray[1] == 'Bookshelf'):
				self.webSiteInfo['mainTabList'][3]['selected']=None
			elif (pathArray[1] == 'AboutMe'):
				self.webSiteInfo['mainTabList'][4]['selected']=None
			else:
				self.webSiteInfo['mainTabList'][0]['selected']=None