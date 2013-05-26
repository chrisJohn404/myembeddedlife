# Copyright 2012 Digital Inspiration
# http://www.labnol.org/
#dg
import webapp2
import os
import jinja2
from google.appengine.api import users
import yaml
import logging

#Include .py file that determines what page to load & run the web-application
from webApplication import webApplication

#defines the jinja_environment variable
jinja_environment = jinja2.Environment(
	#defines the jinja_template location
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__)+"/templates"))


class MainPage(webapp2.RequestHandler):
    def get(self):
		print "hello!!"
    	#create an instance of the webApplication class
		self.page = webApplication()

		#get the client's user-name
		user = users.get_current_user()
		if user:
			self.userString = str(self.user)
			self.webSiteInfo['currentUserName'] = 'Hello ' + str(user) + "!"
		else:
			self.userString = None

		print "hello!!"
		#get information to load webpage
		self.page.returnPageString(str(self.request), self.userString)

    	#load the home page & perform actions
		self.template_values, self.pageStr = self.page.getHomePage()        
        
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
