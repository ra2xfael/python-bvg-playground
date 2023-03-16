import folium


def init_map(init_stop):
    print("Mapping initialized")
    folium.Marker(location=init_stop.location).add_to(map)
    map.save("map.html")
    return map


def map_stop(map, stop):
    print(f"Added {stop.name}")
    folium.Marker(location=stop.location).add_to(map)
    map.save("map.html")
