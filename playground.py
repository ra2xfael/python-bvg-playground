import bvg_api.request_handler as request_handler
import bvg_api.loader as loader
import threading

loader.load_stop("Helene-Weigel")
loader.load_stop("Rathaus Spandau")
loader.load_stop("Fehrbelliner Platz")
loader.load_stop("Freie Universität")
loader.load_stop("Ernst-Reuter")
loader.load_stop("S+U Südkreuz")

queue_thread = threading.Thread(target=request_handler.process_queue)
queue_thread.start()

# stop_request = request_handler.StopRequest("900023101")
# stop_request.run()
# stop_request.serialize()
