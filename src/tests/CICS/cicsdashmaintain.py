from seleniumwrapper import *
import unittest

class CICSRegion(unittest.TestCase):


	def setUp(self):
		self.splunk = SeleniumWrapper(2)
		self.splunk.logon()
		self.url = "http://localhost:5601/app/kibana#/dashboard/AV-klLpMJq-v-ecTBGib?_g=(refreshInterval:(display:Off,pause:!f,value:0),time:(from:'Wed%20Nov%2022%202017%2000:00:00%20GMT%2B0800',mode:absolute,to:'Wed%20Nov%2022%202017%2000:59:59%20GMT%2B0800'))&_a=(description:'',filters:!(),options:(darkTheme:!f),panels:!((col:1,id:AV_i8rHeju-vp428agmS,panelIndex:1,row:1,size_x:6,size_y:3,type:visualization),(col:7,id:AV_ms5kYju-vp428ayIa,panelIndex:2,row:1,size_x:6,size_y:3,type:visualization),(col:1,id:AV_mtyGeju-vp428ayMj,panelIndex:3,row:4,size_x:6,size_y:3,type:visualization),(col:7,id:AV_mucHvju-vp428ayPq,panelIndex:4,row:4,size_x:6,size_y:3,type:visualization),(col:1,id:AV_i84-dju-vp428agnZ,panelIndex:5,row:7,size_x:6,size_y:3,type:visualization),(col:7,id:AV_mw0Fuju-vp428ayad,panelIndex:6,row:7,size_x:6,size_y:3,type:visualization),(col:1,id:AV_mxjvRju-vp428ayes,panelIndex:7,row:10,size_x:6,size_y:3,type:visualization),(col:7,id:AV_iyqyJju-vp428af47,panelIndex:8,row:10,size_x:6,size_y:3,type:visualization),(col:1,id:AV_i8epgju-vp428aglN,panelIndex:9,row:13,size_x:12,size_y:3,type:visualization)),query:(match_all:()),timeRestore:!t,title:'CICS%20Dashboard',uiState:(),viewMode:view)"
		self.splunk.navigate_to_page(self.url)

		self.ignore_panels = [3,4, 15, 16]
		# FOR TEST_VERIFY_PANEL_TITLES:
		self.panel_titles = ["Top 5 CICS Total CPU Time by System:Job Name",
							"Top 5 CICS Average CPU Time by System:Job Name",
							"Top 5 CICS Total SRB Time by System:Job Name",
							"Top 5 CICS Average SRB Time by System:Job Name",
							"Top 5 CICS Total IO Time by System:Job Name",
							"Top 5 CICS Total Data Set Blocks Transferred by Job Name",
							"Top 5 CICS Short/Clear Storage Messages by System:Job Name",
							"Top 5 CICS Storage Violations by System:Job Name",
							"Top 5 CICS All Messages by System:Job Name"
                            ]
		self.panel_title_css = "//dashboard-panel[@remove='removePanel({})']/div/div/span"

		#FOR TEST_GRAPH_FORMATTING
		self.base_graph_css = "#panel{} >div>div > div >div.panel-body.dashboard-element-body>div>div>div>div>div>div>div>div>div>svg>"
		self.y_axis_text_css = self.base_graph_css + "g.highcharts-axis.highcharts-yaxis>text:nth-child(1)"
		self.y_axis_chart = ["Transaction Count",
		 				"CPU Utilization",
						"CPU Time",
						"Elapsed Time",
						"Dispatch Time",
						"Response Time",
						"Wait Time",
						"Message Count",
						"QR TCB Dispatch Time",
						"Ratio",
						"Message Count",
						"Percent of MAXTASK"]
		self.x_axis_label_text_css = self.base_graph_css + "g.highcharts-axis-labels.highcharts-xaxis-labels > text:nth-child(1)"
		self.legend_text_css = self.base_graph_css + "g.highcharts-legend > g > g > g.highcharts-legend-item.highcharts-column-series.highcharts-color-undefined.highcharts-series-0 > text > tspan"
		self.legend_text_css_line = self.base_graph_css + "g.highcharts-legend > g > g > g.highcharts-legend-item.highcharts-line-series.highcharts-color-undefined.highcharts-series-0 > text > tspan"
		#svg > g.highcharts-legend > g > g > g.highcharts-legend-item.highcharts-column-series.highcharts-color-undefined.highcharts-series-0
		self.general_x_axis = "svg > g.highcharts-axis-labels.highcharts-xaxis-labels > text:nth-child(1)"
		self.number_of_graphs = len(self.y_axis_chart)
		self.columns = [15, 19]
		self.graphs = [1, 3, 5, 7, 9, 11, 13, 15, 17, 18, 19, 20]
		

		#FOR TEST_TABLE_FORMATTING
		self.subheading_css = "#panel{} > div #statistics > table > thead > tr > th> a"
		self.table_subheadings = [
							["_time", "Transaction Count", "Sysplex", "System", "CICS Region","Transaction ID"],
							[""],
							["_time","Maximum CPU Time", "Average CPU Time","Sysplex","System","CICS Region","Transaction ID"],
							["_time","Maximum Elapsed Time","Average Elapsed Time","Sysplex","System","CICS Region",	"Transaction ID"],
							["_time","Maximum Dispatch Time","Average Dispatch Time","Sysplex", "System", "CICS Region","Transaction ID"],
							["_time","Maximum Response Time","Average Response Time","Sysplex", "System", "CICS Region","Transaction ID"],
							["_time","Maximum Wait Time","Average Wait Time","Sysplex", "System", "CICS Region","Transaction ID"],
							["_time","Message Text","Sysplex","System",	"CICS Region"]
							]
		self.table_css = "#panel{} > div #statistics > table > tbody > tr > td:nth-child(2)"
		self.number_of_tables_subheadings = len(self.table_subheadings)
		self.exclude = [4,16]
		self.tables = [2, 4, 6, 8, 10, 12, 14, 16]
		self.table_ignore = [4]
		self.number_of_tables = len(self.tables)

		#FOR TEST_DRILLDOWNS
		#self.results_url = "http://cdpz02.rtp.raleigh.ibm.com:8000/en-US/app/ibm_oaz_insights/cics_system_dashboard?filterSystem={}&filterSysplex={}&form.inputTime.earliest=0&form.inputTime.latest=&form.inputSysplex={}&form.inputSystem={}"
		#self.results_url_region = "http://cdpz02.rtp.raleigh.ibm.com:8000/en-US/app/ibm_oaz_insights/cics_region_dashboard?filterSystem={}&filterRegion={}&filterSysplex={}&form.inputTime.earliest=0&form.inputTime.latest=&form.inputSysplex={}&form.inputSystem={}&form.inputRegion={}"

		self.results_url = "http://cdpz02.rtp.raleigh.ibm.com:8000/en-US/app/ibm_oaz_insights/cics_transaction_dashboard?filterTran={}&filterRegion={}&filterSystem={}&filterSysplex={}&form.inputTime.earliest=-24h%40h&form.inputTime.latest=now&form.inputSysplex={}&form.inputSystem={}&form.inputRegion={}&form.inputTran={}"

		self.line_css = "#panel{} > div #statistics > table > tbody > tr >td:nth-child({})"
		self.drilldown_panels = [2,4,6,8,10,12,14]


	def tearDown(self):
		self.splunk.close_out()

	def test_verify_panels_exist(self):
		"""This test just checks if there are 8 different panels """
		#print("Checking Existance of 8 panels")
		print("Checking presence of all panels")

		number_of_panels = int()
		panel_debugging = ''
		#css_selector_class = ".panel-title"
		xpath_selector_class = "//dashboard-panel[@remove='removePanel({})']/div/div/span"
	

		for x in range(1, len(self.panel_titles)+ 1):
			if self.splunk.grab_element_kibana(xpath_selector_class.format(x)) != 0:
				print("Panel {} exists: Passed\n".format(x))
				panel_debugging += "Panel {} exists: Passed\n".format(x)
				number_of_panels += 1
			else:
				panel_debugging += "Panel {} exists: Failed\n".format(x)

		assert number_of_panels == len(self.panel_titles), panel_debugging
		
	def test_verify_panel_titles(self):
		""" Making sure panel titles are correct """
		print("Checking Panel Titles")

		number_correct = 0
		panel_title_debugging = "\n"

		for panel in range(1, len(self.panel_titles)+ 1):
			#Grabbing each panel title text
			element = self.splunk.grab_element_text_kibana(self.panel_title_css.format(panel,panel))

			if element == 0:
				panel_title_debugging += "Panel {} title: Failed: Element did not exist\n".format(panel)
				continue

			if element == self.panel_titles[panel-1]:
				number_correct += 1
				panel_title_debugging += "Panel {} title: Passed\n".format(panel)
			else:
				panel_title_debugging += "Panel {} title: Failed: Element does not match provided string\n".format(panel)

		assert number_correct == len(self.panel_titles), panel_title_debugging




