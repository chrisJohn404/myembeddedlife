#this .py file tests to make sure the webApplication class used in the main.py file is returning proper results.


import yaml
from webApplication import webApplication

mainDict = yaml.load(open('index.yaml','rb'))['mainDict']

'''
Unit test for testing whether or not the right .html file is being loaded.

The page that is loaded is determined by the index.yaml file & the code in the webApplication.py
'''
def getHomePageTest():
	print 'Creating WebApp Instance'
	page = webApplication(configDict = mainDict, DEBUG = True)
	
	testStrings = [
		'/',
		'/Home',
		'/Tutorials',
		'/tutorials',
		'/Tutorials/Not A Page',
		'/Tutorials/MyTutorial1',
		'/Projects',
		'/projects',
		'/Projects/Not A Page',
		'/Projects/PJ1',
		'/Projects/PJ2',
		'/BookShelf',
		'/bookShelf',
		'/bookshelf',
		'/Bookshelf',
		'/BookShelf/Not A Page',
		'/AboutMe',
		'/aboutMe',
		'/aboutme',
		'/Aboutme',
		'/AboutMe/Not A Page',
	]

	resultStrings = [
		'Home/home.html',
		'Home/home.html',
		'Tutorials/tutorialsTab.html',
		'Tutorials/tutorialsTab.html',
		'Tutorials/tutorialNotFound.html',
		'Tutorials/tutorialsTabDefault.html',
		'Projects/projectsTab.html',
		'Projects/projectsTab.html',
		'Projects/projectNotFound.html',
		'Projects/PJ1/PJ1.html',
		'Projects/projectsTabDefault.html',
		'Bookshelf/bookshelfTab.html',
		'Bookshelf/bookshelfTab.html',
		'Bookshelf/bookshelfTab.html',
		'Bookshelf/bookshelfTab.html',
		'Bookshelf/bookNotFound.html',
		'AboutMe/aboutMeTab.html',
		'AboutMe/aboutMeTab.html',
		'AboutMe/aboutMeTab.html',
		'AboutMe/aboutMeTab.html',
		'AboutMe/attributeNotFound.html',
	]
	if(len(testStrings) != len(resultStrings)):
		print "bad test-cases"
		print "Num Tests",len(testStrings)
		print "Num Results",len(resultStrings)
		return True
	testError = False
	for i in range(0,len(testStrings)):
		template_values, pageStr = page.returnPageString(testStrings[i], 'chris')
		if(pageStr != resultStrings[i]):
			print "Failed URL test case: " + testStrings[i]
			print 'Returned Pages: ',pageStr
			print ''
			
			testError = True
		#print 'Request',testStrings[i]
		#if((testStrings[i] == '/Projects/PJ1')):
		#	print template_values['pageData']
		#	print 'Returned Page: ',pageStr

	return testError


