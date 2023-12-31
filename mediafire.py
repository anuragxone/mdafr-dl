from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Function to download a single file from MediaFire using Selenium
def download_file(url, chrome_binary, chromedriver_binary):
    try:
        chrome_options = Options()
        chrome_options.binary_location = chrome_binary  # Set custom Chrome binary location

        service = Service(chromedriver_binary)  # Set custom Chromedriver binary location
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.get(url)
        time.sleep(2)  # Allow time for the page to load (adjust as needed)

        download_button = driver.find_element(By.ID, 'downloadButton')  # Replace 'downloadButton' with the correct ID
        download_button.click()

        # Additional logic may be required to handle the download dialog or process the download

        print(f"Downloaded: {url}")

        driver.quit()

    except Exception as e:
        print(f"Failed to download {url}: {e}")

# Function to read links from a file and trigger downloads
def download_links(link_file, chrome_binary, chromedriver_binary):
    try:
        with open(link_file, 'r') as f:
            links = f.readlines()

        links = [link.strip() for link in links]

        for link in links:
            download_file(link, chrome_binary, chromedriver_binary)

    except Exception as e:
        print(f"Error: {e}")

# Usage example
input_link_file = './links.txt'  # Replace with your input file name
custom_chrome_binary = './chrome/chrome'  # Replace with the path to your Chrome binary
custom_chromedriver_binary = './chromedriver/chromedriver'  # Replace with the path to your Chromedriver binary

download_links(input_link_file, custom_chrome_binary, custom_chromedriver_binary)
