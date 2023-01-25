import requests
from bs4 import BeautifulSoup
from pprint import pprint
URL = 'https://www.mountainproject.com/'
response = requests.get(url=URL)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

# Get the state anchor tags
data = soup.select('div#route-guide strong a')

state_links =[]
area_links = []
for item in data:
    if item['href'] not in state_links:
        state_links.append(item['href'])

for item in state_links[:3]:
    response = requests.get(url=item)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.select('div.lef-nav-row a')
    for link in data:
        area_links.append(link['href'])
pprint(area_links)
