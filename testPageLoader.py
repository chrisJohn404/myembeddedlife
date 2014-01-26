#this .py file tests to make sure the webApplication class used in the main.py file is returning proper results.


import yaml
from webApplication import webApplication

mainDict = yaml.load(open('index-data.yaml','rb'))['mainDict']

'''
Unit test for testing whether or not the right .html file is being loaded.

The page that is loaded is determined by the index.yaml file & the code in the webApplication.py
'''
def getHomePageTest():
	print 'Creating WebApp Instance'
	page = webApplication(configDict = mainDict, DEBUG = True)
	
	tests = [
	# #Home Page Loading
	{	'test':'/',										'result':'Home/home.html'										},
	{	'test':'/Home',									'result':'Home/home.html'										},
	{	'test':'/home',									'result':'Home/home.html'										},
	{	'test':'/Not A Page',							'result':'pageNotFound.html',									},

	#Test Tutorial URL's
	{	'test':'/Tutorials',							'result':'Tutorials/tutorialsTab.html',							},
	{	'test':'/Tutorials/bla',						'result':'Tutorials/tutorialNotFound.html',						},
	{	'test':'/Tutorials/Google-Graphs',				'result':'Tutorials/tutorialsTabDefault.html',					},
	{	'test':'/Tutorials/Embedding-Git',				'result':'Tutorials/tutorialsTabDefault.html',					},

	#Test Projects URL's
	{	'test':'/Projects',								'result':'Projects/projectsTab.html',							},
	{	'test':'/Projects/bla',							'result':'Projects/projectNotFound.html',						},
	{	'test':'/Projects/MyEmbeddedLife',				'result':'Projects/projectsTabDefault.html',					},
	{	'test':'/Projects/S.T.A.B.L.E.',				'result':'Projects/projectsTabDefault.html',					},
	{	'test':'/Projects/Diablo',						'result':'Projects/projectsTabDefault.html',					},
	{	'test':'/Projects/Simon-Says',					'result':'Projects/projectsTabDefault.html',					},

	#Test Notes URL's
	{	'test':'/Notes',								'result':'Notes/notesTab.html',									},
	{	'test':'/Notes/bla',							'result':'Notes/noteNotFound.html',								},
	{	'test':'/Notes/ble',							'result':'Notes/notesTabDefault.html',							},
	{	'test':'/Notes/ble/Nordic-nRF51822',			'result':'Notes/notesTabDefault.html',							},
	{	
		'test':'/Notes/ble/Nordic-nRF51822/GettingStarted',			
		'result':'Notes/notesTabDefault.html',							
	},
	{	
		'test':'/Notes/ble/Nordic-nRF51822/TestApplication',			
		'result':'Notes/notesTabDefault.html',							
	},

	#Test Bookshelf URL's
	{	'test':'/Bookshelf',							'result':'Bookshelf/bookshelfTab.html',							},
	{	'test':'/Bookshelf/bla',						'result':'Bookshelf/bookNotFound.html',							},

	#Test AboutMe URL's
	{	'test':'/AboutMe',								'result':'AboutMe/aboutMeTab.html',								},
	{	'test':'/AboutMe/bla',							'result':'AboutMe/attributeNotFound.html',						},

	]


	testStrings = [
		'/',
		#'/Home',
		#'/home',
		'/Tutorials',
		'/tutorials',
		'/Tutorials/Not A Page',
		'/Tutorials/Google-Graphs',
		'/Tutorials/Embedding-Git',
		'/Projects',
		'/projects',
		'/Projects/Not A Page',
		'/Projects/MyEmbeddedLife/bl',
		'/Projects/MyEmbeddedLife',
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
		#'Home/home.html',
		#'Home/home.html',
		'Tutorials/tutorialsTab.html',
		'Tutorials/tutorialsTab.html',
		'Tutorials/tutorialNotFound.html',
		'Tutorials/tutorialsTabDefault.html',
		'Tutorials/tutorialsTabDefault.html',
		'Projects/projectsTab.html',
		'Projects/projectsTab.html',
		'Projects/projectNotFound.html',
		'Projects/projectNotFound.html',
		'Projects/PJ1/PJ1.html',
		'Projects/projectNotFound.html',
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
	#else:
	#	for i in range(0,len(resultStrings)):
	#		print testStrings[i] + ' -> ' + resultStrings[i]
	testError = False

	for i in range(0,len(tests)):
		template_values, pageStr = page.returnPageString(tests[i]['test'], 'chris')
		try:
			print len(template_values['pageData']['breadCrumbs'])
		except:
			1+1
		if(pageStr != tests[i]['result']):
			print "Failed URL test case: " + tests[i]['test']
			print 'Returned Pages: ',pageStr
			print ''
			testError = True
	"""
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
	"""
	return testError


