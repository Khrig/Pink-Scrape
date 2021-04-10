
from bs4 import BeautifulSoup
import pandas as pd
import requests

def create_csv():
    name = "Results.csv"
    results = pd.DataFrame(columns = ["title", "price", "url", "time", "id", "location","desc"])
    results.to_csv(name)

def find_values(div):
    bike_dict = {}
    bike_dict["url"] = div.a["href"]
    bike_dict["id"] = div["id"]
    
    tds = div.find_all('td')
    bike_dict["title"] = tds[1].a.text
    bike_dict["price"] = tds[4].text
    bike_dict["location"] = tds[2].text
    bike_dict["desc"] = tds[5].text
    for key in bike_dict:
        bike_dict[key] = bike_dict[key].replace("\n","").strip(" ")
    return bike_dict

def notification(name):
    from win10toast import ToastNotifier
    toaster = ToastNotifier ()
    toaster.show_toast("Pink Scrape", "New Listing: {}".format(name)) 

def main():
    always_notify = True

    with open('search.txt', 'r') as file:
        search_URL = file.read()

    try:
        d = pd.read_csv("Results.csv")
    except:
        print("CSV not found attmpting to make new")
        create_csv()
        d = pd.read_csv("Results.csv")
        
    r = requests.get(search_URL)

    soup = BeautifulSoup(r.text, features = 'lxml')

    bsitems = []
    divtags = soup.find_all('div')
    for div in divtags:
        if div.has_attr('id'):
            if div["id"][:4] == "csid":#one div per bike
                bsitems.append(div)
    bsitem_dicts = [find_values(div) for div in bsitems]
    bike_frame = pd.DataFrame(bsitem_dicts)

    change = False
    try:
        if d["id"][0] != bike_frame["id"][0]:
            change = True
    except:
        print("failed to compare old and new")

    if change == True:
        bike_frame.to_csv("Results.csv", index_label = "index")
    elif always_notify == True:
        print("telling you anyway")
        notification(bike_frame["title"][0])

main()

# with open("Output.txt", "w") as text_file:
#     text_file.write(soup.prettify())


