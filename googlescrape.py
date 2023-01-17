import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape Google Shopping
def scrape_google_shopping():
    # Send a GET request to the Google Shopping URL with the query parameter
    url = 'https://www.google.co.uk/search?q=apple+iphone+12+128GB&sxsrf=AJOqlzXc_EWCelOtpsMfrgnqCm5CgvgFNw:1673875847002&source=lnms&tbm=shop&sa=X&ved=2ahUKEwjezoi6mcz8AhVCZcAKHW_QBasQ_AUoAXoECAEQAw&biw=1512&bih=786&dpr=2'
    page = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(page.content, 'html.parser')

    # Find all the items on the page
    items = soup.find_all('div', class_='i0X6df')
    print(items)
    # Create an empty list to store the results
    results = []

    # Iterate through the items and extract the relevant information
    for item in items:
        #title = item.find('h3', class_='tAxDx').text
        print(item).text


    return results


