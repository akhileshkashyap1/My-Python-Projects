import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Create output path (relative to project root)
OUTPUT_DIR = os.path.join(os.getcwd(), "My-Python-Projects")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set up Selenium (headless browser)
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# URL 1: Screener.in
url1 = "https://www.screener.in/screens/6994/low-on-10-year-average-earnings/"
print(f"Fetching data from {url1}")
driver.get(url1)
time.sleep(5)  # Let JS load fully

soup1 = BeautifulSoup(driver.page_source, 'html.parser')
table1 = soup1.find('table', class_='data-table')

data1 = []
headers1 = []

if table1:
    # Extract headers
    for th in table1.find_all('th'):
        headers1.append(th.text.strip())

    # Extract rows
    for row in table1.find_all('tr')[1:]:
        cells = [td.text.strip() for td in row.find_all('td')]
        if cells:
            data1.append(cells)

    df1 = pd.DataFrame(data1, columns=headers1)
    print("Screener.in data preview:")
    print(df1.head())
    df1.to_csv(os.path.join(OUTPUT_DIR, "screener_output.csv"), index=False)
else:
    print("No table found on Screener page.")

# URL 2: MoneyControl
url2 = "https://www.moneycontrol.com/markets/stock-deals/"
print(f"\nFetching data from {url2}")
driver.get(url2)
time.sleep(5)

soup2 = BeautifulSoup(driver.page_source, 'html.parser')
table2 = soup2.find('table')

data2 = []
headers2 = []

if table2:
    # Extract headers
    for th in table2.find_all('th'):
        headers2.append(th.text.strip())

    # Extract rows
    for row in table2.find_all('tr')[1:]:
        cells = [td.text.strip() for td in row.find_all('td')]
        if cells:
            data2.append(cells)

    df2 = pd.DataFrame(data2, columns=headers2)
    print("\nMoneyControl Stock Deals data preview:")
    print(df2.head())
    df2.to_csv(os.path.join(OUTPUT_DIR, "moneycontrol_output.csv"), index=False)
else:
    print("No table found on MoneyControl page.")

# Done
driver.quit()
print(f"\nCSV files saved to: {OUTPUT_DIR}")
 