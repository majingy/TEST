import sys
import os
import importlib
import unittest
import inspect
from datetime import datetime
from multiprocessing import Process
# from concurrent.futures import Executor
from concurrent.futures import ProcessPoolExecutor
# from concurrent.futures import ThreadPoolExecutor

testpath = "."
def find_tests(ignored):
	"""This function just grabs all the python files in the directory"""
	"""It will return the fully qualified path"""
	results_list = list()
	for x in os.walk(testpath):
		#print(x)
		ignore = 0
		for ignored_mem in ignored:
			if ignored_mem in x[0]:
				ignore = 1
				break
		if ignore == 0:
			for y in x[2]:
				if y[-3:] == ".py":
					file_name = ""
					if x[0][-1] != "/":
						file_name = x[0] + "/"+ y
					else:
						file_name = x[0] + y
					results_list.append(file_name)
	return results_list

def import_testcases(selection, selection_list):
	"""
	This function imports the testing modules. Returns a tuple
	containing the name of each Class, and a Module object to
	instantiate it from.
	"""

	#Create the proper form of the testpath
	formatted_testpath = testpath.strip("./").replace("/",".")
	
	module_list = list()
	mod_names = list()
	#This block performs two actions: It adds the Class name of the testcase to
	#a list to be instantiated later, and it imports the module dynamically
	for module in selection:
		#print("Module name: ",module)
		#for x in inspect.getmembers()
		test_name = selection_list[module-1][:-3].replace("/",".").lstrip(".")
		# #print("Original test name: "+ test_name)
		# #print("Printing Testpath: "+formatted_testpath)
		test_name = test_name.replace(formatted_testpath,"")
		# #print("New test name: "+ test_name)
		# mod_names.append(selection_list[module-1].split("/")[-1][:-3].capitalize())
		value = importlib.import_module(test_name.lstrip("."))
		#print(inspect.getmembers(value,inspect.isclass))
		for x in inspect.getmembers(value,inspect.isclass):
			if issubclass(x[1],unittest.TestCase):
				module_list.append(x[1])
				val = x[1]()
				#print(x)


		#module_list.append(value)
	#return (mod_names,module_list)
	return module_list

def construct_testsuite(mod_list):
	"""
	This function creates suites from all the test cases in the provided classes.
	Returns a list of Suite objects.
	"""
	all_suites = list()
	for number,module in enumerate(mod_list):
		#temp_class = getattr(module,name_mod[number])
		#test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(temp_class)
		test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(module)
		all_suites.append(test_suite)
	print(all_suites)
	return all_suites

def suite_runner(suite):
	result = ""
	#print(suite)
	result = unittest.TextTestRunner().run(suite[0])
	file_name = suite[2]+suite[1].__name__ +"_debug.txt"
	with open(file_name,"w")as file:
		file.write("Errors:\n")
		file.write(str(result.errors)+"\n")
		file.write("Failures:\n")
		try:
			file.write(str(result.failures[0][-1]))
		except:
			file.write("[]")
	#print(result)
	#return result






if __name__ == "__main__":
	configuration = dict()

	if len(sys.argv) == 1:
		print("Usage: python3 TestSuiteMain.py [Config File]")
	else:
		with open(sys.argv[1], "r") as in_file:
			for line in in_file:
				data = line.split(":")
				if len(data) != 2:
					print("Error in configuration file.")
					exit()
				configuration[data[0]] = data[1]
				#print (data[1])
		#print(configuration["platform"])

		testpath = configuration["tests_loc"].strip()
		ignored_directories = [x.strip() for x in configuration["ignore"].split(",")]
		debug_dir = configuration["debug_dir"].strip()
		interactive = configuration["interactive"].strip()
		#print(ignored_directories)
		#Not the best practice, but it makes any directory tree searchable for imports
		sys.path.append(testpath)

		tests_found = find_tests(ignored_directories)
		if interactive == "true":
			print("Tests Found:")
			for number,test in enumerate(tests_found):
				print("{}. {}".format(number + 1, test.replace(testpath,"")))#test.split("/")[-1]))

		choices = ""
		list_choices = list()
		if interactive == "true":
			choices = input("Please enter the numbers of the tests you would like to "\
				"run (space separated):\n")
			choices = choices.strip()

		#if len(choices) > 1:
		else:
			choices = configuration["tests"].strip()
			if choices == "*":
				list_range = [str(x) for x in range(1,len(tests_found)+1)]
				#print(list_range)
				choices = " ".join(list_range)

		list_choices.extend(list(map(int,choices.split(" "))))
		#print(list_choices)
		#else:
		#	choices = int(choices)
		mod_list = import_testcases(list_choices,tests_found)
		suites = construct_testsuite(mod_list)
		#create a new directory for the test results to be stored in
		date_name = str(datetime.now()).replace(" ","_")
		new_repo_name = debug_dir + date_name
		os.mkdir(new_repo_name)
		new_repo_name +="/"
		debug_dir_list = [new_repo_name]*len(mod_list)
		suites = zip(suites,mod_list,debug_dir_list)

		#print(debug_dir_list)
		#print(suites)
		#print(mod_list)

		proc_list = list()
		results = list()
		with ProcessPoolExecutor(max_workers=3) as pool:
			print("Inside pool")
			results =[x for x in pool.map(suite_runner, suites)]
		#print(results)

		# for suite in suites:
		# 	#print("Hello")
		# 	new_proc = Process(target=suite_runner,args=(suite,))
		# 	new_proc.start()
		# 	proc_list.append(new_proc)
		# for proc in proc_list:
		# 	proc.join()

			#unittest.TextTestRunner().run(suite)
