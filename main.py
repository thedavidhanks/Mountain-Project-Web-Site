import requests
import json
from bs4 import BeautifulSoup
from pprint import pprint
from lxml import etree

from terminal import clean_term_output
from webCrawler.parseUrl import getAreaInfo

TESTING = True
STATES_TO_TEST = 1
URL = 'https://www.mountainproject.com/'
PATH_TO_OUTPUT = './output/'

response = requests.get(url=URL)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')
status = ''

# Get the state anchor tags
status += 'Getting state urls...\n'
clean_term_output(status)
data = soup.select('div#route-guide strong a')
status += 'Found '+str(len(data))+' total url in route-guide...\n'
clean_term_output(status)

state_links =[]
area_links = []
for item in data:
    if item['href'] not in state_links:
        state_links.append(item['href'])
status += 'Found '+str(len(state_links))+' unique urls...\n'
clean_term_output(status)

states_to_eval = state_links[:STATES_TO_TEST] if TESTING else state_links

status += 'Indexing climbs in '+str(len(states_to_eval))+' states...\n'
clean_term_output(status)
for state_url in states_to_eval:
    state_name = state_url.split('/')[-1]
    response = requests.get(url=state_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.select('div.lef-nav-row a')
    for link in data:
        area_links.append(link['href'])
    status += 'Found '+str(len(area_links))+' areas in '+state_name+'...\n'
    clean_term_output(status)
climb_names = []
grade_list = []
gps_list = []
state_areas = []
total_climbs = 0
total_areas = 0
for url in area_links:
    new_area = getAreaInfo(url)
    total_areas += 1
    total_climbs += new_area.no_of_climbs
    state_areas.append(new_area)
    # Write the area to it's own json
    # Serializing json
    json_object = json.dumps(new_area.get_climbs_dict(), indent=4)
    
    # Writing to sample.json
    with open(PATH_TO_OUTPUT+new_area.name.replace('/','')+".json", "w") as outfile:
        outfile.write(json_object)
    print(new_area.get_area_short_summary())

summary = f'\n\n------SUMMARY------\nFound {total_climbs} climbs\nFound {total_areas} areas\n-------------------'
status += summary
clean_term_output(status)