from typing import List


class boxNode(object):

    def __init__(self):
        self.stench = False
        self.breeze = False
        self.wumpus = False
        self.pit = False
        self.glitter = False
        self.previous_node = None
        self.next_nodes = []

    def __repr__(self):
        return "{0: >17s}".format(self.stench * "stench " + self.breeze * "breeze " + self.wumpus * "wumpus" + self.pit * "pit" + self.glitter * "glitter")

def boundary_check(x,y):
    if x > 9 or x < 0 or y > 9 or y < 0:
        return False
    return x, y

def board (wumpus_number, pit_number):
    _board = [[boxNode() for i in range(10)] for i in range(10)]
    wumpus, pit, glitter = random_board_generation(wumpus_number, pit_number)
    set_adjacent_box(_board, wumpus, "wumpus")
    set_adjacent_box(_board, pit, "pit")
    set_adjacent_box(_board, glitter)
    print_board(_board)
    return _board


def print_board(_board):
    print("-" * 180)
    for i in range(10):
        print("|", end="")
        for j in range(10):
            print(_board[i][j], end="|")
        print()
        print("-" * 180)
        # print()
    # import pprint
    # pprint.pprint(_board)


def set_adjacent_box(_board, danger_attr, danger_type= "glitter"):
    if danger_type == "glitter":
        x, y = danger_attr
        _board[x][y].glitter = True
        return
    for pos in danger_attr:
        x, y = pos
        if danger_type == "wumpus":
            _board[x][y].wumpus = True
        if danger_type == "pit":
            _board[x][y].pit = True
        valid = [boundary_check(x + 1, y), boundary_check(x, y + 1), boundary_check(x - 1, y), boundary_check(x, y - 1)]
        for val in valid:
            if val:
                x_adjacent, y_adjacent = val
                if danger_type == "wumpus":
                    _board[x_adjacent][y_adjacent].stench = True
                if danger_type == "pit":
                    _board[x_adjacent][y_adjacent].breeze = True


def random_board_generation(wupmus_number, pit_number):
    import random
    abstract_position = random.sample(range(2, 100), wupmus_number+pit_number+2)
    try:
        pos_10 = abstract_position.index(10)
        abstract_position.pop(pos_10)
    except ValueError:
        abstract_position = abstract_position[:-1]
    print(abstract_position)
    board_data = [(val//10, val % 10) for val in abstract_position]
    return board_data[:wupmus_number], board_data[wupmus_number:-1], board_data[-1]


class atomic_sentence(object):
    def __init__(self, term, is_pos):
        self.term = term
        self.is_pos = is_pos

    def __repr__(self):
        return (not self.is_pos)*"~"+str(self.term)

def logic_factory(co_ordinate, type, is_neg):
    x, y = co_ordinate
    valid = [(x,y),boundary_check(x + 1, y), boundary_check(x, y + 1), boundary_check(x - 1, y), boundary_check(x, y - 1)]
    key = type+str(x)+str(y)

    if is_neg and type == "S":
        neg_stench[key] = []
        for cor in valid:
            if cor:
                adjacent_x, adjacent_y = cor
                adjacent_node = "W"+str(adjacent_x)+str(adjacent_y)
                neg_stench[key].append(atomic_sentence(adjacent_node, False))

    elif is_neg and type == "B":
        neg_breeze[key] = []
        for cor in valid:
            if cor:
                adjacent_x, adjacent_y = cor
                adjacent_node = "P"+str(adjacent_x)+str(adjacent_y)
                neg_breeze[key].append(atomic_sentence(adjacent_node, False))

    elif not is_neg and type == "S":
        stench[key] = []
        for cor in valid:
            if cor:
                adjacent_x, adjacent_y = cor
                adjacent_node = "W" + str(adjacent_x) + str(adjacent_y)
                stench[key].append(atomic_sentence(adjacent_node, True))
                del adjacent_node
    elif not is_neg and type == "B":
        breeze[key] = []
        for cor in valid:
            if cor:
                adjacent_x, adjacent_y = cor
                adjacent_node = "P" + str(adjacent_x) + str(adjacent_y)
                breeze[key].append(atomic_sentence(adjacent_node, True))
                del adjacent_node

def logic_formulation(co_ordinate,current_state):
    if current_state=="Blank":
        logic_factory(co_ordinate, "S", is_neg=True)
        logic_factory(co_ordinate, "B", is_neg=True)
    if current_state =="Stench":
        logic_factory(co_ordinate, "S", is_neg=False)

    if current_state =="Breeze":
        logic_factory(co_ordinate, "B", is_neg=False)
    #print(neg_breeze,neg_stench, breeze, stench,sep="\n")
    print(co_ordinate)




def current_box(co_ordinate, _board:List[List[boxNode]]):
    x,y = co_ordinate
    if not _board[x][y].stench and not _board[x][y].breeze:
        logic_formulation(co_ordinate, "Blank")
    if _board[x][y].stench:
        logic_formulation(co_ordinate, "Stench")
    if _board[x][y].breeze:
        logic_formulation(co_ordinate, "Breeze")

def backward_chaining(fringe, board):
    if not fringe.empty():
        x, y = fringe.get()
    #resulation here
    if board[x][y].glitter ==True:
        print("Here", x, y)
        print("Found")
        exit()
    valid = [boundary_check(x + 1, y), boundary_check(x, y + 1), boundary_check(x - 1, y),
             boundary_check(x, y - 1)]
    for cor in valid:
        if cor:
            fringe.put(cor)
    current_box((x,y),board)
    backward_chaining(fringe, board)


if __name__ == "__main__":
    #print(wumpus,pit, glitter)
    neg_stench = {}
    stench =  {}
    neg_breeze = {}
    breeze = {}
    board = board(wumpus_number=3, pit_number=6)
    #logic_formulation((0,0), "Blank")
    import queue
    fringe = queue.LifoQueue()
    fringe.put((0,0))
    backward_chaining(fringe, board)
