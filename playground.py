import bvg_api.request_handler as request_handler
import bvg_api.loader as loader
import threading
import time

request_handler.fetch_stop("Helene-Weigel")

queue_thread = threading.Thread(target=request_handler.process_queue)
queue_thread.start()
update_thread = threading.Thread(target=loader.synchronize_fetched_data())
update_thread.start()

while True:
    input()



# stop_request = request_handler.StopRequest("900023101")
# stop_request.run()
# stop_request.serialize()
