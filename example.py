__author__ = 'Travis Moy'

import math
import random
import AStar

# ExampleMap holds both a map (a 2-D array of True/False values indicating passability) and the four functions noted
# in AStar.
class ExampleMap(object):
    PROB_OBSTRUCTED = .25
    MAP_SIZE = 20

    def __init__(self):
        self.map = [[(lambda: self.PROB_OBSTRUCTED < random.uniform(0.0, 1.0))() for _ in range(self.MAP_SIZE)]
                    for _ in range(self.MAP_SIZE)]

    # Note that we're not checking to see if the nodes are valid coordinates.
    # That's because node_is_passable should handle running off the map!
    # Still, if you want to check, it won't hurt anything. It's just not necessary.
    def list_adjacent_nodes(self, coordinates):
        adjacent = list()
        adjacent.append((coordinates[0]+1, coordinates[1]+1))
        adjacent.append((coordinates[0]+1, coordinates[1]))
        adjacent.append((coordinates[0]+1, coordinates[1]-1))
        adjacent.append((coordinates[0], coordinates[1]+1))
        adjacent.append((coordinates[0]-1, coordinates[1]+1))
        adjacent.append((coordinates[0]-1, coordinates[1]))
        adjacent.append((coordinates[0]-1, coordinates[1]-1))
        adjacent.append((coordinates[0], coordinates[1]-1))
        return adjacent

    # Make sure that if the node is off the map, you return False.
    def node_is_passable(self, coordinates):
        try:
            return self.map[coordinates[0]][coordinates[1]]
        except IndexError:
            return False

    # This function calculates the move cost as the following:
    #   Horizontal/Vertical moves: 1
    #   Diagonal: .1
    # This strongly encourages diagonal movement - even when there's no real reason to do so!
    def calculate_move_cost(self, origin, destination):
        distance = math.sqrt(((destination[0] - origin[0]) * (destination[0] - origin[0])) +
                             ((destination[1] - origin[1]) * (destination[1] - origin[1])))
        if distance == 1.0:
            return 1
        else:
            return .1

    # Utilizes a square-root distance estimation.
    def estimate_cost(self, origin, destination):
        return math.sqrt(((destination[0] - origin[0]) * (destination[0] - origin[0])) +
                         ((destination[1] - origin[1]) * (destination[1] - origin[1])))

    def __repr__(self):
        repr_str = ''
        col = self.MAP_SIZE - 1
        while col >= 0:
            for row in range(self.MAP_SIZE):
                if self.node_is_passable((col, row)):
                    repr_str += '.'
                else:
                    repr_str += '#'
                repr_str += ' '
            repr_str += '\n'
            col -= 1
        return repr_str

em = ExampleMap()
print "The map (. is a passable square, # is an impassable square):"
print em


# This code is just to generate an empty start and end point for our algorithm to plot a path between.
def find_empty_coordinates(m):
    x = random.randint(0, m.MAP_SIZE)
    y = random.randint(0, m.MAP_SIZE)
    while not m.node_is_passable((x, y)):
        x = random.randint(0, m.MAP_SIZE)
        y = random.randint(0, m.MAP_SIZE)
    return x, y
origin = find_empty_coordinates(em)
destination = find_empty_coordinates(em)

# Here, we use the four functions defined back up in ExampleMap and generate a path.
path = AStar.find_path(origin, destination,
                       func_list_adjacent_nodes=em.list_adjacent_nodes,
                       func_calculate_move_cost=em.calculate_move_cost,
                       func_node_is_passable=em.node_is_passable,
                       func_estimate_cost=em.estimate_cost)
print "The path provided by the A* algorithm from", origin, "to", destination, "is:", path
print ''


def print_map_with_path(example, origin, destination, path):
    print_str = ''
    col = example.MAP_SIZE - 1
    while col >= 0:
        for row in range(example.MAP_SIZE):
            if (row, col) == origin:
                print_str += 'O'
            elif (row, col) == destination:
                print_str += 'D'
            elif (row, col) in path:
                print_str += 'x'
            elif example.node_is_passable((col, row)):
                print_str += ' '
            else:
                print_str += '#'
            print_str += ' '
        print_str += '\n'
        col -= 1
    print print_str

print "The map, with the path plotted. 'x' are the points on the path from origin 'O' to destination 'D':"
print_map_with_path(em, origin, destination, path)