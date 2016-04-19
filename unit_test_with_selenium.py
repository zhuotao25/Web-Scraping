from selenium import webdriver
driver = webdriver.PhantomJS(executable_path='phantomjs-2.0.0-windows/bin/phantomjs')
driver.get("http://en.wikipedia.org/wiki/Monty_Python")
assert "Monty Python2" in driver.title
driver.close()
