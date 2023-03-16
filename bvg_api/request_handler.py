import threading
import time
import bvg_api.request as request
import traffic.stop as stop
import traffic.trip as trip

QUEUE_PROCESSING = True

queue = []

stops = []
departures_id = []
connections = []

lock = threading.Lock()

def get_stop(id):
    result = [stop for stop in stops if stop.id == id]
    if result is None:
        fetch_stop(id)
    else:
        return result


def fetch_stop(name):
    with lock:
        queue.append(request.StopRequest(name))

def fetch_departures(stop):
    with lock:
        queue.append(request.DepartureRequest(stop))

def fetch_connections(id):
    with lock:
        queue.append(request.ConnectionRequest(id))


def save_stop(stop):
    fetch_departures(stop)
    stops.append(stop)


def process_departures(departures):
    pass

def save_connection(connection):
    pass

def save_serialization(serialization):
    print(serialization)
    if type(serialization) == stop.Stop:
        save_stop(stop)
    elif type(serialization) == trip.Connection:
        pass
    else:
        fetch_connections(serialization)

def process_queue():
    while QUEUE_PROCESSING:
        if len(queue) > 0:
            with lock:
                request = queue.pop(0)
            request.fetch()
            save_serialization(request.serialize()) # Ergebnis verwenden
            time.sleep(1)
            continue
        print(".", end="")
        time.sleep(2)


