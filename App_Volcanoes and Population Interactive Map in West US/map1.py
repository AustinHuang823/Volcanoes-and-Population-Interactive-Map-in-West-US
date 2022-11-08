import folium #useful map extension
import pandas #for reading .txt & .json files

data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

html = """
<h6>Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""
# html = """<h4>Volcano information:</h4>
# Height: %s m
# """

# <br> will add newline here
# <a ..... </a> transform the link to 2nd %s
# <h4> is the word type here

def color_chooser(elevation):
    if elevation < 1000:
        return "green"
    elif elevation < 3000:
        return "orange"
    else:
        return "red"

map = folium.Map(location = [34.01900366323226, -118.297542299363], zoom_start = 7,  tiles="Stamen Terrain")

fgv = folium.FeatureGroup(name = "Volcanoes")
for lt, ln, el, name in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location= [lt, ln], radius = 6, popup = folium.Popup(iframe), fill_color = color_chooser(el), color = "black", fill_opacity = 0.7))
    
fgp = folium.FeatureGroup(name = "Population")
fgp.add_child(folium.GeoJson(data= open('world.json', 'r', encoding= 'utf-8-sig').read(), 
                            style_function= lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 30000000
                                                       else 'orange' if 30000000 <= x['properties']['POP2005'] < 100000000
                                                       else 'red'}))
#json contains polygon

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())

map.save("Volcanoes and Population Interactive Map in West US.html")