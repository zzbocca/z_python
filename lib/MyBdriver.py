from selenium import webdriver

class myDriver:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--test-type")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-setuid-sandbox")
        self.driver = webdriver.Chrome(executable_path=("/usr/local/bin/chromedriver"), chrome_options=options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(20)

    def getDriver(self):
        return self.driver

    def temDriver(self):
        self.driver.close()
