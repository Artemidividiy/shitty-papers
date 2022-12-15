import json
import os
from PIL import Image
import datetime 
import time
from rich.console import Console
from selenium import webdriver
from selenium.webdriver.common.by import By

latin = r'[a-z]'

class Restrictions: 
    def __init__(self, time: str, memory: str) -> None:
        self.time = time
        self.memory = memory
    
    def to_str(self):
        return f"time {self.time} || memory: {self.memory}\n"
    def to_dict(self):
        return {"time" : self.time, "memory": self.memory}

    def fromDriver(driver):
        time = driver.find_element(By.CLASS_NAME, "time-limit").text
        memory = driver.find_element(By.CLASS_NAME, "memory-limit").text
        return Restrictions(time=time, memory=memory)
    
    def generate_markdown(self):
        return f" | Ограничение на время | Ограничение на память |\n| ---- | ---- |\n| {self.time} | {self.memory} |"
class SystemData:
    def __init__(self,iteration: int) -> None:
        self.createdAt = datetime.datetime.now()
        self.iteration = iteration

    def to_string(self):
        return f"createdAt : {self.createdAt} | iteration : {self.iteration}\n"

    def to_dict(self):
        return {
            "createdAt" : self.createdAt,
            "iteration": self.iteration
        }
    def generate_markdown(self):
        return f"---\n{self.to_string()}\n---"
class Page:
    def __init__(self, url=None) -> None:
        self.parser = Parser(url)
        (self.title, 
        self.restrictions, 
        self.input_type, self.task, self.input_specification, self.output_specification) = self.parser.parse()
    def to_str(self):
        return f"\ntitle: {self.title}\n\n---\nrestrictions: {self.restrictions.to_str()}\n\n---\ninput_type: {self.input_type}\n\n---\ntask: {self.split_text()}\n\n---\ninput_specification: {self.input_specification}\n\n---\noutput_specification: {self.output_specification}\n"
    def generate_markdown(self):
        target = f"# {self.title}\n"
        target += f"### Ограничения: \n{self.restrictions.generate_markdown()}\n"
        target += f"### Организация ввода/вывода: \n {self.input_type} \n\n ---\n"
        target += f"### Задание\n {self.split_text()}\n\n---\n"
        target += f"### Входные данные\n {self.input_specification}\n"
        target += f"### Выходные данные]\n {self.output_specification}\n"
        return target

    def write_to_file(self):
        iteration = 1
        try:
            with open(f"{self.title}.md", 'r') as f:
                iteration = f.read()[f.read().find("iteration") + len("iteration") + 4] + 1
                
                f.close()
            with open(f"{self.title}.md", 'w') as f:
                f.write(SystemData(iteration=iteration).generate_markdown() + self.generate_markdown())
                f.close()
        except:
            with open(f"{self.title}.md", 'w') as f:
                f.write(SystemData(iteration=iteration).generate_markdown() + self.generate_markdown())
                f.close()
    
    def split_text(self):
        
        cur_len = 0
        target = "\n$$"
        for i in range(len(self.task)):
            if(cur_len > 100): 
                while(self.task[i] != "."):
                    i+=1
                    target += self.task[i]
                target += '\\\\'
                cur_len = 0
            else: 
                target += self.task[i]
                cur_len+=1
        self.task = target + "\n$$"
        target = "\, ".join(self.task.split(" "))
        self.task = target
        return self.task

    def remove_duplicating_latins(self):
        target = ""
        for i in range(len(self.task)):
            if(self.task[i] in latin):
                sub = "$" + self.task[i]
                while(self.task[i] in latin):
                    sub += self.task[i]
                    i += 1
                target += sub + "$"
            else: target += self.task[i]
        self.task = target

    def dispose(self):
        self.parser.dispose()
class Parser: 
    def __init__(self, url = None) -> None:
        self.authData = AuthWorker()
        self.interface = Interface()
        self.driver = webdriver.Firefox()
        self.auth(url)

    def auth(self, url=None): 
        if(url == None):
            url = self.interface.ask_for_input(f'{url=}'.split("=")[0])[0]
        self.driver.get(url)
        self.driver.find_element(By.ID, "handleOrEmail").send_keys(self.authData.login)
        self.driver.find_element(By.ID, "password").send_keys(self.authData.password)
        self.driver.find_element(by=By.CLASS_NAME, value="submit").click()

    def save_img(self):
        page_screenshot = self.driver.get_full_page_screenshot_as_png()
        img = Image.frombytes(size=(300, 300), data=page_screenshot, mode='RGB')
        img = img.save(f"{datetime.datetime.now()}_url.jpeg")    

    def parse(self):
        # time.sleep(10)
        self.driver.implicitly_wait(60)
        title = self.driver.find_element(By.CLASS_NAME, 'title').text
        restrictions = Restrictions.fromDriver(self.driver)
        input_type = self.get_input_type()
        task = self.driver.find_element(By.XPATH, '/html/body/div[6]/div[4]/div[2]/div[3]/div[2]/div/div[2]').get_property("textContent")
        input_specification = self.driver.find_element(By.CLASS_NAME, "input-specification").text
        output_spectification = self.driver.find_element(By.CLASS_NAME, "output-specification").text
        return (title, restrictions, input_type, task, input_specification, output_spectification)

    def get_input_type(self):
        input_text = self.driver.find_element(By.CLASS_NAME, "input-file").text
        output_text = self.driver.find_element(By.CLASS_NAME, "output-file").text
        return "консоль" if(input_text == "стандартный ввод" and output_text == "стандартный вывод") else "файл"

    def dispose(self):
        self.driver.close()
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