import bvg_api.request_handler as request_handler
import bvg_api.loader as loader
import mapping.mapping as mapping
import threading
import time

request_handler.fetch_stop("Helene-Weigel")

queue_thread = threading.Thread(target=request_handler.process_queue)
queue_thread.start()
time.sleep(2)

main_stop = request_handler.stops[0]
mapping.init_map(main_stop)

# stop_request = request_handler.StopRequest("900023101")
# stop_request.run()
# stop_request.serialize()
