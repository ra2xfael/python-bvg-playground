import bvg_api.request_handler as request_handler


class Stop:

    def __init__(self, id, name, location):
        self.id = id
        self.name = name
        self.location = location
        self.departures = set()

    def __repr__(self):
        return "[" + str(self.id) + ": " + str(self.name) + " " + str(self.location) + "]"

    def get_next_stops(self):

        return [connection.route[connection.get_index_in_route(self) + 1] for connection in self.departures
                if connection.get_index_in_route(self) < len(connection.route) - 1]

        # next_stops = [departure.route[departure.route.index(self) + 1] for departure in self.departures]
        # return next_stops
