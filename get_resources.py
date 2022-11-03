import re
from rich.table import Table
from rich.console import Console
from rich.progress import track
import os

console = Console()

# {имя: ссылка}
refs = {} 

# чистим прошлые ссылки
def prepare():
    with open('all resources.md', 'w') as file:
        file.close()
def check_bottom(dir, files):
    try: 
        dirs = os.listdir(f'./{dir}')
        if len(dirs) != 0: 
            for i in track(dirs, description=f"checking: {dir}"):
                if len(list(filter(lambda x: x =='.', i))) == 0: 
                    check_bottom(f'./{dir}/{i}', files)
                else: 
                    files.append(f'./{dir}/{i}')
    except: 
        console.print("not a directory")
# идем по всем .мд файлам 
# возвращаем каждый мд как строку 
def check_files():
    directories = os.listdir('./')
    directories = list(filter( lambda x :  x[0] != '.', directories))
    files = []
    for i in directories:
        check_bottom(i, files=files)
    for i in files:
        if i[-2::] != 'md':
            files.remove(i)
    files.remove('./схемотехника/jk-trigger.jpg')
    return files

# в строках ищем ссылки по правилу:
# [что-то](http...)
def get_refs(files: list) -> list:
    target = []
    regex = '/\[([^\[]+)\](\(.*\))/gm'
    for i in files:
        with open(i, 'r') as file: 
            data = file.read()
            target.append([file.name, re.search(regex, data)])
        file.close()
    for i in target:
        if i[1] != None:
            i[1] = i[1].string
    return target

# из полученных строк-ссылок cоздаем пары для refs и закидываем их в all resources.md
def add_refs():
    for i in get_refs(check_files()):
        if i[1] != None:
            refs[i[0]] = i[1]
    with open('all resources.md', 'w') as file: 
        table = Table()
        table.add_column("name")
        table.add_column("url")
        for i in refs:
            table.add_row(str(i), str(refs[i]))
            file.write(f'[{i}]({refs[i]})\n')
        console.print(table)
        file.close()
    


def main():
    prepare()
    add_refs()
if __name__ == "__main__" :
    main()