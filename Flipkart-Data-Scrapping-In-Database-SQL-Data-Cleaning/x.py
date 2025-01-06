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

# Function to connect to the database
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",  # Replace with your MySQL host
            user="root",  # Replace with your MySQL username

            password="",  # Replace with your MySQL password
            database="flipkart_database"  # Replace with your database name
        )
        print("Connected to the database successfully!")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Function to create the table
def create_table(cursor):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS flipkart_mobiles (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Product_name VARCHAR(255),
        Price VARCHAR(50),
        Storage VARCHAR(255),
        Display_size VARCHAR(255),
        Camera_Details VARCHAR(255),
        Battery VARCHAR(255),
        Rating VARCHAR(50),
        Processor VARCHAR(255),
        Warranty VARCHAR(255),
        Overall_Review TEXT
    );
    """
    cursor.execute(create_table_query)
    print("Table created or already exists.")

# Function to insert data into the table
def insert_data_to_sql(connection, data):
    insert_query = """
    INSERT INTO flipkart_mobiles (
        Product_name, Price, Storage, Display_size, Camera_Details, Battery, Rating, Processor, Warranty, Overall_Review
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    cursor = connection.cursor()
    cursor.executemany(insert_query, data)
    connection.commit()
    print(f"{cursor.rowcount} rows inserted into the database.")

# Function to get random headers
def get_random_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept-Language': 'en-US, en;q=0.5'
    }

# Function to ensure consistent list lengths
def ensure_length(data_list, target_length, fill_value="Not Available"):
    while len(data_list) < target_length:
        data_list.append(fill_value)
    return data_list

def scrape_page(page_number):
    ## Here we can change the URL
    url = f"https://www.flipkart.com/search?q=samsung+mobile&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={page_number}"
    headers = get_random_headers()  # Use random headers
    try:
        response = requests.get(url, headers=headers, timeout=10)  # Timeout to handle slow responses
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page {page_number}: {e}")
        return 0

    soup = BeautifulSoup(response.content, 'lxml')
    box = soup.find("div", class_="DOjaWF gdgoEp")
    if not box:
        return 0

    
    Product_name.extend([item.text for item in box.find_all("div", class_="KzDlHZ")])
    Price.extend([item.text for item in box.find_all("div", class_="Nx9bqj _4b5DiR")])

    ul_elements = box.find_all("ul", class_="G4BRas")
    for ul in ul_elements:
        li_items = [li.text for li in ul.find_all("li", class_="J+igdf")]
        Storage.append(next((item for item in li_items if "RAM" in item or "ROM" in item), "Not Available"))
        Display_size.append(next((item for item in li_items if "Display" in item), "Not Available"))
        Camera_Details.append(next((item for item in li_items if "Camera" in item or "MP" in item), "Not Available"))
        Battery.append(next((item for item in li_items if "Battery" in item), "Not Available"))
        Processor.append(next((item for item in li_items if "Processor" in item), "Not Available"))
        Warranty.append(next((item for item in li_items if "Warranty" in item), "Not Available"))

    Rating.extend([item.text for item in box.find_all("div", class_="XQDdHH")])
    Overall_Review.extend([item.text for item in box.find_all("span", class_="Wphh3N")])

    return len(Product_name)

# Main execution block
if __name__ == "__main__":
    Product_name, Price, Storage, Display_size, Camera_Details = [], [], [], [], []
    Battery, Rating, Processor, Warranty, Overall_Review = [], [], [], [], []

    # Scrape data from multiple pages
    num_pages = 3  # Change this to the number of pages you want to scrape
    for page in range(1, num_pages + 1):
        products_count = scrape_page(page)
        if products_count == 0:
            break
        time.sleep(random.uniform(2, 5))  # Random delay

    
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

    # Convert data into a list of tuples for SQL insertion
    data = list(zip(
        Product_name, Price, Storage, Display_size, Camera_Details, Battery,
        Rating, Processor, Warranty, Overall_Review
    ))

    # Connect to the database and store data
    db_connection = connect_to_database()
    if db_connection:
        cursor = db_connection.cursor()
        create_table(cursor)
        insert_data_to_sql(db_connection, data)
        cursor.close()
        db_connection.close()

    print("Data scraping and storage completed!")
