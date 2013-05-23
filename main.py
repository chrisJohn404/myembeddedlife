# Copyright 2012 Digital Inspiration
# http://www.labnol.org/


import webapp2
import os
import jinja2
from google.appengine.api import users
import yaml

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
	def getHomePage(self):
		#get the client's user-name
		user = users.get_current_user()
		if user:
			self.webSiteInfo['currentUserName'] = 'Hello ' + str(user) + "!"
        #else:
        #	self.webSiteInfo['pageTitle'] = 'Log In'

		#make select the proper page as active
		self.webSiteInfo['mainTabList'][0]['selected']='true'
		return self.webSiteInfo

class MainPage(webapp2.RequestHandler):
    def get(self):
    	#create an instance of the webApplication class
    	page = webApplication()

    	#load the home page & perform actions
    	self.template_values = page.getHomePage()        
        
        #	self.redirect(users.create_login_url(self.request.uri))

        template = jinja_environment.get_template('Home/home.html')
        self.response.out.write(template.render(self.template_values))
class TutorialsPage(webapp2.RequestHandler):
	def get(self):
		print "testing"

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/Home', MainPage),
	])

def main():
    app.run()

if __name__ == '__main__':
    main()
