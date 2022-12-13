import json
import os
import pprint
import time
from rich.console import Console
from selenium import webdriver
from selenium.webdriver.common.by import By
class Parser: 
    def __init__(self) -> None:
        self.authData = AuthWorker()
        self.interface = Interface()
        self.driver = webdriver.Firefox()
    def auth(self): 
        url = None
        url = self.interface.ask_for_input(f'{url=}'.split("=")[0])[0]
        self.driver.get(url)
        self.driver.find_element(By.ID, "handleOrEmail").send_keys(self.authData.login)
        self.driver.find_element(By.ID, "password").send_keys(self.authData.password)
        self.driver.find_element(by=By.CLASS_NAME, value="submit").click()

    def parse(self):
        self.auth()
        time.sleep(2)
        page = self.driver.get_full_page_screenshot_as_png()

    
class AuthWorker: 
    def __init__(self) -> None:
        self.interface = Interface()
        all_vars = os.environ
        self.interface.print_collections(all_vars)
        try: 
            self.login = all_vars["cf_login"]
            self.password = all_vars['cf_password']
        except: 
            try:
                with open("auth_data.txt", "r") as f: 
                    self.login, self.password = f.readlines()
                    f.close()
            except:
                self.ask_for_credentials()
            
    def ask_for_credentials(self):
        self.login, self.password = self.interface.ask_for_input("self.login", "self.password")
        os.environ['cf_login'] = self.login
        os.environ['cf_password'] = self.password
        with open("auth_data.txt", "w") as f: 
            f.writelines([self.login + "\n", self.password])
            f.close()


class Interface():
    def __init__(self) -> None:
        self.console = Console()

    def _inp(self, paramName) -> str:
        self.console.print(f"provide {paramName}")
        return input()
        
    def ask_for_input(self,*vars):
        target = []
        for i in range(len(vars)): 
            target.append ( self._inp(vars[i]))
        return target

    def print_collections(self, vars):
        if(type(vars) == list): 
            for i in vars: 
                self.console.print(i)
        if(type(vars) == dict):
            self.console.print_json(json.dumps(vars))
    def interface(self, **options):
        pass