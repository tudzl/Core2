#Calculate Distance Between GPS Points in Python
import math

def haversine(coord1, coord2):
    R = 6372800  # Earth radius in meters
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    phi1, phi2 = math.radians(lat1), math.radians(lat2) 
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)
    
    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    
    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
london_coord = 51.5073219,  -0.1276474
cities = {
    'berlin': (52.5170365,  13.3888599),
    'vienna': (48.2083537,  16.3725042),
    'sydney': (-33.8548157, 151.2164539),
    'madrid': (40.4167047,  -3.7035825) 
}

for city, coord in cities.items():
    distance = haversine(london_coord, coord)
    print(city, distance)
#berlin 930723.2019867426
#vienna 1235650.1412429418
#sydney 16997984.55171465
#madrid 1263769.8859593808    

from geopy.distance import distance

for city, coord in cities.items():
    d = distance(london_coord, coord).m
    print(city, d)
    
#berlin 933410.7641236288
#vienna 1238804.7757673298
#sydney 16988546.466908157
#madrid 1263101.9239179497
    
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="specify_your_app_name_here")
location = geolocator.geocode("175 5th Avenue NYC")
print(location.address)
#Flatiron Building, 175, 5th Avenue, Flatiron, New York, NYC, New York, ...
print((location.latitude, location.longitude))
#(40.7410861, -73.9896297241625)
print(location.raw)
#{'place_id': '9167009604', 'type': 'attraction', ...}