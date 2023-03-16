
class Connection:

    def __init__(self, id, name, type, route):
        self.id = id
        self.name = name
        self.type = type
        self.route = route

    def __repr__(self):
        return "[" + str(self.id) + ": " + str(self.name) + " " + str(self.location) + "]"