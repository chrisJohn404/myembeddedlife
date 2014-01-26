#this file contains the
#import webapp2
import os
import yaml
#from google.appengine.api import users
import logging
import re
from webAppLogger import log


class webApplication(object):
	def __init__(self, configDict=None, DEBUG=False):
		self.debug = DEBUG
		self.preLoadedDict = False

		if(configDict == None):
			self.webSiteInfo = yaml.load(open('index-data.yaml', 'rb'))
			#log('loading index-data.yaml file')
		else:
			self.webSiteInfo = configDict
			self.preLoadedDict = True
			#log('using pre-loaded index-data.yaml file')

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
			self.webSiteInfo['mainTabList'][5]['location']:
			yaml.load(open(self.webSiteInfo['mainTabList'][5]['location'],'rb')),
		}


		#get initial data from yaml file
		self.numMainTabs = len(self.webSiteInfo['mainTabList'])
		self.mainTabs = self.webSiteInfo['mainTabList']
		self.validMainTabs = []
		for i in range(0,6):
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
	def getCrumbURL(self,pathArray,index):
		crumbURL = ''
		for i in range(0,index):
			if(pathArray[i] != '') and (pathArray[i] !='Home'):
				crumbURL = crumbURL + '/' + pathArray[i]
		return crumbURL
	def parseSubPageURLs(self,pathArray,pData,data,index):
		pageData = pData['subPages']
		numPages = len(pageData)
		templateLocation = None
		startbreadCrumbVal = 3
		testVal = 10
		if(index > testVal):
			print pathArray[index]
		for page in pageData:
			if(page['title'] == pathArray[index]):
				pageData = page
				#if page exists try & load its template
				try:
					templateLocation = page['template']
				except KeyError:
					templateLocation = data['defaultTemplate']
				if(len(pathArray) == index+1):
					if(index > testVal):
						print templateLocation
					pageData['breadCrumbs'] = []
					crumbURL = self.getCrumbURL(pathArray,index)
					pageData['breadCrumbs'].insert(0,{'title': pData['dTitle'],'url': crumbURL})
					return pageData, templateLocation
				else:
					pageData, templateLocation = self.parseSubPageURLs(pathArray,pageData,data,index+1)
					if(index > testVal):
						print templateLocation
					crumbURL = self.getCrumbURL(pathArray,index)
					pageData['breadCrumbs'].insert(0,{'title': pData['dTitle'],'url': crumbURL})
					return pageData, templateLocation

		print 'Not Found'
		return pData, data['notFoundTemplate']
	#pData contains the more local yaml file data that needs to be parsed for valid pages & sub-pages
	#data contains the main yaml file.  Needed for loading the default html file if no specific one is found
	def parsePageURLs(self,pathArray,pData,data):
		if(len(pathArray) >= 3):
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
					if(len(pathArray) == 3):
						return pageData, templateLocation
					else:
						pageData, templateLocation = self.parseSubPageURLs(pathArray,pageData,data,3)
						pageData['breadCrumbs']
						print pageData['breadCrumbs']
						return pageData, templateLocation
			#if page isn't found then return the notFoundTemplate
			return pageData, data['notFoundTemplate']
		else:
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

	def getCustomHomeData(self, pathArray, data):
		pageData,templateLocation = self.getInitialData(pathArray, data)
		featuredPages = data['featuredPages']
		pageData = []

		#for each featured page, find & push appropriate project information into pageData array
		for fp in featuredPages:
			pType = fp['type']
			pTitle = fp['title']
			for mt in self.mainTabs:
				if(mt['title'] == pType):
					tLoc = mt['location']
					pData = self.pageYamls[tLoc]
					for rp in pData['pages']:
						if(rp['title'] == pTitle):
							#print 'Project Match!',pTitle
							rp.update({'type':pType})
							pageData.append(rp);
		if(self.debug and False):
			for p in pageData:
				print p['title']
				print p['type']
		return pageData, templateLocation

	#Parses path for main tabs.  Recognizes capital cases as 'altNames'
	def parseRequestString(self, pathArray):
		reqStr = pathArray[1]
		for i in range(0,self.numMainTabs):
			pData = self.webSiteInfo['mainTabList'][i]
			pTitle = pData['title']
			if(reqStr == pTitle):
				#print 'Found Match in title',reqStr, pTitle
				self.markTabAsActive(i)
				if(i == 0):
					return self.getCustomHomeData(pathArray,pData)
				else:
					return self.getInitialData(pathArray, pData)
			else:
				try:
					aNames = pData['altNames']
					for name in aNames:
						if(reqStr == name):
							#print 'Found Match in altNames',reqStr, name
							self.markTabAsActive(i)
							if(i == 0):
								return self.getCustomHomeData(pathArray,pData)
							else:
								return self.getInitialData(pathArray, pData)
				except KeyError:
					print 'KeyError on finding altNames'

		#If tab is not found (should never get here) then return None's
		#This case is hopefully covered by the app.yaml file
		#return None, None
		# This was clearly not true, return default page instead:
		return self.webSiteInfo,self.webSiteInfo['notFoundTemplate']

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
			#if(self.preLoadedDict != True):
			#	self.webSiteInfo['activePage'] = "pre-loaded dict"
			#else:
			#	self.webSiteInfo['activePage'] = reqStr


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
			elif (pathArray[1] == 'Notes'):
				self.webSiteInfo['mainTabList'][3]['selected']=None
			elif (pathArray[1] == 'Bookshelf'):
				self.webSiteInfo['mainTabList'][4]['selected']=None
			elif (pathArray[1] == 'AboutMe'):
				self.webSiteInfo['mainTabList'][5]['selected']=None
			else:
				self.webSiteInfo['mainTabList'][0]['selected']=None