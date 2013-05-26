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

configFile = yaml.load(open('index.yaml', 'rb'))

class MainPage(webapp2.RequestHandler):
    def get(self):

		self.mainPageDict = self.app.config.get('mainDict')
    	#create an instance of the webApplication class
		self.page = webApplication(configDict = self.mainPageDict)

		#get the client's user-name
		user = users.get_current_user()
		if user:
			self.userString = str(self.user)
			self.webSiteInfo['currentUserName'] = 'Hello ' + str(user) + "!"
		else:
			self.userString = None

		#get information to load webpage
		#request options: path, url, (none)
		reqStr = str(self.request.path)
		self.template_values, self.pageStr = self.page.returnPageString(reqStr, self.userString)

		template = jinja_environment.get_template(self.pageStr)
		self.response.out.write(template.render(self.template_values))
		self.page.fixDict(reqStr)

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/Home', MainPage),
	('/Tutorials', MainPage),
	('/Tutorials/.*', MainPage),
	('/Projects', MainPage),
	('/Projects/.*', MainPage),
	('/Bookshelf', MainPage),
	('/Bookshelf/.*', MainPage),
	('/AboutMe', MainPage),
	('/AboutMe/.*', MainPage),
	],
debug=True, config=configFile)

def main():
	logging.getLogger().setLevel(logging.DEBUG)
	app.run()

if __name__ == '__main__':
    main()
