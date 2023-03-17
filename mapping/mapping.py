import folium


class Map:

    def __init__(self, init_stop):
        print(f"Mapping initialized with {init_stop.name}")
        self.map = folium.Map(location=init_stop.location, zoom_start=15)
        folium.Marker(location=init_stop.location).add_to(self.map)
        self.map.save("map.html")

    def map_stop(self, stop):
        print(f"Added {stop.name}")
        folium.Marker(location=stop.location).add_to(self.map)
        self.map.save("map.html")
