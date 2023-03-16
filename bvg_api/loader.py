import bvg_api.request_handler as request_handler
import threading

serialized_stops = []
lock = threading.Lock()



def load_stop(name):
    for stop in serialized_stops:
        if stop.name == name:
            print("Stop gefunden")
            return stop
    print("Serialisieren von " + name)
    request_handler.fetch_stop(name)



def add_stop(stop):
    print("new stop serialized: " + stop.name)
    with lock:
        serialized_stops.append(stop)
