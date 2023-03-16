import threading
import time
import bvg_api.request as request
import traffic.stop as stop
import traffic.trip as trip
import mapping.mapping as mapping

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
        queue.append(request.DepartureRequest(stop, int(time.time()), 15))


def fetch_connections(id):
    with lock:
        queue.append(request.ConnectionRequest(id))


def save_stop(stop):
    for saved_stop in stops:
        if saved_stop.id == stop.id:
            print(f"{stop.name} bereits gespeichert.")
            return
    fetch_departures(stop)
    stops.append(stop)



def process_departures(departures):
    for departure_id in departures:
        fetch_connections(departure_id)


def save_connection(connection):
    connections.append(connection)
    for stop in connection.route:
        save_stop(stop)


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
