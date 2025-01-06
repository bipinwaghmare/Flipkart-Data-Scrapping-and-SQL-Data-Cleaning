# Flipkart Data Scraping and Cleaning Project

## Project Overview

This repository contains two distinct approaches for extracting, storing, and cleaning smartphone data scraped from **Flipkart**. The purpose is to demonstrate two different workflows for data processing, each suited for different use cases.

### **Approach 1: Data Cleaning with Python**
- Scrape smartphone data using Python libraries like **BeautifulSoup** and **requests**.
- Save the scraped data into a **CSV file**.
- Perform **data cleaning** using Python's **Pandas** library and **regex** operations.

### **Approach 2: Data Cleaning with SQL**
- Scrape smartphone data using Python libraries like **BeautifulSoup** and **requests**.
- Store the scraped data directly into a **MySQL database**.
- Perform **data cleaning** directly in SQL using advanced **queries** for efficient processing.

Both approaches showcase web scraping, structured data storage, and data cleaning workflows.

---

## Folder Structure

```plaintext
📂 Flipkart-Data-Scraping
├── 📁 Approach1_Python          # Python-based data cleaning
│   ├── main.py                 # Python script for scraping and saving data
│   ├── README.md               # Documentation for Approach 1
├── 📁 Approach2_SQL             # SQL-based data cleaning
│   ├── main.py                 # Python script for scraping and storing in SQL
│   ├── scrapped_querry.sql     # SQL queries for cleaning data
│   ├── README.md               # Documentation for Approach 2
└── README.md                   # Main documentation for the repository
```

---

## Key Features

### Common Features
- Web scraping using **BeautifulSoup** and **requests** to extract product details.
- Data includes:
  - Product Name
  - Price
  - Storage
  - Display Size
  - Camera Details
  - Battery
  - Processor
  - Ratings and Reviews

### Approach-Specific Features

#### **Approach 1: Python**
- Save raw data in CSV format for portability.
- Perform data cleaning using Python libraries:
  - Convert prices to numeric values.
  - Extract RAM, ROM, display size, and camera details.
  - Handle missing or inconsistent data.
  - Use regex for text extraction.

#### **Approach 2: SQL**
- Directly store raw data into a MySQL database.
- Perform data cleaning with SQL queries:
  - Extract numeric values from strings.
  - Standardize text formats.
  - Normalize data by separating key attributes (e.g., RAM, ROM, camera details).
  - Handle null and inconsistent data directly in SQL.

---

## Tools and Technologies

- **Python 3.x**
  - Libraries: `BeautifulSoup`, `requests`, `pandas`, `re`.
- **MySQL**: For structured data storage and cleaning.
- **SQL Queries**: For efficient data manipulation.
- **MySQL Connector**: To connect Python scripts to MySQL.

---

## How to Run

### Prerequisites
- Install Python 3.x and MySQL.
- Install Python libraries:
  ```bash
  pip install -r requirements.txt
  ```

---

### **Approach 1: Python-Based Data Cleaning**
1. Navigate to the `Approach1_Python` folder.
2. Run the scraping script:
   ```bash
   python main.py
   ```
3. The raw data is saved to a CSV file.
4. Data cleaning is performed within the script, producing cleaned data in-memory.

---

### **Approach 2: SQL-Based Data Cleaning**
1. Navigate to the `Approach2_SQL` folder.
2. Run the scraping script to store data in SQL:
   ```bash
   python main.py
   ```
3. Open the `scrapped_querry.sql` file in your MySQL client or editor.
4. Execute the queries step by step to clean the raw data in the database.

---

## Outputs

| Approach       | Raw Data                   | Cleaned Data             |
|----------------|----------------------------|--------------------------|
| **Approach 1** | Saved to in-memory dataframes | Cleaned within the script |
| **Approach 2** | Stored in SQL database     | Cleaned directly in SQL  |

---

## Future Work
- Automate data visualization and insights generation.
- Implement error handling and logging for scraping and database operations.
- Develop a dashboard for interactive analysis.

---

## Author

**Bipin Waghmare**  
[LinkedIn](https://www.linkedin.com/in/bipin-waghmare-2bb623167/) | [GitHub](https://github.com/bipinwaghmare)

---

Feel free to ask if you want further customization or have specific points to highlight!
