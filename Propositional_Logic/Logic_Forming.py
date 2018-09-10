from typing import List, Dict
from sympy import *
from sympy.logic.boolalg import to_cnf
from sympy.abc import A, B, D
from sympy.logic.inference import satisfiable
from sympy import Symbol
from collections import namedtuple

class Logic_Forming(object):
    def __init__(self):
        self.symbol: Dict[str, str] = {}

    def __getattr__(self, attr):
        return self.data[attr]

#print(to_cnf(~(A | B) | D))
def resolution(propositional_list, alpha):
    index = None
    propositional_list.push(~alpha)
    for index, value in enumerate(propositional_list):
        val = propositional_list.pop(index)
        for next_prop in propositional_list:
            simplified = next_prop & val
            if val == False:
                return True
        propositional_list.insert(index, val)
    return False

def visit_Square(world_matrix, start_pos):
    DownPoint, LeftPoint, RightPoint, UpPoint = define_Next_Points()
    next_point = allPoints(DownPoint, LeftPoint, RightPoint, UpPoint)
    point= create_Next_Point(next_point, start_pos)
    valid_boundary = boundary_Check(start_pos)
    if world_matrix[start_pos.x][start_pos.y] == "N":
        knowledge_Creation(point, start_pos, valid_boundary, "W", neg = True)


def knowledge_Creation(point, start_pos, valid_boundary, symboling, neg):
    down_point, left_point, right_point, up_point = point
    prop_symbol = []
    if valid_boundary.up:
        postrior = Symbol(symboling + str(up_point.x) + str(up_point.y))
        if neg:
            prop_symbol.append(~postrior)
        else:
            prop_symbol.append(postrior)
    if valid_boundary.down:
        postrior = Symbol(symboling + str(down_point.x) + str(down_point.y))
        if neg:
            prop_symbol.append(~postrior)
        else:
            prop_symbol.append(postrior)
    if valid_boundary.left:
        postrior = Symbol(symboling + str(left_point.x) + str(left_point.y))
        if neg:
            prop_symbol.append(~postrior)
        else:
            prop_symbol.append(postrior)
    if valid_boundary.right:
        postrior = Symbol(symboling + str(right_point.x) + str(right_point.y))
        if neg:
            prop_symbol.append(~postrior)
        else:
            prop_symbol.append(postrior)
    prior = symboling + str(start_pos.x) + str(start_pos.y)
    symbol = prop_symbol[0]
    for symb in prop_symbol[1:]:
        symbol = symbol | symb
    Logic.append(~Symbol(prior) >> symbol)


def allPoints(DownPoint, LeftPoint, RightPoint, UpPoint):
    NextPoints = namedtuple('NextPoints', ['DownPoint', 'LeftPoint', 'RightPoint', 'UpPoint'])
    next_point = NextPoints(DownPoint, LeftPoint, RightPoint, UpPoint)
    return next_point


def create_Next_Point(next_point, start_pos):
    DownPoint, LeftPoint, RightPoint, UpPoint = next_point
    up_x, up_y, down_x, down_y, right_x, right_y, left_x, left_y = None, None, None, None, None, None, None, None
    up_point = UpPoint(x=up_x, y=up_y)
    down_point = DownPoint(x=down_x, y=down_y)
    left_point = LeftPoint(x=left_x, y=left_y)
    right_point = RightPoint(x=right_x, y=right_y)

    return down_point, left_point, right_point, up_point


def define_Next_Points():
    UpPoint = namedtuple('UpPoint', ['x', 'y'])
    DownPoint = namedtuple('DownPoint', ['x', 'y'])
    LeftPoint = namedtuple('LeftPoint', ['x', 'y'])
    RightPoint = namedtuple('RightPoint', ['x', 'y'])
    return DownPoint, LeftPoint, RightPoint, UpPoint


def boundary_Check(current_pos):
    x, y = current_pos
    up, down, left, right = False, False, False, False
    if not y == 9:
        up_x, up_y = x, y + 1
        up = True
    if not y == 0:
        down_x, down_y = x, y - 1
        down = True
    if not x == 9:
        right_x, right_y = x + 1, y
    if not x == 0:
        left_x, left_y = x - 1, y
    BoundaryChecking = namedtuple('BoundaryChecking', ['up', 'down', 'left', 'right'])
    boundary = BoundaryChecking(up=up, down=down, left=left, right=right)

    boundary = BoundaryChecking(up=up, down=down, left=left, right=right)


    return boundary

def formulate_knowledge(boundary):
    pass

#
# x = Symbol('x')
# y = Symbol('y')
# z = Symbol('z')
# print(to_cnf(~(x | y) | z))
# print(satisfiable(x & ~x))
# print(satisfiable((x | y) & (x | ~y) & (~x | y)))
if __name__ == "__main__":
    KB = []
    Logic = []
    world_matrix = [[]]
    Start_Position = namedtuple('Start_Position', ['x', 'y'])
    start_pos = Start_Position(x = 2, y= 3)
    visit_Square(world_matrix, start_pos)
