from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
import time
import math

class StaleException(Exception):
	pass
class FailedInstantiationException(Exception):
	pass
class SeleniumWrapper:

	def __init__(self, drivers):
		self.driver = ''
		self.wait = ''
		print(drivers)
		try:
			if drivers == 1:
				opts = webdriver.ChromeOptions()
				#opts.add_argument('headless')
				self.driver = webdriver.Chrome(chrome_options=opts)
				#self.driver.set_window_position(math.randint(0,2000),math.randint(0,2000))
				self.wait = WebDriverWait(self.driver,10)
			elif drivers == 2:
				opts = webdriver.ChromeOptions()
				opts.add_argument('headless')
				#opts.add_argument('--disable-gpu')
				#opts.add_argument("window-size=1024,768")
				#opts.add_argument("--no-sandox")
				#display = Display(visible=0, size=(800, 800))    
				#display.start() 
				self.driver = webdriver.Chrome(chrome_options=opts)
				self.wait = WebDriverWait(self.driver,10)
			elif drivers == 3:
				pass
		except Exception as e:
			#print("Exception: "+str(e))
			raise FailedInstantiationException

	def logon(self):
		self.driver.get("http://localhost:5601")
		#usn = self.driver.find_element_by_name("username")
		#usn.send_keys(username)
		#passw = self.driver.find_element_by_name("password")
		#passw.send_keys(password)
		#passw.send_keys(Keys.RETURN)
		self.wait.until(EC.title_contains("Kibana"))
		self.driver.get("http://localhost:5601/app/kibana#/dashboards?_g=()")
		self.wait.until(EC.presence_of_element_located((By.XPATH,'//div[@class="kuiTableRowCell__liner"]')))

	def close_out(self):
		self.driver.close()
		self.driver.quit()

	def navigate_to_page(self, url):
		"""
		Navigates to desired URL
		"""
		self.driver.get(url)

	def grab_element(self, location, method=0):
		"""
		Returns a webelement. The method defaults to CSS selctor
		but can be changed to xpath when needed. On failure to verify
		that the element actually exists, it returns 0.
		"""
		locator = By.CSS_SELECTOR
		function = self.driver.find_element_by_css_selector

		if method == 1:
			locator = By.XPATH
			function = self.driver.find_element_by_xpath
		worked = 0
		for x in range(3):
			try:
				self.wait.until(EC.visibility_of_element_located((locator,location)))
			except TimeoutException:
				pass#print("Exception caught: "+ str(TimeoutException))
			except StaleElementReferenceException:
				pass#print("Exception caught: "+ str(StaleElementReferenceException))
			else:
				worked = 1
				break
		if worked == 0:
			return 0

		element = ''

		while 1:
			elements_list = list()
			try:
				element = function(location)
				el = element.text
				print(el)
			except Exception as e:
				print("Exception in grab_element "+str(e))

			else:
				return element


				
	def grab_all_elements(self, location, method=0):
		"""
		Returns a webelement. The method defaults to CSS selctor
		but can be changed to xpath when needed. On failure to verify
		that the element actually exists, it returns 0.
		"""
		locator = By.CSS_SELECTOR
		function = self.driver.find_elements_by_css_selector

		if method == 1:
			locator = By.XPATH
			function = self.driver.find_elements_by_xpath

		worked = 0
		for x in range(3):
			try:
				self.wait.until(EC.visibility_of_all_elements_located((locator,location)))
			except TimeoutException:
				pass#print("Exception caught: "+ str(TimeoutException))
			except StaleElementReferenceException:
				pass#print("Exception caught: "+ str(StaleElementReferenceException))
			else:
				worked = 1
				break
		if worked == 0:
			return 0

		element = ''

		while 1:
			try:
				element = function(location)
				el = element[0].text
			except Exception as e:
				print("Exception in grab_all_elements"+str(e))

			else:
				return element
				
	def grab_all_elements_text(self, location, method=0):
		locator = By.CSS_SELECTOR
		function = self.driver.find_elements_by_css_selector

		if method == 1:
			locator = By.XPATH
			function = self.driver.find_elements_by_xpath

		worked = 0
		for x in range(3):
			try:
				self.wait.until(EC.visibility_of_all_elements_located((locator,location)))
			except TimeoutException:
				pass#print("Exception caught: "+ str(TimeoutException))
			except StaleElementReferenceException:
				pass#print("Exception caught: "+ str(StaleElementReferenceException))
			else:
				worked = 1
				break
		if worked == 0:
			return 0

		element = ''

		while 1:
			elements_list = list()
			try:
				element = function(location)
				for x in element:
					elements_list.append(x.text)
			except Exception as e:
				pass#print("Exception in grab_all_elements_text "+str(e))

			else:
				return elements_list



	def grab_all_elements_attribute(self, location, attr, method=0):
		locator = By.CSS_SELECTOR
		function = self.driver.find_elements_by_css_selector
		if method == 1:
			locator = By.XPATH
			function = self.driver.find_elements_by_xpath

		worked = 0
		for x in range(3):
			try:
				self.wait.until(EC.visibility_of_all_elements_located((locator,location)))
			except TimeoutException:
				pass#print("Exception caught: "+ str(TimeoutException))
			except StaleElementReferenceException:
				pass#print("Exception caught: "+ str(StaleElementReferenceException))
			else:
				worked = 1
				break
		if worked == 0:
			return 0

		element = ''

		while 1:
			elements_list = list()
			try:
				element = function(location)
				for x in element:
					elements_list.append(x.get_attribute(attr))
			except Exception as e:
				pass#print("Exception in grab_all_elements_text "+str(e))

			else:
				return elements_list
		# def click_all_elements(self, location, attr, method=0):
		# 	locator = By.CSS_SELECTOR
		# 	function = self.driver.find_elements_by_css_selector
		# 	if method == 1:
		# 		locator = By.XPATH
		# 		function = self.driver.find_elements_by_xpath

		# 	worked = 0
		# 	for x in range(3):
		# 		try:
		# 			self.wait.until(EC.visibility_of_all_elements_located((locator,location)))
		# 		except TimeoutException:
		# 			print("Exception caught: "+ str(TimeoutException))
		# 		except StaleElementReferenceException:
		# 			print("Exception caught: "+ str(StaleElementReferenceException))
		# 		else:
		# 			worked = 1
		# 			break
		# 	if worked == 0:
		# 		return 0

		# 	element = ''

		# 	while 1:
		# 		elements_list = list()
		# 		try:
		# 			element = function(location)
		# 			for x in element:
		# 				elements_list.append(x.click())
		# 		except Exception as e:
		# 			print("Exception in grab_all_elements_text "+str(e))

		# 		else:
		# 			return elements_list

	def click_on_element(self, location, method=0):
		element = self.grab_element(location, method)
		if element != 0:
			element.click()
		else:
			return 0

	def get_current_url(self):
		return self.driver.current_url

	# def grab_attribute(self, element, attribute):
	# 	for x in range(3):
	# 		element_attr = ''
	# 		try:
	# 			element_attr = element.get_attribute(attribute)
	# 		except StaleElementReferenceException as e:
	# 			print("Exception in grab_attribute "+str(e))
	# 		else:
	# 			return element_attr
	# 	return 0

	def grab_element_text(self, location, method=0):
		#print("Location: "+location)
		locator = By.CSS_SELECTOR
		function = self.driver.find_element_by_css_selector
		if method == 1:
			locator = By.XPATH
			function = self.driver.find_element_by_xpath

		worked = 0
		for x in range(3):
			try:
				self.wait.until(EC.visibility_of_element_located((locator,location)))
			except TimeoutException:
				pass#print("Exception caught: "+ str(TimeoutException))
			except StaleElementReferenceException:
				pass#print("Exception caught: "+ str(StaleElementReferenceException))
			else:
				worked = 1
				break
		if worked == 0:
			return 0

		element = ''

		while 1:
			try:
				element = function(location).text
			except Exception as e:
				pass#print("Exception in grab_element_text "+str(e))
			else:
				return element
	def grab_attribute(self, location, attribute, method=0):
		#print("Location: "+location)
		locator = By.CSS_SELECTOR
		function = self.driver.find_element_by_css_selector
		if method == 1:
			locator = By.XPATH
			function = self.driver.find_element_by_xpath

		worked = 0
		for x in range(3):
			try:
				self.wait.until(EC.visibility_of_element_located((locator,location)))
			except TimeoutException:
				pass#print("Exception caught: "+ str(TimeoutException))
			except StaleElementReferenceException:
				pass#print("Exception caught: "+ str(StaleElementReferenceException))
			else:
				worked = 1
				break
		if worked == 0:
			return 0

		element = ''

		while 1:
			try:
				element = function(location).get_attribute(attribute)
			except Exception as e:
				pass#print("Exception in grab_element_text "+str(e))
			else:
				return element

	#def grab_element_within
	def grab_element_kibana(self, location, method=1):
		#get element from kibana by xpath
		
		locator = By.CSS_SELECTOR
		#locator = By.XPATH
		function = self.driver.find_element_by_css_selector
		#function = self.driver.find_element_by_xpath

		if method == 1:
			locator = By.XPATH
			function = self.driver.find_element_by_xpath
		worked = 0
		for x in range(3):
			try:
				self.wait.until(EC.visibility_of_element_located((locator,location)))
			except TimeoutException:
				pass#print("Exception caught: "+ str(TimeoutException))
			except StaleElementReferenceException:
				pass#print("Exception caught: "+ str(StaleElementReferenceException))
			else:
				worked = 1
				break
		if worked == 0:
			return 0

		element = ''

		while 1:
			elements_list = list()
			try:
				#element = self.driver.find_element_by_css_selector(".panel-title")
				element = function(location)
				#element = self.driver.find_element_by_xpath("//dashboard-panel[@remove='removePanel(3)']/div/div/span")
				el = element.text
			except Exception as e:
				print("Exception in grab_element "+str(e))

			else:
				return element


	
	def grab_element_text_kibana(self, location, method=1):
		#Get element text from kibana by xpath
		locator = By.CSS_SELECTOR
		function = self.driver.find_element_by_css_selector
		if method == 1:
			locator = By.XPATH
			function = self.driver.find_element_by_xpath

		worked = 0
		for x in range(3):
			try:
				self.wait.until(EC.visibility_of_element_located((locator,location)))
			except TimeoutException:
				pass#print("Exception caught: "+ str(TimeoutException))
			except StaleElementReferenceException:
				pass#print("Exception caught: "+ str(StaleElementReferenceException))
			else:
				worked = 1
				break
		if worked == 0:
			return 0

		element = ''

		while 1:
			try:
				element = function(location).text
			except Exception as e:
				pass#print("Exception in grab_element_text "+str(e))
			else:
				return element
