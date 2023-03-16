import bvg_api.request_handler as request_handler

serialized_stops = []


def initialize_serialization_stop(name):
    request_handler.request_stop(name)


def load_stop(name):

    for stop in serialized_stops:
        if stop.key == name:
            print("Stop gefunden")
            return stop
    print("Serialisieren von " + name)
    initialize_serialization_stop(name)



def add_stop(stop):
    serialized_stops.append(stop)
    print("new stop serialized: " + stop.name)
