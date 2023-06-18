import datetime
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

#Fix
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# set options to be headless, ..
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager


#Get bot selenium make sure you can access google chrome

keyword = input("ใส่ keyword : ")


url = "https://www.lazada.co.th/catalog/?q={}".format(keyword)
# page_end = int(input("กรุณาใส่เลขหน้าที่จะดึง หน้าปลายทาง : "))
file_name = input("ใส่ชื่อไฟล์ : ")





from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

product_name = []
base_price_lis = []
sell_price_lis = []
link_lis = []
quant_lis = []

driver.get(url)

for i in range(3):
    driver.execute_script("window.scrollBy(0,5000)")
time.sleep(5)
soup = BeautifulSoup(driver.page_source,'html.parser')
print(soup.prettify())


name_lis = []
desc_lis = []
base_price_lis = []
sell_price_lis = []
item_link_lis = []
image_lis = []
rating_count_lis = []
sell_total_lis = []

item_lis = soup.find_all("div",{'class':'Bm3ON'})
for i in item_lis: 
    name = i.find('img',{'class':'jBwCF'})['alt']
    print(name)
    name_lis.append(name)


    link = i.find('a')
    print(link['href'])
    item_link_lis.append(link['href'])

    image = i.find('div',{'class':'picture-wrapper'}).find('img',{'class':'jBwCF'})
    print(image['src'])
    image_lis.append(image['src'])

    #=== Scrape Description ============
    driver.get(link['href'])
    


    desc = i.find('div',{'class':'RfADt'})
    print(desc.text)
    desc_lis.append(desc.text)

    sell_price = i.find('div',{'class':'aBrP0'})
    print(sell_price.text)
    sell_price_lis.append(sell_price.text)

    sell_total = i.find('div',{'class':'_6uN7R'}).text 
    print(sell_total)

    sell_total_lis.append(sell_total)

df = pd.DataFrame()
df['ชื่อสินค้า'] = name_lis 
df['รายละเอียดสินค้า'] = desc_lis 
df['ราคาขาย'] = sell_price_lis 
df['รูปสินค้า'] = image_lis 
df['ลิงค์สินค้า'] =item_link_lis 
df['จำนวนที่ขายไปแล้ว'] = sell_total_lis 




df.to_excel("{}.xlsx".format(file_name))

driver.close()

