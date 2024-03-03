#started 20/08/2022 02:28



from SLHandler import SLHandler
from selenium.webdriver.common.by import By
import time

class Crawler():

    def __init__(self, header=None, proxies=None, headless=False) -> None:
        self.webdriver = SLHandler(headless=headless)
    
    def getResult(self, drivers, step):
        if step["actionOnReturn"] == "GET_ATTR" or step["actionOnReturn"] == "TAG_NAME":
            try:
                if step["action"] == "findS":
                    return [element.get_attribute(step["actionOnReturnArg"]) for element in drivers]
                else:
                    if type(drivers) == list:
                        return drivers[0].get_attribute(step["actionOnReturnArg"])
                    else:
                        return drivers.get_attribute(step["actionOnReturnArg"])
            except Exception as e:
                print("FAILED IN GET RESULT")
                print(e)
                return False
        elif step["actionOnReturn"] == "TEXT":
            if type(drivers) == list:
                return ''.join([element.text for element in drivers])
            else:
                return drivers[0].text

    def gotoObjective(self, steps, url, do_init=False):
        time.sleep(0.5)
        while not self.webdriver.get(url):
            print("TIMEOUT TRYING AGAIN")
        if do_init:
            to_do = steps["init"]
        else:
            to_do = steps
        for step in to_do:
            time.sleep(0.5)
            try:
                if step["mandatoryLevel"] == '3':
                    if step["SuccessReturn"] == "CONTENT":
                        return self.getResult(self.__doAction(step), step)
                    elif step["SuccessReturn"] == "CONTINUE":
                       self.webdriver.driver = self.__doAction(step)
                else:
                    self.__doAction(step)
            except Exception as e:
                print(e)
                if step["mandatoryLevel"] == '3':
                    return step["FailedReturn"]
                if step["mandatoryLevel"] == '2':
                    step["source"] = step["source2"]
                    if "newType" in step:
                        step["type"] = step["newType"]
                    try:
                        self.__doAction(step)
                    except Exception as e:
                        return None
                else:
                    return None
        return True

    def __doAction(self, step):
        type = self.__returnType(step["type"])
        source = step["source"]
    
        if step["action"] == "find":
            if step["subAction"] == "click":
                return self.webdriver.driver.find_element(type, source).click()
            elif step["subAction"] == "clear":
                return self.webdriver.driver.find_element(type, source).clear()
            elif step["subAction"] == "sendKey":
                return self.webdriver.driver.find_element(type, source).send_keys(step["input"])
            else:
                return self.webdriver.driver.find_element(type, source)
        elif step["action"] == "findS":
                return self.webdriver.driver.find_elements(type, source)
        else:
            pass

    def __returnType(self, type):
        if type == "XPATH":
            return By.XPATH
        elif type == "ID":
            return By.ID
        elif type == "CLASS_NAME":
            return By.CLASS_NAME
        elif type == "CSS_SELECTOR":
            return By.CSS_SELECTOR
        elif type == "TAG_NAME":
            return By.TAG_NAME
        else:
            pass

    def shutdown(self):
        self.webdriver.quit()
