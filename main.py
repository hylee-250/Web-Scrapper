import os
import csv
import requests
from bs4 import BeautifulSoup
def save_to_csv(brand_name,brand_info):
  file = open(f"{brand_name}.csv",mode="w")
  writer = csv.writer(file)
  writer.writerow(["location","company","time","pay","date"])
  for alba in brand_info:
    writer.writerow(alba)
  return
os.system("clear")
alba_url = "http://www.alba.co.kr"
links =[]
brand_names=[]
def all_csv_delete():
    dir_name = os.path.dirname(os.path.realpath("__file__"))
    test = os.listdir(dir_name)
    for item in test:
        if item.endswith(".csv"):
            os.remove(os.path.join(dir_name, item))
all_csv_delete()
def extract_brand():
  alba_request = requests.get(alba_url)
  alba_soup = BeautifulSoup(alba_request.text,"html.parser")
  alba_super_brands = alba_soup.find("div",{"id":"MainSuperBrand"})
  #alba_brand = alba_super_brands.find("ul",{"class":"goodsBox"})
  brands = alba_super_brands.find_all("li",{"class":"first impact"})
  brands2 = alba_super_brands.find_all("li",{"class":"impact"})
  #company = brand.find("span",{"class":"company"})
  #link = brand.find("a",{"class":"brandHover"})
  for brand in brands:
    links.append(brand.find("a")["href"])
    brand_names.append(brand.find("span",{"class":"company"}).text)
  for brand in brands2:
    links.append(brand.find("a")["href"])
    brand_names.append(brand.find("span",{"class":"company"}).text)
# brand_names, links 나열
location=[]
company = []
time=[]
pay=[]
date=[]
brand_info = []
#브랜드가 정해지고 난 후
def extract_alba(URL):
  location=[]
  company = []
  time=[]
  pay=[]
  date=[]
  alba_request = requests.get(URL)
  alba_soup = BeautifulSoup(alba_request.text,"html.parser")
  alba_locat = alba_soup.find_all("td",{"class":"local first"})
  alba_title = alba_soup.find_all("td",{"class":"title"})
  alba_time = alba_soup.find_all("td",{"class":"data"})
  alba_pay = alba_soup.find_all("td",{"class":"pay"})
  alba_date = alba_soup.find_all("td",{"class":"regDate last"})
  if alba_title:
    company = []
    for span in alba_title:
      company.append(span.find("span",{"class":"company"}).get_text())
  if alba_locat:
    location=[]
    for td in alba_locat:
      location.append(td.get_text().replace("\xa0"," "))
  if alba_time:
    time=[]
    for span in alba_time:
      try:
        time.append(span.find("span",{"class":"time"}).get_text())
      except AttributeError:
        pass
  if alba_pay:
    pay=[]
    for span in alba_pay:
      if span.find("span",{"class":"payIcon hour"}):
        pay.append(span.find("span",{"class":"payIcon hour"}).get_text()+ span.find("span",{"class":"number"}).get_text())
      if span.find("span",{"class":"payIcon week"}):
        pay.append(span.find("span",{"class":"payIcon week"}).get_text()+ span.find("span",{"class":"number"}).get_text())
      if span.find("span",{"class":"payIcon month"}):
        pay.append(span.find("span",{"class":"payIcon month"}).get_text()+ span.find("span",{"class":"number"}).get_text())
      if span.find("span",{"class":"payIcon year"}):
        pay.append(span.find("span",{"class":"payIcon year"}).get_text()+ span.find("span",{"class":"number"}).get_text())
  if alba_date:
    date=[]
    for span in alba_date:
      if type(span.find("strong")) == "NoneType":
        date.append(span.find("strong").get_text())
      else:
        date.append(span.get_text())
  brand_info = []
  for i in range(len(location)):
    try:
      brand_info.append([location[i],company[i],time[i],pay[i],date[i]])
    except IndexError:
      pass
  return brand_info
extract_brand()
for i,link in enumerate(links):
  print(f"extracting {brand_names[i]}...")
  brand_info = []
  a = extract_alba(link)
  save_to_csv(brand_names[i],a)