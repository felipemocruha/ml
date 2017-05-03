from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

caps = webdriver.DesiredCapabilities().FIREFOX
caps['marionette'] = False
d = webdriver.Firefox(capabilities=caps)
d.get('http://www.buscape.com.br/xprocura?kw=&eid=255256&pagina=6')
soup = BeautifulSoup(d.page_source)
