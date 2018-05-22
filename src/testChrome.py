from selenium import webdriver
opts = webdriver.ChromeOptions()
opts.add_argument('--headless')
opts.add_argument('--disable-gpu')
opts.add_argument("window-size=1024,768")
opts.add_argument("--no-sandox")
driver = webdriver.Chrome(chrome_options=opts)
driver.get("http://www.baidu.com")