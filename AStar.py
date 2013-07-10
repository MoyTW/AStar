__author__ = 'Travis Moy'

# This is an implementation of the A* pathfinding algorithm.
#
# It is designed to be usable in as many different situations as possible, with as many different types of nodes as
# possible. Therefore, it does not directly manipulate any of the data, and may be used with any data format the user
# would like. For example, this code may be used with a standard 2-D grid of cells which can be traversed diagonally,
# a grid of hexes, a navigation mesh, or any arbitrary graph.
#
# However, this flexibility means that it does not touch the underlying data, and therefore the user must define the
# following functions:
#
#   A function which determines what nodes are adjacent to any given node with the following signature:
#       iterable<node_coordinate> f(node_coordinate)
#
#   A function to calculate the move cost for moving to an adjacent node with the following signature:
#       int f(node_coordinate, node_coordinate)
#           Note that the order in which the adjacent nodes are presented will change the bias of the algorithm! In case
#           of ties in f-values between two options, it will go with the first presented, which is the first option
#           from this function.
#
#   A function which determines whether a given node is passable with the following signature:
#       bool f(node_coordinate)
#
#   A function which estimates the movement cost between two given nodes with the following signature:
#       int f(node_coordinate, node_coordinate)
#
# Given these functions, find_path() will return a tuple of coordinates (in whatever format you supplied them)
# indicating the path to be taken from the origin to the destination.


# Returns a tuple of coordinates, from the origin to the destination.
def find_path(origin, destination,
              func_list_adjacent_nodes,
              func_calculate_move_cost,
              func_node_is_passable,
              func_estimate_cost):
    if origin == destination:
        return []

    start_node = NodeEntry(origin, None, 0, func_estimate_cost(origin, destination))

    open_nodes = [start_node]
    closed_nodes = []
    done = False
    while len(open_nodes) > 0 and not done:
        done = _process_next_node(open_nodes, closed_nodes, destination, func_list_adjacent_nodes,
                                  func_node_is_passable, func_calculate_move_cost, func_estimate_cost)
    return _return_path(origin, destination, closed_nodes)


def _process_next_node(open_nodes, closed_nodes, destination,
                       func_list_adjacent_nodes,
                       func_node_is_passable,
                       func_calculate_move_cost,
                       func_estimate_cost):
    open_nodes.sort()  # Not ideal, because it sorts every time - even if we don't need to.
    target = open_nodes.pop(0)
    closed_nodes.append(target)

    # !End condition! We have found the target!
    if target == destination:
        return True

    adjacent_nodes = func_list_adjacent_nodes(target.coordinates)
    _process_adjacent_nodes(target, adjacent_nodes, open_nodes, closed_nodes, destination,
                            func_node_is_passable, func_calculate_move_cost, func_estimate_cost)

    return False


def _process_adjacent_nodes(origin, adjacent_nodes, open_nodes, closed_nodes, destination,
                            func_node_is_passable,
                            func_calculate_move_cost,
                            func_estimate_cost):
    for coordinates in adjacent_nodes:
        if func_node_is_passable(coordinates) and (coordinates not in closed_nodes):
            new_g = origin.g + func_calculate_move_cost(origin.coordinates, coordinates)

            if coordinates not in open_nodes:
                new_node = NodeEntry(coordinates=coordinates,
                                     parent=origin,
                                     g=new_g,
                                     h=func_estimate_cost(coordinates, destination))
                open_nodes.append(new_node)
            else:
                existing_node = open_nodes[open_nodes.index(coordinates)]
                if new_g < existing_node.g:
                    existing_node.g = new_g
                    existing_node.parent = origin


def _return_path(origin, destination, closed_nodes):
    if destination in closed_nodes:
        path = list()
        end_node = closed_nodes[closed_nodes.index(destination)]
        parent_node = end_node.parent
        path.insert(0, end_node.coordinates)
        while parent_node != origin:
            end_node = parent_node
            parent_node = end_node.parent
            path.insert(0, end_node.coordinates)
        return path
    else:
        return []


# NodeEntry is an internal helper class.
#
# g = cost to move to this node along the best known path
# h = estimate of cost to destination from this node
# f = total estimated cost for travel to destination from this node
#
# This class has to methods of comparison - equality utilizing coordinates, and gt/lt/le/ge utilizing f.
# See the comments below for more info.
class NodeEntry(object):
    def __init__(self, coordinates, parent, g, h):
        self.coordinates = coordinates
        self.parent = parent
        self.g = g
        self.h = h

    @property
    def f(self):
        return self.g + self.h

    # So, we're doing something not recommended here.
    #
    # We've defined __eq__ and __ne__, but *not* the other rich comparison methods.
    # We've also defined __cmp__.
    # What this will do is allows us to use the equality-based functions ('in' or '==') while also allowing us to use
    # the built-in sorting algorithms, as the sorting algorithms fall back on __cmp__ if the rich comparison operators
    # (__lt__, __gt__, etc) are not defined.
    #
    # This is a terrible, hacky thing to do, and it doesn't work in Python 3, where they removed __cmp__. Never do it.
    def __ne__(self, other):
        return not self == other

    # We allow valid comparisons with coordinates, as well as NodeEntry instances.
    #
    # This is another hacky thing to do which should be avoided.
    def __eq__(self, other):
        try:
            return self.coordinates == other.coordinates
        except AttributeError:
            return self.coordinates == other

    def __cmp__(self, other):
        return cmp(self.f, other.f)