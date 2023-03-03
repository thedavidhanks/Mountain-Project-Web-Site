import requests
import validators
from bs4 import BeautifulSoup

from classes.area import Area
from classes.climb import Climb

DEBUG = False

def gps_from_string(gps_string):
    if gps_string != None:
        gps_list = gps_string.replace(" ","").split(',')
        gps_dict = {"lat": gps_list[0], "long": gps_list[1]}
        return gps_dict
    else:
        return None

def coord_str_from_soup(soup):
    desc_rows = soup.select('table.description-details tr')
    gps_string = None
    for row in desc_rows:
        if row.td.contents[0] == 'GPS:':
            gps_string = row.contents[3].text.split('\n')[1].replace(' ','')
    return gps_string

def climbs_from_soup(soup, areaId = None):
    climb_list = []
    route_table_tag = soup.select('table#left-nav-route-table tr')
    
    for row in route_table_tag:
        climb_url_tag = row.select('td a')

        # TODO for some reason if there's only 1 climb on a page, there is no url tag in route_table_tag
        # For now check the length
        if len(climb_url_tag) > 0:
            
            # print(f'climb url tag \n{climb_url_tag}')
            url = climb_url_tag[0]['href']
            name = climb_url_tag[0].string
            grade_tag = row.select('td span.rateYDS')
            if len(grade_tag):
                grade = grade_tag[0].string
            else:
                grade = 'unrated'
            new_climb = Climb(Area.get_id_from_url(url), name, grade ,url=url, areaId=areaId)
            climb_list.append(new_climb)
        else: 
            if DEBUG:
                print('climb_url_tag is empty')
    return climb_list

def climbs_exist(soup):
    route_table_tag = soup.select('table#left-nav-route-table tr')
    return len(route_table_tag) > 0

def getAreaInfo(url):
    # get all the information about an area and put it in a class instance
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Get the area name
    area_heading_tag = soup.select_one('h1')
    area_name = area_heading_tag.contents[0].replace('\n','').strip()
    if False: print(f'Getting areaInfo for {area_name} using {url}')
    gps_string = coord_str_from_soup(soup)
    area_id = Area.get_id_from_url(url)
    current_area = Area(area_id, area_name, coord=gps_from_string(gps_string),url=url)
    
    # find any climbs
    if climbs_exist(soup):
        current_area.add_climb(climbs_from_soup(soup, areaId=area_id))

    # find any subareas
    subArea_table = soup.select('div.mp-sidebar div.max-height-md-0 a')
    for link in subArea_table:
        subArea_url = link['href']
        subArea_name = link.string
        if '/area/' in subArea_url and validators.url(subArea_url):
            if False: print(f'Adding sub-area: {subArea_name} @ {subArea_url} to {current_area.name}')                
            current_area.add_subArea(getAreaInfo(subArea_url))  # Recursion 8P    
    if False: print(f'{current_area.name} has {len(current_area.subArea)} sections with {current_area.no_of_climbs} climbs')
    return current_area