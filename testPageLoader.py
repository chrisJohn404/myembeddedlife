#this .py file tests to make sure the webApplication class used in the main.py file is returning proper results.


import yaml
from webApplication import webApplication

def getHomePageTest():
	page = webApplication()
	
	#test default-page loading
	template_values, pageStr = page.returnPageString('/', 'chris')
	print "template loaded: " + pageStr
	#print "dict returned: " + str(template_values)
	if(pageStr != 'Home/home.html'):
		return True
	template_valuesa, pageStr = page.getHomePage();
	print "template loaded: " + pageStr
	if(template_values == template_valuesa):
		print "dict's match"
	#test Home-page loading
	template_values, pageStr = page.returnPageString('/Home', 'chris')
	if(pageStr != 'Home/home.html'):
		return True

	return False