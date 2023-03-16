import requests
import threading
import time
import traffic.stop as stop
import bvg_api.loader as loader

STOP_URL = "http://v6.bvg.transport.rest/locations"
QUEUE_PROCESSING = True

queue = []
lock = threading.Lock()


def fetch_stop(name):
    with lock:
        queue.append(StopRequest(name))


def process_queue():
    while QUEUE_PROCESSING:
        if len(queue) > 0:
            with lock:
                request = queue.pop(0)
            request.fetch()
            request.serialize()
            time.sleep(1)
            continue
        print(".", end="")
        time.sleep(2)


class Request:

    def fetch(self):
        pass

    def serialize(self):
        pass


class StopRequest(Request):

    def __init__(self, key):
        self.key = key
        self.response = None

    def fetch(self):
        super()
        parameters = {"query": self.key, "stops": "true", "adresses": "false", "poi": "false", "linesOfStops": "true"}
        request = requests.get(STOP_URL, parameters)
        self.response = [location for location in request.json() if location["type"] == "stop"][0]
        return request.json()

    def serialize(self):
        id = self.response["id"]
        name = self.response["name"]
        location = [self.response["location"]["latitude"], self.response["location"]["longitude"]]
        new_stop = stop.Stop(id, name, location)
        loader.add_stop(new_stop)

    # self.response = [{'type': 'stop', 'id': '900023101', 'name': 'U Ernst-Reuter-Platz (Berlin)', 'location': {'type': 'location', 'id': '900023101', 'latitude': 52.511584, 'longitude': 13.32258}, 'products': {'suburban': False, 'subway': True, 'tram': False, 'bus': True, 'ferry': False, 'express': False, 'regional': False}, 'lines': [{'type': 'line', 'id': 'u2', 'fahrtNr': None, 'name': 'U2', 'public': True, 'mode': 'train', 'product': 'subway'}, {'type': 'line', 'id': '245', 'fahrtNr': None, 'name': '245', 'public': True, 'mode': 'bus', 'product': 'bus'}, {'type': 'line', 'id': 'm45', 'fahrtNr': None, 'name': 'M45', 'public': True, 'mode': 'bus', 'product': 'bus'}, {'type': 'line', 'id': 'n2', 'fahrtNr': None, 'name': 'N2', 'public': True, 'mode': 'bus', 'product': 'bus'}], 'stationDHID': 'de:11000:900023101'},
    #                  {'type': 'stop', 'id': '900093151', 'name': 'Dohnensteig (Berlin)', 'location': {'type': 'location', 'id': '900093151', 'latitude': 52.605297, 'longitude': 13.291486}, 'products': {'suburban': False, 'subway': False, 'tram': False, 'bus': True, 'ferry': False, 'express': False, 'regional': False}, 'lines': [{'type': 'line', 'id': '125', 'fahrtNr': None, 'name': '125', 'public': True, 'mode': 'bus', 'product': 'bus'}, {'type': 'line', 'id': 'n25', 'fahrtNr': None, 'name': 'N25', 'public': True, 'mode': 'bus', 'product': 'bus'}], 'stationDHID': 'de:11000:900093151'}, {'type': 'location', 'id': None, 'latitude': 52.513148, 'longitude': 13.321717, 'address': '10587 Berlin-Charlottenburg, Ernst-Reuter-Platz'},
    #                  {'type': 'location', 'id': None, 'latitude': 52.535873, 'longitude': 13.385594, 'address': '13355 Berlin-Gesundbrunnen, Ernst-Reuter-Siedlung'},
    #                  {'type': 'stop', 'id': '900034101', 'name': 'U Paulsternstr. (Berlin)', 'location': {'type': 'location', 'id': '900034101', 'latitude': 52.538129, 'longitude': 13.248068}, 'products': {'suburban': False, 'subway': True, 'tram': False, 'bus': True, 'ferry': False, 'express': False, 'regional': False}, 'lines': [{'type': 'line', 'id': 'u7', 'fahrtNr': None, 'name': 'U7', 'public': True, 'mode': 'train', 'product': 'subway'}, {'type': 'line', 'id': '139', 'fahrtNr': None, 'name': '139', 'public': True, 'mode': 'bus', 'product': 'bus'}, {'type': 'line', 'id': 'n7', 'fahrtNr': None, 'name': 'N7', 'public': True, 'mode': 'bus', 'product': 'bus'}, {'type': 'line', 'id': 'n39', 'fahrtNr': None, 'name': 'N39', 'public': True, 'mode': 'bus', 'product': 'bus'}], 'stationDHID': 'de:11000:900034101'}]
    #
