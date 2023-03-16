import bvg_api.request_handler as request_handler
import bvg_api.loader as loader
import asyncio

loader.load_stop("Helene-Weigel")
asyncio.run(request_handler.process_queue())


# stop_request = request_handler.StopRequest("900023101")
# stop_request.run()
# stop_request.serialize()

