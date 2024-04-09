# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 15:23:21 2022

@author: Ale
"""

import os
import time
import datetime
import requests_html
from concurrent.futures import ThreadPoolExecutor
from RPA.Excel.Files import Files

class MyClass():
    url = 'https://www.rosariogarage.com/index.php?&action=carro/showRubro&rbrId='
    sections2 = [['Planes de Ahorro', 136], ['Deportes Náuticos', 137]]
    count = None
    contents = []
    indices = []
    pages = []
    url_avisos = []
    data = []
    verbose = False
    NombreyCelu = []

def start():
        
    url = MyClass.url + str(MyClass.sections2[0][1])
    response  = requests_html.requests.get(url)
    text = response.content
    text = text.decode("iso-8859-1")
    response.close()
    if not 'class="pager04">' in text:
        MyClass.indices = []
    else:
        text = text.split('class="pager04">')[-1]
        text = text.split('</select>')[0]
        text = text.split('<option value=')
        count = 0
        for t in text:
            if len(t) == 0:
                text.pop(count)
            try:
                text[count] = text[count].replace("</option>", "")
                text[count] = text[count].replace("selected", "")
            except: pass
            text[count] = text[count].split('>')[0]
            text[count] = text[count].replace(" ", "")
            MyClass.indices = text
            count+=1
        MyClass.indices = text

def getAvisos(url):
    response  = requests_html.requests.get(url)
    text = response.content
    text = text.decode("iso-8859-1")
    text = text.split('<div class="precio bg-dark-gray ">')
    count = 0
    for t in text:
        if len(t) == 0:
            text.pop(count)
        if len(t) > 1500:
            text.pop(count)  
        try:
            text[count] = text[count].replace("\n<a href=", "")
            text[count] = text[count].split('>\n')[0]
            text[count] = text[count].replace('"', "")
            text[count] = text[count].replace('<a href=', "")
        except: pass
        count+=1
    for t in text:
        MyClass.url_avisos.append(t)
        
start()     
getAvisos(MyClass.url + str(MyClass.sections2[0][1]))

response  = requests_html.requests.get('https://www.rosariogarage.com/index.php?action=carro/showProduct&itmId=3640621&rbrId=113')
text = response.content
response.close()

text = text.decode("iso-8859-1")
title = description = price = text

with open(os.getcwd() + 'data.txt', 'w') as f:
    f.write(text) 


title = title.split('main-title bg-light-gray')[1]
title = title.split("<h1>")[1]
title = title.split("</h1>")[0]
description = description.split('Descripci&oacute;n ampliada')[1]
description = description.split('</div>')[1]
description = description.replace('<div class="box-text">', "")
description = description.replace("\n", " ")
description = description.replace("<br />", "")
price = price.split('class="subtitle">Precio</div><div class="box-text">', maxsplit=1)[1]
price = price.split('</div>', maxsplit=1)[0]


text = text.split("Ver Mail", maxsplit=1)[0]
text = text.split("Datos de contacto", maxsplit=1)[1]
text = text.split('<br>', maxsplit=4)
text[0] = text[0].replace('</div><div class="box-text">', "")
text[0] = text[0].replace('<i class="fa "></i>', "")
text[1] = text[1].replace("<span>Provincia: </span> ", "")
text[1] = text[1].replace("<span>Direcci&oacute;n:</span>", "")
text[2] = text[2].replace("<span>Ciudad: </span> ", "")
text[2] = text[2].replace("<span>Provincia: </span> ", "")
text[3] = text[3].replace("<span>Celular:</span> ", "")
text[3] = text[3].replace(" ", "")
if len(text[3]) > 15: text[3] = ""
text[0] = text[0].title()
text[1] = text[1].title()
text[2] = text[2].title()
text.pop(4)

# text.append(title)
# text.append(price)
# text.append(description)

print(text)

# print('Nombre: ' + str(text[0]) + ' Provincia: ' + str(text[1]) + ' Ciudad: ' + str(text[2]) + ' Celular: ' + str(text[3]))

# print(title)
# print(description)
# print(price)

print(len(text))





































