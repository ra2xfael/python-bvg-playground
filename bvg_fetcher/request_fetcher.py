import threading
import time

import traffic.stop
import traffic.trip
import request

request_queue = []

stops = []
connections = {}

lock = threading.Lock()


def fetch_stop(lookup_key):
    with lock:
        request_queue.append(request.StopRequest(lookup_key))


def fetch_departures(stop):
    with lock:
        request_queue.append(request.DepartureRequest(stop, int(time.time()), 10))


def fetch_trip(departure_id):
    with lock:
        request_queue.append(request.ConnectionRequest(departure_id))



def add_stop(new_stop):
    for stop in stops:
        if stop.id == new_stop.id:
            return
    stops.append(new_stop)


def process(serialization):
    if type(serialization) == traffic.stop.Stop:
        add_stop(serialization)
    elif type(serialization) == list:
        [fetch_trip(trip_id) for trip_id in serialization]
    elif type(serialization) == traffic.trip.Connection:
        [add_stop(stop) for stop in serialization.route]
        for i in range(0, len(serialization.route) + 1):
            connections[serialization.route[i]].append(serialization.route[i + 1])





def process_queue():
    while True:
        if len(request_queue) > 0:
            with lock:
                request = request_queue.pop(0)
            request.fetch()
            process(request.serialize)
            time.sleep(1)
            continue
        print(".", end="")
        time.sleep(2)
