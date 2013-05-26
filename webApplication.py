#this file contains the
#import webapp2
import os
import yaml
#from google.appengine.api import users
import logging


class webApplication(object):
	def __init__(self):
		#h
		#ooh la la
		test = {
			'dumb': 'dumb',
		}
		homePage = {
			'title': 'Home',
		}
		instructables = {
			'title': 'Instructables',
			'Inst1': 'hello',
			'Inst2': 'world',
		}
		projects = {
			'title': 'Projects',
			'Project1': 'Project1',
			'Project2': 'Project2',
		}
		books = {
			'title': 'Bookshelf',
			'Book1': 'Book1',
			'Book2': 'Book2',
		}
		aboutMePage = {
			'title': 'AboutMe',
		}
		mainTabList = [
			'Home',
			'Instructables',
			'Projects',
			'Bookshelf',
			'AboutMe',
			'AboutMe',
			'AboutMe',
			'AboutMe',
			'AboutMe',
		]
		mainTabs = {
			'Tab1': homePage,
			'Tab2': instructables,
			'Tab3': projects,
			'Tab4': books,
			'Tab5': aboutMePage
		}
		self.webSiteInfo = {
			'pageTitle': 'myEmbeddedLife',
			'mainTabList': mainTabList,
			'mainTabs': mainTabs,
		}
		data = yaml.load(open('index.yaml', 'rb'))
		#print data
		#print "\r\n\r\n"
		#print self.webSiteInfo
		self.webSiteInfo = data
	def populateUserName(self, userString):
		return
		print "populate user name"
		#get the client's user-name
		#user = users.get_current_user()
		#if user:
		#	self.webSiteInfo['currentUserName'] = 'Hello ' + str(user) + "!"
		#else:
		#	self.webSiteInfo['pageTitle'] = 'Log In'

	def returnPageString(self, reqStr, userStr):
		templateDict = None
		templateLocation = None

		#open & return the proper .yaml parsed dictionary and template.html pointer/file
		if(reqStr != None):

			#shorten the string passed by the request handlers
			reqStr = reqStr[1:len(reqStr)]

			if (reqStr == '') or (reqStr == 'Home'):
				templateDict = self.webSiteInfo
				templateLocation = self.webSiteInfo['mainTabList'][0]['template']

		#update the user-name string in the returned templateDictionary
		if(userStr != None):
			self.populateUserName(userStr)

		return templateDict, templateLocation


	def getHomePage(self):
		#self.populateUserName()

		#make select the proper page as active
		self.webSiteInfo['mainTabList'][0]['selected']='true'
		return self.webSiteInfo, self.webSiteInfo['mainTabList'][0]['template']

	def getTutorialsPage(self, reqStr):
		reqStr = str(reqStr.path)
		#self.populateUserName()

		#make select the proper page as active
		self.webSiteInfo['mainTabList'][1]['selected']='true'
		return self.webSiteInfo, self.webSiteInfo['mainTabList'][1]['template']

	def getProjectsPage(self, reqStr):
		reqStr = str(reqStr.path)
		#self.populateUserName()

		#make select the proper page as active
		self.webSiteInfo['mainTabList'][2]['selected']='true'
		return self.webSiteInfo, self.webSiteInfo['mainTabList'][2]['template']

	def getBookshelfPage(self, reqStr):
		#print reqStr.url
		#print reqStr.path
		reqStr = str(reqStr.path)

		#self.populateUserName()

		#make select the proper page as active
		self.webSiteInfo['mainTabList'][3]['selected']='true'
		return self.webSiteInfo, self.webSiteInfo['mainTabList'][3]['template']

	def getAboutMePage(self, reqStr):
		reqStr = str(reqStr.path)
		#self.populateUserName()

		#make select the proper page as active
		self.webSiteInfo['mainTabList'][4]['selected']='true'
		return self.webSiteInfo, self.webSiteInfo['mainTabList'][4]['template']
