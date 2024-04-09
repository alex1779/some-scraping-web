# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 19:34:35 2022

@author: Ale
"""

import os
import sys
import datetime
import requests_html
from concurrent.futures import ThreadPoolExecutor
from RPA.Excel.Files import Files

class MyClass():
    url = 'https://www.rosariogarage.com/index.php?&action=carro/showRubro&rbrId='
    sections = [['Autos', 107], ['Utilitarios', 108], ['Camionetas', 109], ['Motos', 110],['Embarcaciones', 111], 
            ['Clásicos', 113], ['Camiones y Grúas', 128], ['Telefonía', 129], ['Electrónica', 130], ['Hogar', 131],
            ['Deportes', 132], ['Indumentaria', 133], ['Informatica', 134], ['Instrumentos Musicales', 135],
            ['Planes de Ahorro', 136], ['Deportes Náuticos', 137], ['Accesorios para Motos', 138], ['Otros (Náutica)', 139],
            ['Herramientas', 142], ['Artículos para Bebé', 143], ['Cuatris y UTVs', 144], ['Accesorios para Autos', 116], 
            ['Otros', 123]]
    
    sections2 = [['Utilitarios', 108], ['Deportes Náuticos', 137]]
    sections_selected = []
    count = None
    contents = []
    indices = []
    pages = []
    url_avisos = []
    data = []
    verbose = False
    NombreyCelu = []
    FirstTime = False
    counter_request = 0
    rubros = None

def get_current_dictory():
    current_dictory = os.getcwd()
    return current_dictory

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
        MyClass.FirstTime = True

def printnew(text):
    sys.stdout.write("\r")
    sys.stdout.write("\r" + text)
    sys.stdout.flush()

def get_requests(url):
        try:
            MyClass.counter_request +=1  
            percent = str(round((MyClass.counter_request * 100)/len(MyClass.url_avisos)))
            printnew('Consultando datos en la web..[' + percent + '%]')
            response  = requests_html.requests.get(url)
            MyClass.contents.append(response.content)
            response.close()
        except Exception as ex:
            print(f'Error {ex} url:{url}')
            
            
def start():
    create_folder(get_current_dictory() + '/Output')
    
    print('Bienvenido a mi Programa!')
    print('[Busca en la carpeta "Output" los resultados]')
    print(MyClass.sections)
    MyClass.rubros = input('Por favor ingrese los rubro/s que desea separados por coma (código/s) (ingrese "a" para seleccionar todos los rubros): ')
    if MyClass.rubros == "a":
        MyClass.sections_selected = MyClass.sections
    else:
        MyClass.rubros = MyClass.rubros.replace(" ", "")
        MyClass.rubros = MyClass.rubros.split(',')
        for i in MyClass.rubros:
            for s in MyClass.sections:
                if int(i) == int(s[1]):
                    MyClass.sections_selected.append(s)
        
        
def get_Pages_Sections(section):
    try:
        print('Obteniendo datos de la sección: "'+ str(section[0])+'".')
        MyClass.url_avisos = []
        MyClass.contents = []
        MyClass.data = []
        getIndex(MyClass.url + str(section[1]))
        
        if MyClass.indices == []:
            getAvisos(MyClass.url+str(section[1]))
        else:
            for indice in MyClass.indices:
                getAvisos(MyClass.url+str(section[1])+'&o='+str(indice))
        print('Hay "'+ str(len(MyClass.url_avisos)) +'" avisos en la sección "' + str(section[0]) +'".')
        
    except Exception as ex: 
        print(ex)
        pass         
            
def getIndex(url):
    MyClass.indices = []
    response  = requests_html.requests.get(url)
    text = response.content
    response.close()
    text = text.decode("iso-8859-1")
    if not 'class="pager04">' in text:
        MyClass.indices = []
        if MyClass.verbose: print('La sección  no contiene páginas.')
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
        if MyClass.verbose: print('La sección contiene ' + str(len(MyClass.indices)) + ' páginas.')
    # print(MyClass.indices)


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
    

def decodingInfo():
    try:
        for content in MyClass.contents:
            text = content.decode("iso-8859-1")
            title = description = price = text
            
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
            text.append(title)
            text.append(price)
            text.append(description)
            # print('Nombre: ' + str(text[0]) + ' Provincia: ' + str(text[1]) + ' Ciudad: ' + str(text[2]) + ' Celular: ' + str(text[3]))
            MyClass.data.append(text)
        if MyClass.verbose: print('Hay '+ str(len(MyClass.data)) +' datos.')
    except Exception as ex: 
        if MyClass.verbose: print(ex)
        pass

def pull_Requests():
    try:
        MyClass.counter_request = 0
        with ThreadPoolExecutor(max_workers=10) as exe:
            [exe.submit(get_requests, url) for url in MyClass.url_avisos]
    except Exception as ex: 
        if MyClass.verbose: print(ex)
        pass

def create_excel_file(section):
    try:
        print('\nCreando libro Excel..')
        MyClass.NombreyCelu = []
        date = datetime.datetime.now().strftime("%d-%m-%Y")
        name_worksheet = get_current_dictory() + '/Output/' + 'Rosario Garage '+section[0]+' '+date+'.xlsx' 
        excel_lib = Files()
        excel_lib.create_workbook(name_worksheet,fmt='xlsx')
        excel_lib.rename_worksheet(excel_lib.get_active_worksheet(), section[0])
        excel_lib.set_cell_value(1, 1, 'Nombre')
        excel_lib.set_cell_value(1, 2, 'Provincia')
        excel_lib.set_cell_value(1, 3, 'Ciudad')
        excel_lib.set_cell_value(1, 4, 'Celular')
        excel_lib.set_cell_value(1, 5, 'Titulo')
        excel_lib.set_cell_value(1, 6, 'Precio')
        excel_lib.set_cell_value(1, 7, 'Descripcion')
        excel_lib.set_cell_value(1, 8, 'Link')
        
        count = 0
        for item in MyClass.data:
            excel_lib.set_cell_value(count+2, 1, item[0])
            excel_lib.set_cell_value(count+2, 2, item[1])
            excel_lib.set_cell_value(count+2, 3, item[2])
            excel_lib.set_cell_value(count+2, 4, item[3])
            excel_lib.set_cell_value(count+2, 5, item[4])
            excel_lib.set_cell_value(count+2, 6, item[5])
            excel_lib.set_cell_value(count+2, 7, item[6])
            excel_lib.set_cell_value(count+2, 8, MyClass.url_avisos[count])
            
            if item[3] != '':
                MyClass.NombreyCelu.append(item[0] + ', ' + item[3] + ', ' + item[1]  + ', ' + item[2]  )
            
            count+=1
        excel_lib.save_workbook(name_worksheet)
        print('Excel File Guardado!')
            
    except Exception as ex: 
        print(ex)
        pass
    
def save_Data_Txt():
    try:
        MyClass.NombreyCelu.sort()
        with open(get_current_dictory() + '/Output/' + 'names.txt', 'w') as f:
            for item in MyClass.NombreyCelu:
                f.write(item + '\n') 
        lines = open(get_current_dictory() + '/Output/' + 'names.txt', 'r').readlines()
        lines_set = set(lines)
        lis = sorted(lines_set)
        print('Total contacts ',len(lis))
        out = open(get_current_dictory() + '/Output/' + 'names2.txt', 'w')
        for line in lis:
            out.write(line)
        out.close()
        os.replace(get_current_dictory() + '/Output/' + 'names2.txt',get_current_dictory() + '/Output/' + 'names.txt')
    except Exception as ex: 
        print(ex)
        pass
    


def main():
    start()
    for section in MyClass.sections_selected:
        try:
            get_Pages_Sections(section)
            pull_Requests()
            decodingInfo()
            create_excel_file(section)
            # save_Data_Txt()
            
        except Exception as ex:
            print(ex)
            continue
        
if __name__ == "__main__":
    main()

            
        
