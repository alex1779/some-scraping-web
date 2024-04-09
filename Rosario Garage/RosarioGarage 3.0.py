
import time
from selenium import webdriver
from RPA.Excel.Files import Files


itStart = time.time()
url = 'https://www.rosariogarage.com/'
sections = ['Autos', 'Utilitarios', 'Camionetas', 'Camiones', 'Motos', 'cuatris-y-utvs',
            'Planes-de-ahorro', 'Embarcaciones', 'Deportes-nauticos', 'otros-nautica', 
            'Clasicos', 'Accesorios-autos', 'Accesorios-motos']



#> Contar y Seleccionar paginas del rubro
#> Extraer links por cada aviso
#> Por cada aviso extraer la info
#> Exportar a planilla excel



excel_lib = Files()
excel_lib.create_workbook("C:/Users/Ale/Google Drive/Programacion/Python/Scraping Web/RosarioGarage.xlsx",fmt='xlsx')
excel_lib.rename_worksheet(excel_lib.get_active_worksheet(), "Autos")

excel_lib.set_cell_value(1, 1, 'Nombre')
excel_lib.set_cell_value(1, 2, 'Provincia')
excel_lib.set_cell_value(1, 3, 'Ciudad')
excel_lib.set_cell_value(1, 4, 'Celular')
excel_lib.set_cell_value(1, 5, 'Link')

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
            if len(text[3]) > 20: text[3] = ""
            
            print('Nombre: ' + str(text[0]) + ' Provincia: ' + str(text[1]) + ' Ciudad: ' + str(text[2]) + ' Celular: ' + str(text[3]))
           
            excel_lib.set_cell_value(url_count+1, 1, text[0])
            excel_lib.set_cell_value(url_count+1, 2, text[1])
            excel_lib.set_cell_value(url_count+1, 3, text[2])
            excel_lib.set_cell_value(url_count+1, 4, text[3])
            excel_lib.set_cell_value(url_count+1, 5, url)
            
            # if url_count == 10: break
        
            url_count += 1
        
        excel_lib.save_workbook("C:/Users/Ale/Google Drive/Programacion/Python/Scraping Web/RosarioGarage.xlsx") 
            
    except Exception as ex:
        print(ex)
        pass
    
    driver.quit()

    itProcess = time.time()-itStart


    print('time:', itProcess)


except Exception as ex:
    print(ex)
    # driver.quit()


    


    
