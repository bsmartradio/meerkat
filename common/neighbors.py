from common import build_center
from common import build_neighbor

class Neighbors:

    left = []
    center_left = []
    center_right = []
    right = []

    def __init__(self):

        self.center_left = build_center.BuildCenter()
        self.center_right = build_center.BuildCenter()
        self.left = build_neighbor.BuildNeighbor()
        self.right = build_neighbor.BuildNeighbor()