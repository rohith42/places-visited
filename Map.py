import folium, pandas

# (40,-99),zoom_start=4.4 for the entire US, currently set to world-view 
map = folium.Map(location=[35,-15], zoom_start=3, tiles='Stamen Toner')

## Read all the data using pandas 
data = pandas.read_csv("data/PlacesVisited.csv")
isv = list(pandas.read_csv("data/IndianStates_Visited.txt")['States'])
usv = list(pandas.read_csv("data/AmericanStates_Visited.txt")['States'])
cv = list(pandas.read_csv("data/Countries_Visited.txt")['Countries'])


## Specific location markers
fg1 = folium.FeatureGroup(name='Places Visited')
# Uses pandas to extract each column as a list
lats = list(data["LAT"])
longs = list(data["LON"])
places = list(data["PLACE"])
months = list(data["MONTH"])
years = list(data["YEAR"])

# Maps each entry to a folium marker with a popup describing that location
for lat, longi, place, month, year in zip(lats, longs, places, months, years):
    dt = "{} {}".format(month, year)
    iframe = folium.IFrame(place + '<br>' + dt)  # Formats the popup
    pop = folium.Popup(iframe, min_width=200, max_width=200)
    fg1.add_child(folium.Marker(location=[lat, longi], popup=pop, icon=folium.Icon(color='purple')))


# Reads each geojson entry in US_States.json 
# and highlights them blue if found in usv (list of states visited in America)
fg2 = folium.FeatureGroup(name='American States Visited')
fg2.add_child(folium.GeoJson( data=(open('json/US_States.json', 'r', encoding='utf-8-sig').read()), 
style_function=lambda x: {'color': 'blue' if x['properties']['NAME'] in usv else 'none', 
'fillColor': 'blue' if x['properties']['NAME'] in usv else 'none'} ))


# Reads each geojson entry in Indian_States.json 
# and highlights them red if found in isv (list of Indian states visited)
fg3 = folium.FeatureGroup(name='Indian States Visited')
fg3.add_child(folium.GeoJson( data=(open('json/Indian_States.json', 'r', encoding='utf-8-sig').read()), 
style_function=lambda x: {'color': 'red' if x['properties']['NAME_1'] in isv else 'none', 
'fillColor': 'red' if x['properties']['NAME_1'] in isv else 'none'} ))


# Reads each geojson entry in world.json 
# and highlights them green if found in cv (list of countries visited around the world)
fg4 = folium.FeatureGroup(name='Countries Visited')
fg4.add_child(folium.GeoJson( data=(open('json/world.json', 'r', encoding='utf-8-sig').read()), 
style_function=lambda x: {'color': 'green' if x['properties']['NAME'] in cv else 'none', 
'fillColor': 'green' if x['properties']['NAME'] in cv else 'none'} ))


# Adds each feature group above to the map and a layer control
map.add_child(fg1)
map.add_child(fg2)
map.add_child(fg3)
map.add_child(fg4)
map.add_child(folium.LayerControl())

# Saves the map as Map.html
map.save("Map.html")

