# Copyright 2012 Digital Inspiration
# http://www.labnol.org/


import webapp2
import os
import jinja2
from google.appengine.api import users

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
		self.a = 1
	def get(self):
		return self.webSiteInfo

class MainPage(webapp2.RequestHandler):
    def get(self):
    	user = users.get_current_user()
    	print user

    	page = webApplication()

    	self.template_values = page.get()
        #self.response.headers['Content-Type'] = 'text/html'
        #self.response.write('<h1>Hello, webapp2 Worlda!</h1>')
        
        if user:
        	self.template_values['pageTitle'] = user
        else:
        	self.redirect(users.create_login_url(self.request.uri))
        template = jinja_environment.get_template('Home/home.html')
        self.response.out.write(template.render(self.template_values))
        

app = webapp2.WSGIApplication([('/', MainPage)])

def main():
    app.run()

if __name__ == '__main__':
    main()
