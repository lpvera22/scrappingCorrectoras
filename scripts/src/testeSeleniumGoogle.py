from pyvirtualdisplay import Display
from selenium import webdriver

# display = Display(visible=0, size=(800, 600))
# display.start()
# options = webdriver.ChromeOptions()
# options.add_argument('--no-sandbox')
# options = webdriver.ChromeOptions()
# options.add_argument('--disable-extensions')
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
driver.get('http://google.com')
print(driver.title)