import pydeck
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TOMTOM_API_KEY")

url = "https://api.tomtom.com/traffic/services/5/incidentDetails"

params = {
    "key": API_KEY,
    "bbox": "-0.95,41.60,-0.80,41.72",  # small area around Zaragoza
    "fields": "{incidents{type,geometry{type,coordinates},properties{iconCategory}}}",
    "language": "en-GB",
    "timeValidityFilter": "present"
}

response = requests.get(url, params=params)

print("Status:", response.status_code)

data = response.json()

print(json.dumps(data, indent=2))

# 2014 locations of car accidents in the UK
UK_ACCIDENTS_DATA = ('https://raw.githubusercontent.com/uber-common/'
                     'deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv')

# Define a layer to display on a map
layer = pydeck.Layer(
    'HexagonLayer',
    UK_ACCIDENTS_DATA,
    get_position='[lng, lat]',
    auto_highlight=True,
    elevation_scale=50,
    pickable=True,
    elevation_range=[0, 3000],
    extruded=True,
    coverage=1)

# Set the viewport location
view_state = pydeck.ViewState(
    longitude=-1.415,
    latitude=52.2323,
    zoom=6,
    min_zoom=5,
    max_zoom=15,
    pitch=40.5,
    bearing=-27.36)

# Render
r = pydeck.Deck(layers=[layer], initial_view_state=view_state)
r.to_html('map.html')
