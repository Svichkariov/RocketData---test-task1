import requests
from bs4 import BeautifulSoup
import json


url_TZ = "https://omsk.yapdomik.ru/"
t = requests.get(url_TZ)
soup_url = BeautifulSoup(t.content, "html.parser")


urls=[]
urls_1 = soup_url.find_all("a", class_="city-select__item")

for u in urls_1:
    ur = u.get("href") + "/about"
    if ur not in urls:
        urls.append(ur)


urls.insert(0, f"{url_TZ}about")


for url in urls:
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    script = soup.find_all("script")[4].text.split()[2:]
    name = soup.find("div", class_= "container--about__title").text[1:-16]
    tel = soup.find("a", class_= "link link--black").text
    city = soup.find("a", class_= "city-select__current link link--underline").text

    string = ""
    for element in script:
        string += element


    dict = json.loads(string)
    a = dict["shops"]


    i = 0
    list_parametry = ("address", "coord", "schedule")
    list_vse_magaz_v_gorod = []
    while i < len(a):
        element = a[i]
        coordinat = []
        vrem_rabot = []
        inform_odin_magazin = {"name": name, "address": city, "latlon": "", "phones": tel, "working_hours": ""}
        for key,value in element.items():
            if key in list_parametry[0]:
                address = city + " " + element[key]
                inform_odin_magazin.update(address=address)
            elif key == list_parametry[1]:
                coordinat.append(value['latitude'])
                coordinat.append(value['longitude'])
                inform_odin_magazin.update(latlon=coordinat)
            elif key == list_parametry[2]:
                vrem = value
                for x in vrem:
                    vrem_rabot.append(x['openTime'])
                    vrem_rabot.append(x['closeTime'])
                    inform_odin_magazin.update(working_hours=vrem_rabot)

        list_vse_magaz_v_gorod.append(inform_odin_magazin)
        i += 1

    name_is_json = name + " - " + city
    with open(f"{name_is_json}.json", 'w') as f:
        f.write(json.dumps(list_vse_magaz_v_gorod, indent=4, sort_keys=False, ensure_ascii=False))
