import threading
import time

import folium

import bvg_api.request as request
import traffic.stop as stop
import traffic.trip as trip
import mapping.mapping as mapping

QUEUE_PROCESSING = True

queue = []

stops = {}
departures_id = []
connections = {}

chart = None

lock = threading.Lock()



def get_stop(key):
    if key in stops:
        return stops["id"]
    else:
        fetch_stop(key)


def fetch_stop(name):
    with lock:
        queue.append(request.StopRequest(name))


def fetch_departures(stop):
    with lock:
        queue.append(request.DepartureRequest(stop, int(time.time()), 10))


def fetch_connections(id):
    with lock:
        queue.append(request.ConnectionRequest(id))


def add_stop(stop_to_add):
    if stop_to_add.id in stops:
        return False
    stops[stop_to_add.id] = stop_to_add
    return True

def add_departure_to_stop(stop, connection):
    # for saved_stop in stops:
    #     if saved_stop.id == stop.id:
    #         saved_stop.departures.add(connection)
    if stop.id in stops:
        stops[stop.id].departures.add(connection)


def save_stop(stop):
    if add_stop(stop):
        fetch_departures(stop)


def process_departures(departures):
    for departure_id in departures:
        fetch_connections(departure_id)


def save_connection(connection):
    connections[connection.id] = connection
    print(f"Speicher von {connection}")
    for stop_in_connection in connection.route:
        add_stop(stop_in_connection)
        add_departure_to_stop(stop_in_connection, connection)


def save_serialization(serialization):
    if type(serialization) == stop.Stop:
        save_stop(serialization)
    elif type(serialization) == list:
        process_departures(serialization)
    elif type(serialization) == trip.Connection:
        save_connection(serialization)
    else:
        fetch_connections(serialization)


def process_queue():
    while QUEUE_PROCESSING:
        if len(queue) > 0:
            with lock:
                request = queue.pop(0)
            request.fetch()
            save_serialization(request.serialize())  # Ergebnis verwenden
            time.sleep(1)
            continue
        print(".", end="")
        time.sleep(2)
