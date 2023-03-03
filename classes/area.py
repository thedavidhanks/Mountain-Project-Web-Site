from classes.climb import Climb

DEBUG = False
class Area:
    # id: int, mp id of the area
    # name: string
    # no_of_climbs: int
    # coord: object, like {lat: 30.0, long: -85.0}
    # desc: string
    # subAreas: List of Area instances

    def __init__ (self, id, name, coord=None, no_of_climbs=0, desc=None, url=None):
        self.mp_id = id
        self.url = url
        self.name = name
        if(coord != None and self.coord_is_good(coord)):
            self.coord = coord
        else:
            self.coord = None
        self.no_of_climbs = no_of_climbs
        self.desc = desc
        self.subArea = []
        self.climbs = []
    
    def coord_is_good(self, coord_obj):
        return "lat" in coord_obj and "long" in coord_obj

    def update_no_of_climbs(self, noc):
        self.no_of_climbs = noc

    def add_subArea(self, sa):
        # print('add sub-area: ',sa.name)
        if type(sa) is Area:
            if DEBUG: print(f'{sa.name} is Area with {sa.no_of_climbs} climbs')
            self.subArea.append(sa)
            self.no_of_climbs += sa.no_of_climbs
    
    def add_climb(self, climb):
        
        if type(climb) is Climb:
            self.climbs.append(climb)
            self.no_of_climbs +=1
        elif type(climb) is list:
            for c in climb:
                # Note, we could .extend self.climbs, but this way we check that each item in the list is a climb
                self.add_climb(c)
        else:
            if DEBUG: print(f'no climbs added. Climb is type: {type(climb)}')

    def get_area_summary(self):
        summary = f"----{self.name}----"
        summary += '\n'+self.url
        summary += f"\nClimbs: {self.no_of_climbs}"
        summary += f"\nsub areas: {len(self.subArea)}"
        if len(self.subArea) > 0:
            for sa in self.subArea:
                summary += f'\n   {sa.name}'
        if self.coord:
            summary += f'\ncoords: {self.coord}'
        return summary
    
    def get_area_short_summary(self):
        section_sum = f' {len(self.subArea)} sections |' if len(self.subArea) > 0 else ''
        summary = f'{self.name}:{section_sum} {self.no_of_climbs} climbs'
        return summary

    def get_id_from_url(url):
        url_parts = url.split('/')
        id = None
        for part in url_parts:
            if part.isdigit():
                id = part
                break
        return id
