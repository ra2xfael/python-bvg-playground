import time

import bvg_api.request_handler as request_handler
import threading

serialized_stops = []
serialized_connections = []
lock = threading.Lock()



def load_stop(name):
    for stop in serialized_stops:
        if stop.name == name:
            print("Stop gefunden")
            return stop
    request_handler.fetch_stop(name)

def load_connection(id):
    print(serialized_connections)
    for connection in serialized_connections:
        if connection.id == id:
            print("Connection gefunden")
            return connection
    request_handler.fetch_connections(id)

def add_stops(stops):
    with lock:

        serialized_stops.append(stop)


def add_connection(connections):
    with lock:
        serialized_connections.append(connections)


def synchronize_fetched_data():
    while True:
        time.sleep(5)
        with lock:
            serialized_stops.append(request_handler.ready_stops)

            serialized_connections.append(request_handler.ready_connections)
            [load_connection(departures_id) for departures_id in request_handler.ready_departures_id]
            print(serialized_connections)
            print(serialized_stops)
