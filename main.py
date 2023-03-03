import requests
import json
from bs4 import BeautifulSoup
from pprint import pprint
from lxml import etree

from terminal import clean_term_output

TESTING = True
STATES_TO_TEST = 1
URL = 'https://www.mountainproject.com/'
PATH_TO_OUTPUT = './output'

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

climb_dict = {}
n = 0
for item in climb_names:
    climb = item.title()
    grade = grade_list[n]
    climb_dict[n] = {climb: [{'grade': grade}, {'gps': gps_list[n]}]}
    n+=1
climb_list_json = json.dumps(climb_dict, indent=4)

# Writing to sample.json
with open(PATH_TO_OUTPUT+"/climbs.json", "w") as outfile:
    outfile.write(climb_list_json)

summary = f'\n\n------SUMMARY------\nFound {str(len(climb_dict))} climbs\nFound {str(len(grade_list))} grades\nFound {str(len(gps_list))} coords\n-------------------'
status += summary
clean_term_output(status)