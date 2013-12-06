# Copyright 2012 Digital Inspiration
# http://www.labnol.org/
#dg
import webapp2
import os
import jinja2
from google.appengine.api import users
import yaml
import logging

'''
Include webApplication.py file that determines what page to load & run the 
web-application
'''
from webApplication import webApplication

'''
self defined logger that prints data to Google's Log Console or uses python print command
'''
from webAppLogger import log

#defines the jinja_environment variable
jinja_environment = jinja2.Environment(
	#defines the jinja_template location
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__)+"/templates")
)

configFile = yaml.load(open(os.path.dirname(__file__)+'/index.yaml', 'rb'))

class MainPage(webapp2.RequestHandler):
    def get(self):
    	
		self.mainPageDict = self.app.config.get('mainDict')
		
		data = 'yo'
		logging.info(logging.getLevelName(logging.INFO))
		logging.debug(data)
		#log(data)
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
		self.template_values, self.pageStr = self.page.returnPageString(
			reqStr, 
			self.userString
		)

		template = jinja_environment.get_template(self.pageStr)
		self.response.out.write(template.render(self.template_values))
		self.page.fixDict(reqStr)


'''
Below is where this web-app's URL's get mapped.  They get saved to a WSGI 
Application instance that gets run at the bottom of this file.

Look at the following webpage for further explanation:
https://developers.google.com/appengine/docs/python/tools/webapp/running

'MainPage' and 'PageNotFound' are RequestHandlers, they handle the actual get, 
post, put, delete, etc. Specifics (for python) are:
https://developers.google.com/appengine/docs/python/tools/webapp/requesthandlerclass

'''
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
	#see webAppLogger.py
	logging.getLogger().setLevel(logging.DEBUG)
	app.run()

if __name__ == '__main__':
    main()
