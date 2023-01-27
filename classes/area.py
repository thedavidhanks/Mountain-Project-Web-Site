class Area:
    # id: int, mp id of the area
    # name: string
    # no_of_climbs: int
    # coord: object, like {lat: 30.0, long: -85.0}
    # desc: string
    def __init__ (self, id, name, coord=None, areaId=None, no_of_climbs=None, desc=None):
        self.mp_id = id
        self.name = name
        if(coord != None and self.coord_is_good(coord)):
            self.coord = coord
        else:
            self.coord = None
        self.areaId = areaId
        self.no_of_climbs = no_of_climbs
        self.desc = desc
    
    def coord_is_good(self, coord_obj):
        return "lat" in coord_obj and "long" in coord_obj

    def update_no_of_climbs(self, noc):
        self.no_of_climbs = noc
