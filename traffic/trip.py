
class Connection:

    def __init__(self, id, name, type, route):
        self.id = id
        self.name = name
        self.type = type
        self.route = route

    def get_index_in_route(self, searched_stop):
        for stop in self.route:
            if stop.id == searched_stop.id:
                return self.route.index(stop)
        return -1



    def __repr__(self):
        #return "[" + str(self.id) + ": " + str(self.name) + " " + self.location + "]"
        return f"[{self.name} ({self.id}) [{self.type}]"