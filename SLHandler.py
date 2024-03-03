from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import random
import time

def get_radom_header():
    with open('config_files/headers.json', 'r') as file:
        headers_config = json.load(file)
    
    
    selected_headers = headers_config[random.choice(["1", "2", "3", "4", "5"])]
    print(f"chosen header : {selected_headers}")
    
    options = {
        'seleniumwire_options': {
            'headers': selected_headers
        }
    }
    return options


class SLHandler:
    def __init__(self, headless=False) -> None:
        self.headless = headless
        options = Options()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
        #options.add_argument("window-size=1920,1080")
        if headless:
            options.add_argument("--headless")
        self.firefox_capabilities = webdriver.DesiredCapabilities.CHROME
        #self.firefox_capabilities['marionette'] = True
       
        self.driver = webdriver.Chrome(options=options)

    
    def get(self, url):
        try:
            self.driver.get(url)
            #self.driver.save_screenshot("debug_screenshot.png")

            return True
        except Exception as e:
            return False


    def quit(self):
        self.driver.close()
