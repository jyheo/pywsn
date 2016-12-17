
class Node:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.sensing_range = 15
        self.wireless_range = 50

    def move(self, x, y):
        self.x = x
        self.y = y


class SensingPoints:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.id = 0
        self.coverd_sensors = []


class SensingArea:
    def __init__(self):
        self.width = 100
        self.height = 100
        self.grid_size = 10
        self.generate_sensing_points()

    def generate_sensing_points(self):
        p = SensingPoints()
        self.sensing_points = [p]

    def get_covered_points_by(self, sensor):
        """
        find points covered by the sensor whose sesnor.x sensor.y sensor.sensing_range
        :type sensor: Node
        """
        return []



sa = SensingArea()
n = Node()
n.move(1, 1)
nodes = [n]

coverd_points = sa.get_covered_points_by(n)



