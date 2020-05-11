import requests
from geopy.geocoders import Nominatim
from datetime import datetime
import time

####Not Implemented but works#####
#Originally planned to read in the datetime from the API however it's format was not compatable.
#Other similar API's returned incorrect / unusable times.
#Code would be rerun at certain time every day, getting an updated sunRise / sunSet time. Pass them to main and then capture an image at said time(s)
location = Nominatim().geocode('Galway')
r = requests.get('https://api.sunrise-sunset.org/json', params={'lat': location.latitude, 'lng': location.longitude}).json()['results']


#def sunrise():
sunRise = r['sunrise']
print("Sunrise:"+sunRise)
	#return (sunRise)

#def sunset():
sunSet = r['sunset']
print("Sunset: "+sunSet)
	#return (sunSet)

