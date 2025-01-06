import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time
from datetime import datetime
import logging
from fake_useragent import UserAgent


proxies_list = [
    {"http": "http://47.56.110.204:8989", "https": "http://47.56.110.204:8989"},
    {"http": "http://47.74.152.29:8888", "https": "http://47.74.152.29:8888"},
    {"http": "http://35.209.198.222:80", "https": "http://35.209.198.222:80"},
    {"http": "http://41.74.91.244:80", "https": "http://41.74.91.244:80"},
    {"http": "http://185.64.209.186:53281", "https": "http://185.64.209.186:53281"},
    {"http": "http://46.47.197.210:3128", "https": "http://46.47.197.210:3128"},
    {"http": "http://167.99.236.14:80", "https": "http://167.99.236.14:80"},
    {"http": "http://156.38.112.11:80", "https": "http://156.38.112.11:80"},
    {"http": "http://20.24.43.214:80", "https": "http://20.24.43.214:80"},
    {"http": "http://20.206.106.192:8123", "https": "http://20.206.106.192:8123"}
]

headers_list = [
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36", "Accept-Language": "en-US,en;q=0.5"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36", "Accept-Language": "en-US,en;q=0.5"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36", "Accept-Language": "en-US,en;q=0.5"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36", "Accept-Language": "en-US,en;q=0.5"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36", "Accept-Language": "en-US,en;q=0.5"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36", "Accept-Language": "en-US,en;q=0.5"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36", "Accept-Language": "en-US,en;q=0.5"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36", "Accept-Language": "en-US,en;q=0.5"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36", "Accept-Language": "en-US,en;q=0.5"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.4085.123 Safari/537.36", "Accept-Language": "en-US,en;q=0.5"}
]


Product_name = []
Price = []
# Ram_storage = []
# Rom_storage = []
Storage = []
Display_size = []
# Rare_camera = []
# Front_camera = []
Camera_Details = []
Battery = []
Rating = []
Processor = []
Warranty = []
Overall_Review = []


for i in range(2,4):
    url = "https://www.flipkart.com/search?q=poco+smartphone&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off&page="+str(i)

    # HEADERS = random.choice(headers_list)
    # proxies = random.choice(proxies_list)
    # Defining user-agent and language preferences for the request

    HEADERS = ({'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36","Accept-Language":"en-US, en;q=0.5"})

    # r = requests.get(url, headers = HEADERS, proxies=proxies)
    r = requests.get(url, headers = HEADERS)
    r.raise_for_status()
    soup = BeautifulSoup(r.content, 'lxml')
    # print(r)

    # soup = BeautifulSoup(r.text, "lxml")

    box = soup.find("div", class_= "DOjaWF gdgoEp")
    # print(soup)

    # next_page = soup.find("a", class_ = "_9QVEpD").get("href")

    # complete_next_page = "https://www.flipkart.com"+next_page

    # print(complete_next_page)
    try:
        Product_name_element = box.find_all("div", class_ = "KzDlHZ")
        for i in Product_name_element:
            name = i.text
            if name:
                Product_name.append(name)
            else:
                Product_name.append("Not Available")
    except:
        Product_name.append("Not Available")

    print(Product_name)
    print(len(Product_name))

    try:
        Price_element = box.find_all("div", class_ = "Nx9bqj _4b5DiR")
        for i in Price_element:
            price = i.text
            if price:   
                Price.append(price)
            else:
                Price.append("Not Available")
    except:
        Price.append("Not Available")

    print(Price)
    print(len(Price))


    # Ram_storage_element = soup.find_all("li", class_ = "J+igdf")
    # for i in Ram_storage_element:
    #     ram = i.text
    #     Ram_storage.append(ram)
    # print(Ram_storage)

    ul_elements = box.find_all("ul", class_="G4BRas")


    # Loop through each <ul> and process the <li> tags
    try:
        for ul in ul_elements:
            li_items = ul.find_all("li", class_="J+igdf")  # Find all <li> tags with the specific class
            for li in li_items:
                if li:
                    description = li.text.strip()
                
                # Check for specific keywords and append to the relevant list
                    if "RAM" in description or "ROM" in description:
                        Storage.append(description)
                # if "RAM" in description:
                #     Ram_storage.append(description) 
                # elif "ROM" in description:
                #     Rom_storage.append(description)
                    elif "Display" in description:
                        Display_size.append(description)
                # elif "Rear Camera" in description:
                #     Rare_camera.append(description)
                # elif "Front Camera" in description:
                #     Front_camera.append(description)
                    elif "Camera" in description or "MP" in description:
                        Camera_Details.append(description)
                    elif "Battery" in description:
                        Battery.append(description)
                    elif "Processor" in description:
                        Processor.append(description)
                    elif "Warranty" in description:
                        Warranty.append(description)
                    else:
                        Storage.append("Not Available")
                    # Ram_storage.append(None)
                    # Rom_storage.append(None)
                        Display_size.append("Not Available")
                    # Rare_camera.append(None)
                    # Front_camera.append(None)
                        Camera_Details.append("Not Available")
                        Battery.append("Not Available")
                        Processor.append("Not Available")
                        Warranty.append("Not Available")
    except:
        Storage.append("Not Available")
        # Ram_storage.append(None)
        # Rom_storage.append(None)
        Display_size.append("Not Available")
        # Rare_camera.append(None)
        # Front_camera.append(None)
        Camera_Details.append("Not Available")
        Battery.append("Not Available")
        Processor.append("Not Available")
        Warranty.append("Not Available")

    print("Storage Details:", Storage)
    print(len(Storage))

    # print("RAM Details:", Ram_storage)
    # print(len(Ram_storage))

    # print("ROM Details:", Rom_storage)
    # print(len(Rom_storage))

    print("Display Details:", Display_size)
    print(len(Display_size))

    print("Camera Details:", Storage)
    print(len(Camera_Details))

    # print("Rear Camera Details:", Rare_camera)
    # print(len(Rare_camera))

    # print("Front Camera Details:", Front_camera)
    # print(len(Front_camera))

    print("Battery Details:", Battery)
    print(len(Battery))

    print("Processor Details:", Processor)
    print(len(Processor))

    print("Warranty Details:", Warranty)
    print(len(Warranty))


    try:
        Rating_element = box.find_all("div", class_ = "XQDdHH")
        for i in Rating_element:
            rating = i.text
            if rating:
                Rating.append(rating)
            else:
                Rating.append("Not Available")
    except:
        Rating.append("Not Available")

    print(Rating)
    print(len(Rating))


    try:
        Overall_Review_element = box.find_all("span", class_= "Wphh3N")
        for i in Overall_Review_element:
            review = i.text
            if review:
                Overall_Review.append(review)
            else:
                Overall_Review.append("Not Available")
    except:
        Overall_Review.append("Not Available")

    print(Overall_Review)
    print(len(Overall_Review))

    time.sleep(random.uniform(1, 3))

df = pd.DataFrame(
    {
    "Product_name":Product_name,
    "Storage":Storage,
    # "Ram_storage":Ram_storage,
    # "Rom_storage":Rom_storage,
    "Display_size":Display_size,
    "Camera Details":Camera_Details,
    # "Rare_camera":Rare_camera,
    # "Front_camera":Front_camera,
    "Battery":Battery,
    "Rating":Rating,
    "Processor":Processor,
    "Warranty":Warranty,
    "Overall_Review":Overall_Review,
    "Price":Price
    }
    )



print(df)