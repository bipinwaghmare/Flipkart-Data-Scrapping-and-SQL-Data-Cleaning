import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import mysql.connector


# List of User-Agents for rotation
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
]


def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",  # Replace with your MySQL host
            user="your_username",  # Replace with your MySQL username
            password="your_password",  # Replace with your MySQL password
            database="your_database"  # Replace with your database name
        )
        print("Connected to the database successfully!")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def get_random_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept-Language': 'en-US, en;q=0.5'
    }

Product_name, Price, Storage, Display_size, Camera_Details = [], [], [], [], []
Battery, Rating, Processor, Warranty, Overall_Review = [], [], [], [], []

# Function to ensure consistent list lengths
def ensure_length(data_list, target_length, fill_value="Not Available"):
    while len(data_list) < target_length:
        data_list.append(fill_value)
    return data_list

def scrape_page(page_number):
    # url = f"https://www.flipkart.com/search?q=poco+smartphone&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off&page={page_number}"
    # url = f"https://www.flipkart.com/search?q=realme+mobile&as=on&as-show=on&otracker=AS_Query_HistoryAutoSuggest_1_7_na_na_na&otracker1=AS_Query_HistoryAutoSuggest_1_7_na_na_na&as-pos=1&as-type=HISTORY&suggestionId=realme+mobile&requestId=a2f7e4e8-2ab1-4d8c-9eb6-adaaba065553&as-backfill=on&page={page_number}"
    url = f"https://www.flipkart.com/search?q=samsung+mobile&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={page_number}"
    headers = get_random_headers()  # Use random headers
    proxies = {"http": "http://your-proxy", "https": "https://your-proxy"}  # Add proxies if available

    try:
        response = requests.get(url, headers=headers, timeout=10)  # Timeout to handle slow responses
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page {page_number}: {e}")
        return 0

    soup = BeautifulSoup(response.content, 'lxml')

    # Find the container with product details
    box = soup.find("div", class_="DOjaWF gdgoEp")
    if not box:
        return 0

    # Extract product names
    product_names = [item.text for item in box.find_all("div", class_="KzDlHZ")]
    Product_name.extend(product_names)

    # Extract prices
    prices = [item.text for item in box.find_all("div", class_="Nx9bqj _4b5DiR")]
    Price.extend(prices)

    # Extract details
    ul_elements = box.find_all("ul", class_="G4BRas")
    for ul in ul_elements:
        li_items = [li.text for li in ul.find_all("li", class_="J+igdf")]
        storage = next((item for item in li_items if "RAM" in item or "ROM" in item), "Not Available")
        display_size = next((item for item in li_items if "Display" in item), "Not Available")
        camera_details = next((item for item in li_items if "Camera" in item or "MP" in item), "Not Available")
        battery = next((item for item in li_items if "Battery" in item), "Not Available")
        processor = next((item for item in li_items if "Processor" in item), "Not Available")
        warranty = next((item for item in li_items if "Warranty" in item), "Not Available")

        # Append to corresponding lists
        Storage.append(storage)
        Display_size.append(display_size)
        Camera_Details.append(camera_details)
        Battery.append(battery)
        Processor.append(processor)
        Warranty.append(warranty)

    # Extract ratings and reviews
    ratings = [item.text for item in box.find_all("div", class_="XQDdHH")]
    reviews = [item.text for item in box.find_all("span", class_="Wphh3N")]
    Rating.extend(ratings)
    Overall_Review.extend(reviews)

    return len(product_names)

# Scrape multiple pages
num_pages = 1
for page in range(50, num_pages + 1):
    products_count = scrape_page(page)
    if products_count == 0:
        break
    time.sleep(random.uniform(2, 5))  # Random delay

# Ensure consistent list lengths
max_length = len(Product_name)
ensure_length(Price, max_length)
ensure_length(Storage, max_length)
ensure_length(Display_size, max_length)
ensure_length(Camera_Details, max_length)
ensure_length(Battery, max_length)
ensure_length(Rating, max_length)
ensure_length(Processor, max_length)
ensure_length(Warranty, max_length)
ensure_length(Overall_Review, max_length)

# Save data to CSV
df = pd.DataFrame({
    "Product_name": Product_name,
    "Price": Price,
    "Storage": Storage,
    "Display_size": Display_size,
    "Camera Details": Camera_Details,
    "Battery": Battery,
    "Rating": Rating,
    "Processor": Processor,
    "Warranty": Warranty,
    "Overall_Review": Overall_Review,
})
df.to_csv('flipkart_mobile_data.csv', index=False, encoding='utf-8')

print("Data saved to flipkart_mobile_data.csv")
