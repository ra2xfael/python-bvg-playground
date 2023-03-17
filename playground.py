import bvg_api.request_handler as request_handler
import bvg_api.loader as loader
import mapping.mapping as mapping
import threading
import time

RUNNING = True

# TODO: set mit bereits besuchten Haltestellen!

def visit_stop(mapper, visited_stops, stop):
    if stop not in visited_stops:
        visited_stops.add(stop)
        mapper.map_stop(stop)

def runner():
    visited_stops = set()

    main_stop = request_handler.stops[0]
    print(f"Suche von {main_stop}")
    mapper = mapping.Map(main_stop)
    visit_stop(mapper, visited_stops, main_stop)
    while RUNNING:
        # main_stop = request_handler.stops[0]
        next_stops = main_stop.get_next_stops()
        for stop in next_stops:
            if stop is None:
                continue
            visit_stop(mapper, visited_stops, stop)

        # [mapper.map_stop(reachable_stop) for reachable_stop in next_stops]
        time.sleep(1)


request_handler.fetch_stop("Zoologischer Garten")

queue_thread = threading.Thread(target=request_handler.process_queue, daemon=True)
queue_thread.start()

print("start sleeping")
time.sleep(5)
print("waking up")
runner()

# mapping.init_map(main_stop)

# stop_request = request_handler.StopRequest("900023101")
# stop_request.run()
# stop_request.serialize()
