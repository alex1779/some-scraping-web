
import time
# import json

from requests_html import *
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor
from RPA.Excel.Files import Files


url = 'https://www.rosariogarage.com/'
sections = ['Autos', 'Utilitarios', 'Camionetas', 'Motos', 'Embarcaciones', 'Clasicos',
            'Camiones', 'Telefonia', 'Electronica', 'Hogar', 'Deportes', 'Indumentaria', 
            'Informatica', 'Instrumentos Musicales', 'Planes de Ahorro', 'Deportes Nauticos', 'Accesorios para Motos', 'Otros (Nautica', 
            'Herramientas', 
            
              'cuatris-y-utvs',
            'Planes-de-ahorro',  'Deportes-nauticos', 'otros-nautica', 
             'Accesorios-autos', 'Accesorios-motos']

rubro_id =[107, 108, 109, 110, 111, 113, 
           128, 129, 130, 131, 132, 133, 
           134, 135, 136, 137, 138, 139, 
           142, ]


class MyClass():
    count = None
    contents = []
    
def get_requests(url):
       try:
           response  = requests.get(url)
           contents.append(response.content)
           # print(response.encoding)
           # print('Getting request:', MyClass.count)
           MyClass.count+=1
       except Exception as ex:
           print(f'Error {ex} url:{url}')
     

try:
    print('Getting urls..')
    itStart = time.time() 
    driver = webdriver.Chrome('C:/chromedriver.exe')
    # driver.maximize_window()
    driver.minimize_window()
    
    
    driver.get(url+sections[0])


    pages = []
    url_avisos = []
    
    selects = driver.find_elements_by_tag_name('select')  
    for select in selects:
        if select.get_attribute('class') == "pager04":
            options = select.find_elements_by_tag_name('option')
            for option in options:
                value =  option.get_attribute('value')
                pages.append(value)
            break   
              
        
    for page in pages:
        url_part = 'https://www.rosariogarage.com/index.php?&action=carro/showRubro&rbrId=108&o='
        driver.get(url_part+str(page))
        time.sleep(1)
        div_list = driver.find_elements_by_tag_name('div')
        for div in div_list:
            if div.get_attribute('class') == "precio bg-dark-gray ":
                a = div.find_elements_by_tag_name('a')
                for elem in a:
                    url_avisos.append(elem.get_attribute('href'))
    
    
    
    # print('Urls:', len(url_avisos))
    # print('Seconds:', round(itProcess))
except: pass
driver.quit()


try:
    print('Pull requests..')
    itStart = time.time()
    contents = []
    MyClass.count = 0

    with ThreadPoolExecutor(max_workers=10) as exe:
        [exe.submit(get_requests, url) for url in url_avisos]
    
    itProcess = time.time()-itStart
    # print('Seconds:', round(itProcess))
        
except Exception as ex: 
    print(ex)
    pass



try:
    print('Decoding info..')
    itStart = time.time()
    data = []
    count = 0
    for content in contents:
        text = content.decode("iso-8859-1")
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
        # print('Nombre: ' + str(text[0]) + ' Provincia: ' + str(text[1]) + ' Ciudad: ' + str(text[2]) + ' Celular: ' + str(text[3]))
        data.append(text)
        count+=1
    itProcess = time.time()-itStart
    # print('Seconds:', round(itProcess))
        
except Exception as ex: 
    print(ex)
    pass


try:
    
    itStart = time.time()
    excel_lib = Files()
    excel_lib.create_workbook("C:/Users/Ale/Google Drive/Programacion/Python/Scraping Web/RosarioGarage.xlsx",fmt='xlsx')
    excel_lib.rename_worksheet(excel_lib.get_active_worksheet(), "Autos")
    excel_lib.set_cell_value(1, 1, 'Nombre')
    excel_lib.set_cell_value(1, 2, 'Provincia')
    excel_lib.set_cell_value(1, 3, 'Ciudad')
    excel_lib.set_cell_value(1, 4, 'Celular')
    excel_lib.set_cell_value(1, 5, 'Link')
    count = 0
    for item in data:
        excel_lib.set_cell_value(count+2, 1, item[0])
        excel_lib.set_cell_value(count+2, 2, item[1])
        excel_lib.set_cell_value(count+2, 3, item[2])
        excel_lib.set_cell_value(count+2, 4, item[3])
        excel_lib.set_cell_value(count+2, 5, url_avisos[count])
        count+=1
    excel_lib.save_workbook("C:/Users/Ale/Google Drive/Programacion/Python/Scraping Web/RosarioGarage.xlsx")
    itProcess = time.time()-itStart
    print('Excel File Saved!')
    # print('Seconds:', itProcess)
        
except Exception as ex: 
    print(ex)
    pass




    
