import pydeck as pdk
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TOMTOM_API_KEY")

url = "https://api.tomtom.com/traffic/services/5/incidentDetails"

params = {
    "key": API_KEY,
    "bbox": "-0.95,41.60,-0.80,41.72",
    "fields": "{incidents{type,geometry{type,coordinates},properties{iconCategory}}}",
    "language": "en-GB",
    "timeValidityFilter": "present"
}

response = requests.get(url, params=params)
data = response.json()

points = []

# Category names
category_names = {
    1: "Accident",
    2: "Fog",
    3: "Dangerous conditions",
    4: "Rain",
    5: "Ice",
    6: "Traffic jam",
    7: "Lane closed",
    8: "Road closed",
    9: "Road works",
    10: "Wind",
    11: "Flooding",
    14: "Broken down vehicle"
}

# Height mapping (severity proxy)
category_height = {
    1: 600,  # Accident
    6: 500,  # Traffic jam
    8: 550,  # Road closed
    9: 400,  # Road works
    7: 350,  # Lane closed
    14: 250,  # Broken vehicle
    3: 300,  # Dangerous conditions
    11: 450  # Flooding
}

# Color mapping
category_colors = {
    1: [255, 0, 0],  # Accident - red
    6: [255, 140, 0],  # Traffic jam - orange
    8: [180, 0, 255],  # Road closed - purple
    9: [255, 215, 0],  # Road works - yellow
    7: [255, 100, 100],  # Lane closed
    14: [120, 120, 120],  # Broken vehicle - grey
    3: [255, 80, 80],  # Dangerous
    11: [0, 120, 255],  # Flood
}

# Parse incidents
if "incidents" in data:
    for incident in data["incidents"]:
        geometry = incident["geometry"]
        coords = geometry["coordinates"]
        geo_type = geometry["type"]

        category = incident["properties"]["iconCategory"]
        category_name = category_names.get(category, "Unknown")

        height = category_height.get(category, 200)
        color = category_colors.get(category, [200, 200, 200])

        if geo_type == "Point":
            points.append({
                "lng": coords[0],
                "lat": coords[1],
                "category": category_name,
                "height": height,
                "color": color
            })

        elif geo_type == "LineString":
            for coord in coords:
                points.append({
                    "lng": coord[0],
                    "lat": coord[1],
                    "category": category_name,
                    "height": height,
                    "color": color
                })

print("Incidents:", len(points))

# 3D Incident columns
incident_layer = pdk.Layer(
    "ColumnLayer",
    data=points,
    get_position='[lng, lat]',
    get_elevation='height',
    elevation_scale=1,
    radius=40,
    get_fill_color='color',
    pickable=True,
    extruded=True,
    auto_highlight=True
)

# 3D buildings layer
buildings = pdk.Layer(
    "PolygonLayer",
    "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json",
    get_polygon="geometry.coordinates",
    extruded=True,
    get_elevation="properties.valuePerSqm",
    elevation_scale=5,
    get_fill_color=[160, 160, 180],
    pickable=False
)

# Camera
view_state = pdk.ViewState(
    longitude=-0.8773,
    latitude=41.6488,
    zoom=13,
    pitch=45,
    bearing=0
)

deck = pdk.Deck(
    layers=[buildings, incident_layer],
    initial_view_state=view_state,
    tooltip={"text": "Incident: {category}"}
)

deck.to_html("map.html")

print("It wooorked")
