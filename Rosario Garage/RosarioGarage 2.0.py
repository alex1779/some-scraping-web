
import time
import json
import string
from requests_html import *
from selenium import webdriver
from selenium.webdriver.common.by import By

itStart = time.time()
url = 'https://www.rosariogarage.com/'
sections = ['Autos', 'Utilitarios', 'Camionetas', 'Camiones', 'Motos', 'cuatris-y-utvs',
            'Planes-de-ahorro', 'Embarcaciones', 'Deportes-nauticos', 'otros-nautica', 
            'Clasicos', 'Accesorios-autos', 'Accesorios-motos']



#> Contar y Seleccionar paginas del rubro
#> Extraer links por cada aviso
#> Por cada aviso extraer la info


try:

    driver = webdriver.Chrome('C:/chromedriver.exe')
    driver.maximize_window()
    driver.get(url+sections[0])
    
    try:
        avisos_premium_loaded = []
        avisos_premium = []
        avisos_no_premium_loaded = []
        avisos_no_premium = []
        url_avisos = []
        div_list = driver.find_elements_by_tag_name('div')
        for div in div_list:
            if div.get_attribute('class') == "precio bg-dark-gray ":
                a = div.find_elements_by_tag_name('a')
                for elem in a:
                    url_avisos.append(elem.get_attribute('href'))
        print('Urls:', len(url_avisos))
    except: pass
    

    try:
        url_count = 1
        for url in url_avisos:
            driver.get(url)
            div_list = driver.find_elements_by_tag_name('div')
            text_box = []
            for div in div_list:
                if div.get_attribute('class') == "box-text":
                    text_box.append(div)
                    
            text = text_box[3].get_attribute('innerHTML')
            text = text.split('<br>',4)
            text[1] = text[1].replace("<span>Provincia: </span> ", "")
            text[2] = text[2].replace("<span>Ciudad: </span> ", "")
            text[3] = text[3].replace("<span>Celular:</span> ", "")
            text[3] = text[3].replace(" ", "")
            
            print(url_count, '********************' )
            print('Nombre:',text[0] )
            print('Provincia:',text[1] )
            print('Ciudad:',text[2] )
            print('Celular:',text[3] )
            
            url_count += 1
            if url_count == 10: break
            
    except: pass


    
    
    time.sleep(2)
    
    driver.quit()

except Exception as ex:
    print(ex)
    # driver.quit()


    
    
#     for i in range(1000):
#         print('trying..',number )
#         driver.get('https://web.whatsapp.com/send?autoload=1&app_absent=0&phone=' + str(number) + '&text')
        
#         if not firstTime:
#             time.sleep(20)
#             firstTime = True
#         else:
#             
#         try:
#             div_list = driver.find_elements_by_tag_name('div')
#             for div in div_list:
#                 if div.get_attribute('id') == 'main':
#                     div_list2 = div.find_elements_by_tag_name('div')
#                     for div2 in div_list2:
#                         if div2.get_attribute('title') == 'Detalles del perfil':
#                             div2.click()
#                             time.sleep(1)
#                             driver.save_screenshot(downloadFolderMedia + str(number) + '(1).jpg')
        
#             #Go for info
#             div_list = driver.find_elements_by_tag_name('div')
            
#             for div in div_list:
#                 if div.get_attribute('data-testid') == 'contact-info-drawer':
#                       # Go for image
#                       imgs = div.find_elements_by_tag_name('img')
#                       for img in imgs:
#                           img.click()
#                           time.sleep(1)
#                           driver.save_screenshot(downloadFolderMedia + str(number) + '(2).jpg')
#                           break
#         except:
#             # writeTxt(number, 'no tiene whatsapp')
#             number +=1
#             continue
                    
#         number +=1

    # itProcess = time.time()-itStart


    # print('time:', itProcess)
    
