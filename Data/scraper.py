import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

# URL of the webpage to scrape
url = "https://mtsamples.com/"
file_path = "output.csv"

# Remove the file if it already exists
if os.path.exists(file_path):
    os.remove(file_path)
    print(f"File '{file_path}' has been deleted.")

# Initialize an empty list to store extracted data
data_list = []

# Send a GET request to the webpage and get its HTML content
response = requests.get(url)
html_content = response.content

# Parse the HTML content using Beautiful Soup
soup = BeautifulSoup(html_content, "html.parser")

# Find all the links on the webpage
links = soup.find_all("a")

# Loop through each link on the webpage
for link in links:
    # Get the URL of the link
    link_url = link.get("href")
    if "/site/pages/browse.asp?type=" in link_url:
        link_url = url + link_url
    
        # Send a GET request to the link URL and get its HTML content
        link_response = requests.get(link_url)
        link_html_content = link_response.content

        # Parse the HTML content of the link using Beautiful Soup
        link_soup = BeautifulSoup(link_html_content, "html.parser")

        # Find all the links on the link page
        link_links = link_soup.find_all("a")

        # Loop through each link on the link page
        for link_link in link_links:
            link_link_url = url + link_link.get("href")
            if "/site/pages/browse.asp?type=" and "&Sample=" in link_link_url:
                response = requests.get(link_link_url)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    text_content = soup.get_text()
                    lines = text_content.split('\n')

                    # Clean the lines and extract the required portion
                    clean_list = list(filter(None, lines))
                    sample_data = clean_list[154:174]  # Adjust indices if necessary

                    # Extract relevant data (you may need to parse this properly based on website structure)
                    sample_dict = {
                        'Sample Name': sample_data[0] if len(sample_data) > 0 else '',
                        'Description': sample_data[1] if len(sample_data) > 1 else '',
                        'Keywords': sample_data[-1] if len(sample_data) > 2 else ''
                    }

                    # Append the dictionary to the data list
                    data_list.append(sample_dict)

# Write the data to a CSV file using pandas
df = pd.DataFrame(data_list)
df.to_csv(file_path, index=False)

print(f"Data has been written to '{file_path}'.")
