from classes.climb import Climb
from classes.area import Area

newClimb = Climb(1,'hello','v5')
newClimb2 = Climb(2,'world','v0.0', {'lat': 5, 'long': 30})
area = Area(1, 'Place', desc='an intersting place with rocks')

print(newClimb.__dict__)
print(newClimb2.__dict__)
print(area.__dict__)