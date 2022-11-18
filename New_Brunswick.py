import pandas as pd
import requests as re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service


def get_all_nurse_profile_links():
    # most common name letters in canada
    search_options = ['a','e','i','t','h','o','n','l']

    #find 2 combinations of letters not contains same letter
    search_options = [i+j for i in search_options for j in search_options if i != j]
    

    all_links = list()
    for search in search_options[:1]:


        url = "https://nanb.alinityapp.com/Client/PublicDirectory"
            
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(service=Service("./chromedriver"),options=options)

        driver.get(url)
        time.sleep(3)
        search_name = search

        name_button = driver.find_element(By.XPATH,value = '//*[@id="parameterformcontainer"]/div/fieldset/div/div[1]/div[1]/input').send_keys(search_name)
        search = driver.find_element(By.XPATH,value = '//*[@id="publicdirectorycontainer"]/div[4]/div[1]/div/section/div[1]/div/div/div[2]/div/button').click()
        time.sleep(10)



        next_li = driver.find_elements(By.CLASS_NAME,value = 'next')[0].get_attribute('class')
        

        while next_li == 'next':
            try:
                next_li = driver.find_elements(By.CLASS_NAME,value = 'next')[0].get_attribute('class')
            except:
                pass
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
            table = driver.find_element(By.ID,'Results')
            all_a_tags = table.find_elements(By.TAG_NAME,'a')
            for a in all_a_tags:
                try:
                    href = a.get_attribute('href')
                    class_name = a.get_attribute('class')
                    if ('/Registrant/' in href) and ("hidden" not in class_name):
                        all_links.append(href)
                    
                except:
                    pass

            try:    
                time.sleep(0.5)
                # next_page = driver.find_element(By.XPATH,value = '//*[@id="publicdirectorycontainer"]/div[4]/div[1]/div/div[2]/div[2]/div[2]/div/ul/li[8]/a').click()
                next_page = driver.find_element(By.CLASS_NAME,value = 'next').find_element(By.TAG_NAME, 'a').click()
            except:
                time.sleep(0.5)
                next_page = driver.find_element(By.XPATH,value = '//*[@id="publicdirectorycontainer"]/div[4]/div[1]/div/div[2]/div[2]/div[2]/div/ul/li[9]/a').click()

    return all_links



def get_all_nurse_details(all_links):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    nurse_details = []
    for link in all_links[:20]:
        print("---------------------------------")
        nurse_detail = {}
        driver.get(link)
        wait = WebDriverWait(driver, 10)
        text = driver.find_element(By.ID,"details").text
        raw_text = text.split("\n")
  
        try:
             nurse_detail['Name'] = raw_text[1]
        except:
            nurse_detail['Name'] = None

        try:
            nurse_detail['registration_number'] = raw_text[3]
        except:
            nurse_detail['registration_number'] = None

        try:
            nurse_detail['initial_registiration'] = raw_text[5]

        except:
            nurse_detail['initial_registiration'] = None

        try:
            nurse_detail['status'] = raw_text[8]
        except:
            nurse_detail['status'] = None

        try:
            nurse_detail['current_practice'] = raw_text[10]
        except:
            nurse_detail['current_practice'] = None

        try:
            nurse_detail['effective_time'] = raw_text[12]
        except:
            nurse_detail['effective_time'] = None

        try:
            nurse_detail['expire_date'] = raw_text[14]
        except:
            nurse_detail['expire_date'] = None


        if(raw_text[19] == "Nom de L'organisation"):
            nurse_detail['future_status'] = None
            nurse_detail['future_practice'] = None
            nurse_detail['future_effective_time'] = None
            nurse_detail['future_expire_date'] = None
            nurse_detail['organization_name'] = None
            nurse_detail['organization_address'] = None
            nurse_detail['organization_phone'] = None
        else:
            try:
                nurse_detail['future_status'] = raw_text[19]
            except:
                nurse_detail['future_status'] = None

            try:
                nurse_detail['future_practice'] = raw_text[21]
            except:
                nurse_detail['future_practice'] = None

            try:
                nurse_detail['future_effective_time'] = raw_text[23]
            except:
                nurse_detail['future_effective_time'] = None

            try:
                nurse_detail['future_expire_date'] = raw_text[25]
            except:
                nurse_detail['future_expire_date'] = None

            try:
                nurse_detail['organization_name'] = raw_text[29]
            except:
                nurse_detail['organization_name'] = None

            try:
                nurse_detail['organization_address'] = raw_text[33] + "" + raw_text[34] + "" + raw_text[35]
            except:
                nurse_detail['organization_address'] = None

            try:
                nurse_detail['organization_phone'] = raw_text[38]
            except:
                nurse_detail['organization_phone'] = None

        nurse_details.append(nurse_detail)
    return nurse_details
            

if __name__ == "__main__":
    nurse_profile_links = get_all_nurse_profile_links()
    nurse_details = get_all_nurse_details(nurse_profile_links)
    df = pd.DataFrame(nurse_details)
    df.to_csv("nurse_details.csv",index = False)


