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
from selenium.webdriver.chrome.service import Service

#Get bot selenium make sure you can access google chrome
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

keyword = input("ใส่ keyword : ")
file_name = input("ใส่ชื่อไฟล์ : ")
start = int(input("ใส่หน้าเริ่มต้น : "))
end = int(input("ใส่หน้าสุดท้าย : "))

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


# page_end = int(input("กรุณาใส่เลขหน้าที่จะดึง หน้าปลายทาง : "))


prov_lis = []
sell_price_lis = []
name_lis = []
desc_lis = []
base_price_lis = []
item_link_lis = []
image_lis = []
rating_count_lis = []
sell_total_lis = []
total_review_lis = []
score_lis = []
# for i in range(2):
#     driver.execute_script("window.scrollBy(0,5000)")
# time.sleep(5)

for page in range(start,end+1):
    url = "https://www.lazada.co.th/catalog/?page={}&q={}".format(page,keyword)

    driver.get(url)

    soup = BeautifulSoup(driver.page_source,'html.parser')
    print(soup.prettify())



    item_lis = soup.find_all("div",{'class':'Bm3ON'})

    for i in item_lis: 
        name = i.find('div',{'class':'picture-wrapper'}).find('img')['alt']
        print(name)
        name_lis.append(name)

        try:
            total_review = i.find('span',{'class':'qzqFw'}).text 
        except: 
            total_review = 0

        print('Review : ',total_review)

        total_review_lis.append(total_review)

        link = i.find('a')
        print(link['href'])
        item_link_lis.append("https:"+link['href'])

        image = i.find('div',{'class':'picture-wrapper'}).find('img')
        print(image['src'])
        image_lis.append(image['src'])

        #=== Scrape Description ============
        driver.get(link['href'])
        
        try:
            sell_total = i.find('span',{'class':'_1cEkb'}).text 
            print(sell_total)
        except: 
            sell_total = 0
        sell_total_lis.append(sell_total)
        
        print('Sell Total Lis : ',sell_total_lis)
        
        # try:
        #     desc = i.find('div',{'class':'pdp-product-desc'}).text
        #     print(desc)
        # except: 
        #     desc = "-"
        #     print(desc)
        # desc_lis.append(desc)

        try: 
            province = i.find('span',{'class':'oa6ri'}).text 
            print('Province : ',province)
        except:
            province = "-"
            print('Province : ',province)
        prov_lis.append(province)

        sell_price = i.find('div',{'class':'aBrP0'})
        print(sell_price.text)
        sell_price_lis.append(sell_price.text)

        # score = i.find('div',{'class':'score'}).text 
        # print(score)
        # score_lis.append(score)


df = pd.DataFrame()
df['ชื่อสินค้า'] = name_lis 
df['จังหวัด'] = prov_lis
df['ราคาขาย'] = sell_price_lis 
df['ลิงค์สินค้า'] =item_link_lis 
df['จำนวนที่ขายไปแล้ว'] = sell_total_lis 
df['จำนวนรีวิว'] = total_review_lis 

df['รูปสินค้า'] = image_lis 
# df['คะแนนรีวิว'] = score_lis
# df['รายละเอียดสินค้า'] = desc_lis




df.to_excel("{}.xlsx".format(file_name))

driver.close()
