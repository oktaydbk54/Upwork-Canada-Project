import requests
from bs4 import BeautifulSoup
import pandas as pd

def getPageUrls(name):
    page = requests.get(f"https://nurses.ab.ca/find-a-nurse?FirstName={name}&LastName=")
    soup = BeautifulSoup(page.content, 'html.parser')
    links = soup.find_all('a', href=True)
    links = [link['href'] for link in links if '/find-a-nurse/details?id=' in link['href']]
    return links

def getDetailsOfNurseFromURL(url):
    nurseData = {}
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    details_container = soup.find("div",{"class","g-3"})

    name = soup.find("div",{"class","body-full-screen"}).find('p').text
    
    nurseData['Name'] = name
    details = [detail for detail in details_container.findAll("div",{"class","col-md-6"})]
    for count,value in enumerate(details):
        if(count % 2 == 0):
            key = value.text.replace(":","").replace("\n","").replace("\r","").strip()
            valueOfKey = details[count+1].text.replace(":","").replace("\n","").replace("\r","").strip()
            nurseData[key] = valueOfKey
    
    return nurseData
        
if __name__ == "__main__":
    search_options = ['a','e','i','t','h','o','n','l']

    #find 2 combinations of letters not contains same letter
    search_options = [i+j for i in search_options for j in search_options if i != j]
    nurseDatas = []

    for search in search_options:
        links = getPageUrls(search)
        print("Links: ",len(links))
        nurseData = [getDetailsOfNurseFromURL("https://nurses.ab.ca/"+link) for link in links[:2]]
        nurseDatas = nurseDatas + nurseData
    
    df = pd.DataFrame(nurseDatas)
    df.to_csv("nurses.csv",index=False)
    print(nurseData)



