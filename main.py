import requests
from bs4 import BeautifulSoup
from pprint import pprint
from lxml import etree

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

for item in state_links[:1]:
    response = requests.get(url=item)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.select('div.lef-nav-row a')
    for link in data:
        area_links.append(link['href'])
    climb_names = []
    grade_list = []
    gps_list = []

for item in area_links:
    response = requests.get(url=item)
    soup = BeautifulSoup(response.text, 'html.parser')
    names = soup.select('table.width100 tr td a')
    grades = soup.select('span.rateYDS')
    gps = soup.select_one('table.description-details tr td a').find_parent().find_parent().get_text(strip=True,).split("G")[0]




    for grade in grades:
        grade_real = grade.text
        grade_list.append(grade_real)
        gps_list.append(gps)
    for climb in names:
        climb_name = climb.text
        climb_names.append(climb_name)

climb_list = []
n = 0
for item in climb_names:
    climb = item.title()
    grade = grade_list[n]
    dict = {climb: [{'grade': grade}, {'gps': gps_list[n]}]}
    climb_list.append(dict)
    n+=1
pprint(climb_list)



