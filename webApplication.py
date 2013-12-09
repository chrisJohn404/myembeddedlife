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

		#Load a selected amount of other yaml files
		self.pageYamls = {
			self.webSiteInfo['mainTabList'][1]['location']:
			yaml.load(open(self.webSiteInfo['mainTabList'][1]['location'],'rb')),
			self.webSiteInfo['mainTabList'][2]['location']:
			yaml.load(open(self.webSiteInfo['mainTabList'][2]['location'],'rb')),
			self.webSiteInfo['mainTabList'][3]['location']:
			yaml.load(open(self.webSiteInfo['mainTabList'][3]['location'],'rb')),
			self.webSiteInfo['mainTabList'][4]['location']:
			yaml.load(open(self.webSiteInfo['mainTabList'][4]['location'],'rb')),
		}


		#get initial data from yaml file
		self.numMainTabs = len(self.webSiteInfo['mainTabList'])
		self.validMainTabs = []
		for i in range(0,5):
			self.validMainTabs.append(self.webSiteInfo['mainTabList'][i]['title'])
			self.validMainTabs.extend(self.webSiteInfo['mainTabList'][i]['altNames'])

	def populateUserName(self, userString):
		if(userString != None):
			self.webSiteInfo['currentUserName'] = 'Hello ' + str(userString) + "!"
		else:
			self.webSiteInfo['currentUserName'] = 'Log In'
		return
	def markTabAsActive(self, index):
		self.webSiteInfo['mainTabList'][index]['selected']='true'

	#pData contains the more local yaml file data that needs to be parsed for valid pages & sub-pages
	#data contains the main yaml file.  Needed for loading the default html file if no specific one is found
	def parsePageURLs(self,pathArray,pData,data):
		
		pageData = pData['pages']
		numPages = len(pageData)
		templateLocation = None
		#Loop througgh pages data element & try to match the title with url
		for page in pageData:
			if(page['title'] == pathArray[2]):
				pageData = page
				#if page exists try & load its template
				try:
					templateLocation = page['template']
				except KeyError:
					templateLocation = data['defaultTemplate']
				return pageData, templateLocation

		#if page isn't found then return the notFoundTemplate
		return pageData, data['notFoundTemplate']

	#After first stage of path parsing, figure catch sub-page errors
	def getInitialData(self, pathArray, data):
		#Get Sub-Yaml files if they exist
		pData = None
		try:
			lData = data['location']

			#Currently only supports pre-loaded yaml files
			pData = self.pageYamls[lData]
		except KeyError:
			pData = None
		#Return information if asking for a primary tab
		if(len(pathArray) < 3):
			return pData,data['template']
		else:
			try:
				if(pData != None):
					#There is data to be parsed! call the next function
					return self.parsePageURLs(pathArray,pData,data)
				else:
					return None,data['notFoundTemplate']
			except KeyError:
				#There has been an error in searching for a page
				#or something............
				return None,data['notFoundTemplate']
		#can't do much, no template to return
		return None,None

	#Parses path for main tabs.  Recognizes capital cases as 'altNames'
	def parseRequestString(self, pathArray):
		reqStr = pathArray[1]
		for i in range(0,self.numMainTabs):
			pData = self.webSiteInfo['mainTabList'][i]
			pTitle = pData['title']
			if(reqStr == pTitle):
				#print 'Found Match in title',reqStr, pTitle
				self.markTabAsActive(i)
				return self.getInitialData(pathArray, pData)
			else:
				try:
					aNames = pData['altNames']
					for name in aNames:
						if(reqStr == name):
							#print 'Found Match in altNames',reqStr, name
							self.markTabAsActive(i)
							return self.getInitialData(pathArray, pData)
				except KeyError:
					print 'KeyError on finding altNames'

		#If tab is not found (should never get here) then return None's
		#This case is hopefully covered by the app.yaml file
		return None, None

	def returnPageString(self, reqStr, userStr):

		templateLocation = ""
		pageData = None
		#update the user-name string in the returned templateDictionary
		self.populateUserName(userStr)

		#open & return the proper .yaml parsed dictionary and template.html pointer/file
		if(reqStr != None):

			#Parse the desired path
			pathArray = re.split(r'/',reqStr)
			if(self.debug and False):
				print pathArray[1]
			pathName = pathArray[1]
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
			if(self.debug and False):
				print len(self.webSiteInfo['mainTabList'])
				print 'URL: ',pathName
				for i in range(0,5):
					pData = self.webSiteInfo['mainTabList'][i]
					
					templateStr = pData['template']
					if(templateStr != None):
						print templateStr
					try:
						pageYamlFile = pData['location']
						print pageYamlFile
					except KeyError:
						print 'KeyError'
					try:
						altNames = pData['altNames']
						print altNames
					except KeyError:
						print 'AltNames Key Error'
			'''
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
			'''
			#smart index of data
			pageData,templateLocation = self.parseRequestString(pathArray)
		else:
			if(self.debug):
				print 'Bad Query URL: ', pathArray[1]
			return None, "Home/home.html"			

		#return the required website-info dict allowing jinja to populate the  
		# template & the appropriate template-file location
		if(self.debug and False):
			print 'Results: ', templateLocation

		#pageData was self.webSiteInfo
		self.webSiteInfo['pageData'] = pageData
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