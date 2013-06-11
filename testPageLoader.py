#this .py file tests to make sure the webApplication class used in the main.py file is returning proper results.


import yaml
from webApplication import webApplication

mainDict = yaml.load(open('index.yaml','rb'))['mainDict']
def getHomePageTest():
	page = webApplication(configDict = mainDict, DEBUG = False)
	
	testStrings = [
		'/',
		'/Home',
		'/Tutorials',
		'/Tutorials/Main',
		'/Projects',
		'/Bookshelf',
		'/AboutMe',
	]

	resultStrings = [
		'Home/home.html',
		'Home/home.html',
		'Home/home.html',
		'Home/home.html',
		'Home/home.html',
		'Home/home.html',
		'Home/home.html',
	]
	if(len(testStrings) != len(resultStrings)):
		print "bad test-cases"
		return True

	for i in range(0,len(testStrings)):
		template_values, pageStr = page.returnPageString(testStrings[i], 'chris')
		if(pageStr != resultStrings[i]):
			print "Failed URL test case: " + testStrings[i]
			return True

	return False