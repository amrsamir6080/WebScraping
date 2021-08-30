import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

jop_title = []
company_name = []
loc = []
skls = []
links = []
salary = []
res =[]
date = []
page_number = 0

while True:
    # get the link
    try:
        result = requests.get(f"https://wuzzuf.net/search/jobs/?a=hpb&q=python&start={page_number}")

            # save page content
        src = result.content

            #creat soup object to parse page content
        soup = BeautifulSoup(src , "lxml")

        limit = int(soup.find("strong").text)
        if (page_number > limit // 15):
            break

        jop_titles = soup.find_all("h2" , {"class":"css-m604qf"})
        company_names = soup.find_all("a" , {"class":"css-17s97q8"})
        locations = soup.find_all("span",{"class":"css-5wys0k"})
        skills = soup.find_all("div",{"class":"css-y4udm8"})
        posted_new = soup.find_all("div" , {"class":"css-4c4ojb"})
        posted_old = soup.find_all("div" , {"class":"css-do6t5g"})
        posted = [*posted_new , *posted_old]

        for i in range(len(jop_titles)):
            jop_title.append(jop_titles[i].text)
            links.append(jop_titles[i].find("a").attrs['href']) # can do by just write .a.arrts
            company_name.append(company_names[i].text)
            loc.append(locations[i].text)
            skls.append(skills[i].text)
            date_txt = posted[i].text.replace("-","").strip()
            date.append(date_txt)

        page_number += 1
        print("page switched")
    except:
        print(" Error ")


for link in links:
    result = requests.get(link)
    src = result.content
    soup = BeautifulSoup(src , "lxml")
    salaries = soup.find("div" , {"class":"css-rcl8e5"})
    salary.append(salaries.text.strip())
    responsabilities = soup.find("div",{"class":"css-1t5f0fr"}).find("ul") #cna do just .ul
    respon_text = ""
    for txt in responsabilities.find_all("li"):
        respon_text += txt.text+"| "
    respon_text = respon_text[:-2]
    res.append(respon_text)




#creat csv file to store collected data
file_lists = [jop_title , company_name, date , loc , skls , links , salary ,res]
ex = zip_longest(*file_lists)
with open(r"C:\Users\Amr\OneDrive\Desktop\jops.csv", "w" ) as file:
    wr = csv.writer(file)
    wr.writerow(["Jop Title" , "Company Name" ,"Date", "Location" , "Skills" , "Links" , "salary" , "Responsabilities"])
    wr.writerows(ex)
