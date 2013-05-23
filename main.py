# Copyright 2012 Digital Inspiration
# http://www.labnol.org/


import webapp2
import os
import jinja2
from google.appengine.api import users
import yaml
import logging

#defines the jinja_environment variable
jinja_environment = jinja2.Environment(
	#defines the jinja_template location
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__)+"/templates"))

class webApplication(object):
	def __init__(self):
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
	def populateUserName(self):
		#get the client's user-name
		user = users.get_current_user()
		if user:
			self.webSiteInfo['currentUserName'] = 'Hello ' + str(user) + "!"
		else:
			self.webSiteInfo['pageTitle'] = 'Log In'

	def getHomePage(self):
		self.populateUserName()

		#make select the proper page as active
		self.webSiteInfo['mainTabList'][0]['selected']='true'
		return self.webSiteInfo, self.webSiteInfo['mainTabList'][0]['template']

	def getTutorialsPage(self, reqStr):
		print reqStr[5:(reqStr[5:len(reqStr)].find(' ')+5)]
		self.populateUserName()

		#make select the proper page as active
		self.webSiteInfo['mainTabList'][1]['selected']='true'
		return self.webSiteInfo, self.webSiteInfo['mainTabList'][1]['template']

	def getProjectsPage(self, reqStr):
		reqStr = str(reqStr)
		print reqStr[5:(reqStr[5:len(reqStr)].find(' ')+5)]
		self.populateUserName()

		#make select the proper page as active
		self.webSiteInfo['mainTabList'][2]['selected']='true'
		return self.webSiteInfo, self.webSiteInfo['mainTabList'][2]['template']

	def getBookshelfPage(self, reqStr):
		print type(reqStr)
		print reqStr.url
		print reqStr.path
		reqStr = str(reqStr.path)

		self.populateUserName()

		#make select the proper page as active
		self.webSiteInfo['mainTabList'][3]['selected']='true'
		return self.webSiteInfo, self.webSiteInfo['mainTabList'][3]['template']

	def getAboutMePage(self, reqStr):
		print reqStr[5:(reqStr[5:len(reqStr)].find(' ')+5)]
		self.populateUserName()

		#make select the proper page as active
		self.webSiteInfo['mainTabList'][4]['selected']='true'
		return self.webSiteInfo, self.webSiteInfo['mainTabList'][4]['template']

class MainPage(webapp2.RequestHandler):
    def get(self):
    	#create an instance of the webApplication class
		page = webApplication()

    	#load the home page & perform actions
		self.template_values, self.pageStr = page.getHomePage()        
        
        #print self.request
        #	self.redirect(users.create_login_url(self.request.uri))

		template = jinja_environment.get_template(self.pageStr)
		self.response.out.write(template.render(self.template_values))

		
class TutorialsPage(webapp2.RequestHandler):
	def get(self):
		#create an instance of the webApplication class
		page = webApplication()

		#load the home page & perform actions
		self.template_values, self.pageStr = page.getTutorialsPage(self.request) 

		template = jinja_environment.get_template(self.pageStr)
		self.response.out.write(template.render(self.template_values))

class ProjectsPage(webapp2.RequestHandler):
	def get(self):
		#create an instance of the webApplication class
		page = webApplication()

    	#load the home page & perform actions
		self.template_values, self.pageStr = page.getProjectsPage(self.request) 

		template = jinja_environment.get_template(self.pageStr)
		self.response.out.write(template.render(self.template_values))

class BookshelfPage(webapp2.RequestHandler):
	def get(self):
		#create an instance of the webApplication class
		page = webApplication()

    	#load the home page & perform actions
		self.template_values, self.pageStr = page.getBookshelfPage(self.request) 

		template = jinja_environment.get_template(self.pageStr)
		self.response.out.write(template.render(self.template_values))

class AboutMePage(webapp2.RequestHandler):
	def get(self):
		#create an instance of the webApplication class
		page = webApplication()

    	#load the home page & perform actions
		self.template_values, self.pageStr = page.getAboutMePage(self.request) 

		template = jinja_environment.get_template(self.pageStr)
		self.response.out.write(template.render(self.template_values))

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/Home', MainPage),
	('/Tutorials', TutorialsPage),
	('/Tutorials/.*', TutorialsPage),
	('/Projects', ProjectsPage),
	('/Projects/.*', ProjectsPage),
	('/Bookshelf', BookshelfPage),
	('/Bookshelf/.*', BookshelfPage),
	('/AboutMe', AboutMePage),
	('/AboutMe/.*', AboutMePage),
	],
debug=True)

def main():
	logging.getLogger().setLevel(logging.DEBUG)
	app.run()

if __name__ == '__main__':
    main()
