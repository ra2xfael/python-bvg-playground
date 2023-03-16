class Stop:

    def __init__(self, id, name, location):
        self.id = id
        self.name = name
        self.location = location

    def __repr__(self):
        return "[" + str(self.id) + ": " + str(self.name) + " " + str(self.location) + "]"

    def get_possible_stops(self):
        None

