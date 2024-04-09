
import time
import json
import string
from requests_html import *
from selenium import webdriver
from selenium.webdriver.common.by import By



# from scraper.chrome_driver_setup import driver
# from scraper.export_failed_url import export_failed_urls
# from scraper.save_image import save_image, failed_url_list
# from scraper.scraping_data import scroll_down, get_data

def save_image(url_list: list):
    with ThreadPoolExecutor() as executor:
        [executor.submit(save_image_requests, url) for url in url_list]





def save_image_requests(src, file_name):
    try:
        r = requests.get(src)

        with open(downloadFolder + f'{file_name}.jpg', 'wb') as outfile:
            
            outfile.write(r.content)
            
        # print(f'{file_name} -> Downloaded {src}')
        
    except Exception as ex:
        failed_url_list.append(src)
        print(f'Error {ex} url:{src}')


def get_data() -> list:
    url_list = []

    a_herf = driver.find_element_by_class_name(
        'serp-list serp-list_type_search serp-list_unique_yes serp-list_rum_yes serp-list_justifier_yes serp-controller__list counter__reqid clearfix i-bem serp-list_js_inited'.replace(
            ' ', '.'))

    div_list = a_herf.find_elements_by_tag_name('div')
    data_list = []
    for div in div_list:
        if div.get_attribute('data-bem') is not None:
            data_list.append(div.get_attribute('data-bem'))

    for data in data_list:
        json_data = json.loads(data)
        if 'serp-item' in json_data:
            if 'img_href' in json_data['serp-item']:
                url_list.append(json_data['serp-item']['img_href'])
    print(f'Url count:{len(url_list)}')
    return url_list


def scroll_down(size):
    scroll_pause_time = 3

    for i in range(0, size):
        # Get scroll height
        last_height = driver.execute_script(
            "return document.body.scrollHeight")

        # Scroll down to bottom
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(scroll_pause_time)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            pass

def writeTxt(number, text):
    with open(downloadFolderTxt + str(number) +'.txt', 'w') as f:
        f.write(text)
        


itStart = time.time()



url = 'https://www.rosariogarage.com/'

sections = ['Autos', 'Utilitarios', 'Camionetas', 'Camiones', 'Motos', 'cuatris-y-utvs',
            'Planes-de-ahorro', 'Embarcaciones', 'Deportes-nauticos', 'otros-nautica', 
            'Clasicos', 'Accesorios-autos', 'Accesorios-motos', 
            ]


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
            
            # #Avisos Premium Loaded
            # if div.get_attribute('class') == "col box_aviso_premium d-flex flex-column box_aviso_premium_base  loaded":
            #     avisos_premium_loaded.append(div)
        
            # #Avisos Premium
            # if div.get_attribute('class') == "col box_aviso_premium d-flex flex-column box_aviso_premium_base ":
            #     avisos_premium.append(div)
        
            # #Avisos No Premium Loaded
            # if div.get_attribute('class') == "col box_aviso_base  d-flex flex-column box_aviso_no_premium  loaded":
            #     avisos_no_premium_loaded.append(div)
        
            # #Avisos No Premium
            # if div.get_attribute('class') == "col box_aviso_base  d-flex flex-column box_aviso_no_premium ":
            #     avisos_no_premium.append(div)
        
            #precio bg-dark-gray
            if div.get_attribute('class') == "precio bg-dark-gray ":
                a = div.find_elements_by_tag_name('a')
                for elem in a:
                    url_avisos.append(elem.get_attribute('href'))
                
        # print('Avisos Premium Loaded', len(avisos_premium_loaded))
        # print('Avisos Premium', len(avisos_premium))
        # print('Avisos No Premium Loaded', len(avisos_no_premium_loaded))
        # print('Avisos No Premium', len(avisos_no_premium))
        print('Urls scrapeadas:', len(url_avisos))
    except: pass
    driver.quit()
    
    
    
    try:
        contents = []
        count = 0
        for url in url_avisos:
            r = requests.get(url)
            contents.append(r.content)
            print('request', count)
                
            if count > 10: break
            count+=1
            
    except: pass


    
    
    time.sleep(2)
    
    

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
    
