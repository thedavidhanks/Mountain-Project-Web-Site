class Climb:
    # id: mp id
    # name: string
    # grade: ...a string?
    # coord: object, like {lat: 30.0, long: -85.0}
    # areaId: int, mp id of the area. The immediate parent area, even if that is a subarea.
    def __init__ (self, id, name, grade, coord=None, areaId=None, url=None, desc=''):
        self.mp_id = id
        self.name = name
        self.grade = grade
        if(coord != None and self.coord_is_good(coord)):
            self.coord = coord
        else:
            self.coord = None
        self.areaId = areaId
        self.url = url
        self.desc = desc
        
    def coord_is_good(self, coord_obj):
        return "lat" in coord_obj and "long" in coord_obj


    