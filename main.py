import pydeck as pdk

data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-0.89, 41.64],
                    [-0.88, 41.64],
                    [-0.88, 41.65],
                    [-0.89, 41.65],
                    [-0.89, 41.64]
                ]]
            }
        }
    ]
}

layer = pdk.Layer(
    "GeoJsonLayer",
    data,
    extruded=True,
    get_elevation=100,
    get_fill_color=[255, 0, 0],
)

view = pdk.ViewState(
    latitude=41.6488,
    longitude=-0.8891,
    zoom=14,
    pitch=45
)

deck = pdk.Deck(layers=[layer], initial_view_state=view)
deck.to_html("map.html")
