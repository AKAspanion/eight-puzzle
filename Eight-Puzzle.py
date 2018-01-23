'''
    
    Author: Ankit Kumar Pandit
    Date: 24/01/2017
'''

import queue
import time


# stack data structure class for processing
class Stack:
    def __init__(self):
        self.stack = []

    def pop(self):
        if self.is_empty():
            return None
        else:
            return self.stack.pop()

    def push(self, val):
        return self.stack.append(val)

    def peek(self):
        if self.is_empty():
            return None
        else:
            return self.stack[-1]

    def size(self):
        return len(self.stack)

    def is_empty(self):
        return self.size() == 0


# This class stores all the information of a state and helps in forming the tree
class Node:
    # initializing the Node class with
    # x y, position of blank space or the coordinate(x, y) of 0 tile
    # m, 2d matrix representing the current state
    # p, object pointing to the parent of current state, i.e. previous state
    # co, cost to reach that state(determined by heuristic functions)
    # lvl, level of the current state in the tree or the depth
    def __init__(self, x, y, m=None, p=None, co=0, lvl=0):
        self.blank_x = x
        self.blank_y = y
        self.mat = m
        self.parent = p
        self.cost = co
        self.level = lvl

    # print all the details of the object [ for -debugging ]
    def print_details(self):
        print_matrix(self.mat)
        print("X Y", self.get_blank_pos_x(), self.get_blank_pos_y())
        print("Cost:", self.get_cost(), "Level:", self.get_level())

    # a overridden comparator necessary in making of priority queue
    def __cmp__(self, other):
        return (self.get_cost() + self.get_level()) < (other.get_cost() + other.get_level())

    # necessary in making of priority queue
    def __lt__(self, other):
        return (self.get_cost() + self.get_level()) < (other.get_cost() + other.get_level())

    # function to swap to coordinates in the matrix
    def swap(self, x, y, n_x, n_y):
        temp = self.mat[x][y]
        self.mat[x][y] = self.mat[n_x][n_y]
        self.mat[n_x][n_y] = temp

    # boolean function to check if one state is equal to the current state
    def equals(self, other):
        if self.mat == other.get_mat():
            return True
        else:
            return False

    # getter methods
    def get_level(self):
        return self.level

    def get_cost(self):
        return self.cost

    def get_blank_pos_x(self):
        return self.blank_x

    def get_blank_pos_y(self):
        return self.blank_y

    def get_mat(self):
        return self.mat

    def get_parent(self):
        return self.parent

    # setter methods
    def set_level(self, level):
        self.level = level

    def set_cost(self, cost):
        self.cost = cost

    def set_blank_pos_x(self, x):
        self.blank_x = x

    def set_blank_pos_y(self, y):
        self.blank_y = y

    def set_mat(self, m):
        self.mat = m

    def set_parent(self, p):
        self.parent = p


# -------------------------------
# all the helper functions below
# -------------------------------

# function to convert 2D matrix to 1D list, returns 1D array
def get_1d(x1):
    lst = [x1[0][0], x1[0][1], x1[0][2],
           x1[1][0], x1[1][1], x1[1][2],
           x1[2][0], x1[2][1], x1[2][2]]
    return lst


# function to convert 1D list to 2D matrix, returns 2D array
def get_2d(arr):
    matrix = [[arr[0], arr[1], arr[2]],
              [arr[3], arr[4], arr[5]],
              [arr[6], arr[7], arr[8]]]
    return matrix


# function to find the location of zero tile in the matrix, returns coordinate(x, y)
def get_zero_pos(matrix):
    for i in range(0, 3):
        for j in range(0, 3):
            if matrix[i][j] == 0:
                return i, j


# function to create an exact copy of a matrix, returns 2D array
def get_copy(x2):
    matrix = [[x2[0][0], x2[0][1], x2[0][2]],
              [x2[1][0], x2[1][1], x2[1][2]],
              [x2[2][0], x2[2][1], x2[2][2]]]
    return matrix


# helper function to create a new node, returns Node object
def new_node(x, y, new_x, new_y, cost, level, mat, parent):
    matrix = get_copy(mat)  # getting a copy of mat, directly passing mat in constructor will change other values
    node = Node(new_x, new_y, matrix, parent, cost, level)
    node.swap(x, y, new_x, new_y)
    return node


# function to calculate no of out of place tiles, returns integer
def cal_out_of_place_cost(initial, final):
    count = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if (initial[i][j] != 0) and (initial[i][j] != final[i][j]):
                count += 1  # counting all the tiles out of correct position
    return count


# helper function for manhattan distance calculation, returns coordinate(x, y)
def get_distance(n, final):
    for i in range(0, 3):
        for j in range(0, 3):
            if final[i][j] == n:
                return i, j    # returns correct coordinate of value n in final state


# function to calculate manhattan distance between initial state and final state, returns integer
def cal_man_dist(initial, final):
    man_dist = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if initial[i][j] == 0:  # leave blank position
                continue
            else:
                r, c = get_distance(initial[i][j], final)  # getting correct coordinate of tile
                man_dist += (abs(r-i) + abs(c-j))  # formula to calculate manhattan distance
    return man_dist


# boolean function to check if it is safe to move the zero tile in given coordinate
def is_safe(x, y):
    return (x >= 0) and (x < 3) and (y >= 0) and (y < 3)


# boolean function to check and avoid self looping among repeating states
def check_repeat(node):
    value = False
    check = node
    while check.get_parent() is not None and not value:
        if check.get_parent().equals(node):
            value = True   # if any repetition found then return True
            break
        check = check.get_parent()
    return value  # if no repetition found then return False


# function to print the matrix
def print_matrix(x3):
    print("-------------")
    print("|", x3[0][0], "|", x3[0][1], "|", x3[0][2], "|")
    print("|", x3[1][0], "|", x3[1][1], "|", x3[1][2], "|")
    print("|", x3[2][0], "|", x3[2][1], "|", x3[2][2], "|")
    print("-------------")


# recursive function to print all states till root
def print_states(root):
    if root is None:
        return
    print_states(root.get_parent())
    print_matrix(root.get_mat())
    print("\t  ↕")


# function that processes result display
def print_result(result):
    print_states(result[0])
    print("\tDONE.✓\n")
    print("*Average_Iterations: \t%s\n*Average_Steps: \t\t%s \n*Average_Time: \t\t\t%s seconds"
          % (result[1], result[2], result[3]))


# ---------------------------------
# all the algorithm functions below
# ---------------------------------

# Implementation of 8-Puzzle using Breadth First Search
def solve_bfs(initial, x, y, final):
    start_time = time.time()
    q = queue.Queue()   # creation of normal queue
    root = new_node(x, y, x, y, 0, 0, initial, None)
    q.put(root)  # en queue in queue
    count = 1
    while not q.empty():
        m = q.get()  # de queue from queue one by one for checking
        count += 1
        if m.get_mat() == final:  # if final state found then return with all data
            return [m, count, m.get_level(), (time.time() - start_time)]

        b_x = m.get_blank_pos_x()
        b_y = m.get_blank_pos_y()  # get position of tile 0

        # only 4 possible children by moving up, down, left, right

        if is_safe(b_x-1, b_y+0):  # check and shift 0 tile up
            child1 = new_node(b_x, b_y, (b_x-1), (b_y+0), m.get_cost()+1, (m.get_level()+1), m.get_mat(), m)
            if not check_repeat(child1):   # if not repeating
                q.put(child1)

        if is_safe(b_x+1, b_y+0):  # check and shift 0 tile down
            child2 = new_node(b_x, b_y, (b_x+1), (b_y+0), m.get_cost()+1, (m.get_level()+1), m.get_mat(), m)
            if not check_repeat(child2):
                q.put(child2)

        if is_safe(b_x+0, b_y-1):  # check and shift 0 tile left
            child3 = new_node(b_x, b_y, (b_x+0), (b_y-1), m.get_cost()+1, (m.get_level()+1), m.get_mat(), m)
            if not check_repeat(child3):
                q.put(child3)

        if is_safe(b_x+0, b_y+1):  # check and shift 0 tile right
            child4 = new_node(b_x, b_y, (b_x+0), (b_y+1), m.get_cost()+1, (m.get_level()+1), m.get_mat(), m)
            child4.set_cost(m.get_cost()+1)
            if not check_repeat(child4):
                q.put(child4)


# Implementation of 8-Puzzle using Depth First Search
def solve_dfs(initial, x, y, final):
    start_time = time.time()
    stack = Stack()  # creation of normal stack
    root = new_node(x, y, x, y, 0,  0, initial, None)
    stack.push(root)  # push root to stack
    count = 1
    while not stack.is_empty():
        m = stack.pop()  # pop from stack one by one for checking
        count += 1
        if m.get_mat() == final:
            return [m, count, m.get_level(), (time.time() - start_time)]

        b_x = m.get_blank_pos_x()
        b_y = m.get_blank_pos_y()  # get position of tile 0

        # only 4 possible children by moving up, down, left, right

        if is_safe(b_x - 1, b_y + 0):  # check and shift 0 tile up
            child1 = new_node(b_x, b_y, (b_x - 1), (b_y + 0), m.get_cost()+1, (m.get_level() + 1), m.get_mat(), m)
            if not check_repeat(child1):
                stack.push(child1)

        if is_safe(b_x + 1, b_y + 0):  # check and shift 0 tile down
            child2 = new_node(b_x, b_y, (b_x + 1), (b_y + 0), m.get_cost()+1, (m.get_level() + 1), m.get_mat(), m)
            if not check_repeat(child2):
                stack.push(child2)

        if is_safe(b_x + 0, b_y - 1):  # check and shift 0 tile left
            child3 = new_node(b_x, b_y, (b_x + 0), (b_y - 1), m.get_cost()+1, (m.get_level() + 1), m.get_mat(), m)
            if not check_repeat(child3):
                stack.push(child3)

        if is_safe(b_x + 0, b_y + 1):  # check and shift 0 tile right
            child4 = new_node(b_x, b_y, (b_x + 0), (b_y + 1), m.get_cost()+1, (m.get_level() + 1), m.get_mat(), m)
            if not check_repeat(child4):
                stack.push(child4)


# Implementation of 8-Puzzle using A Star Algorithm
def solve_a_star(initial, x, y, final, h):
    start_time = time.time()
    pq = queue.PriorityQueue()  # creation of priority queue
    if h == 'o':  # value of h decides the heuristic function
        root = new_node(x, y, x, y, cal_out_of_place_cost(initial, final), 0, initial, None)
    else:
        root = new_node(x, y, x, y, cal_man_dist(initial, final), 0, initial, None)
    pq.put(root)
    count = 1
    while not pq.empty():
        m = pq.get()   # de queue state with minimum cost ( priority queue )
        count += 1
        if m.get_cost() == 0:
            return [m, count, m.get_level(), (time.time() - start_time)]

        b_x = m.get_blank_pos_x()
        b_y = m.get_blank_pos_y()   # get position of tile 0

        # only 4 possible children by moving up, down, left, right

        if h == 'o':  # Implementation of Misplaced Tile Heuristic
            if is_safe(b_x-1, b_y+0):  # up
                child1 = new_node(b_x, b_y, (b_x-1), (b_y+0), 0, (m.get_level()+1), m.get_mat(), m)
                child1.set_cost(cal_out_of_place_cost(child1.get_mat(), final))  # cost my misplaced tile function
                if not check_repeat(child1):
                    pq.put(child1)
            if is_safe(b_x+1, b_y+0):  # down
                child2 = new_node(b_x, b_y, (b_x+1), (b_y+0), 0, (m.get_level()+1), m.get_mat(), m)
                child2.set_cost(cal_out_of_place_cost(child2.get_mat(), final))  # cost my misplaced tile function
                if not check_repeat(child2):
                    pq.put(child2)
            if is_safe(b_x+0, b_y-1):  # left
                child3 = new_node(b_x, b_y, (b_x+0), (b_y-1), 0, (m.get_level()+1), m.get_mat(), m)
                child3.set_cost(cal_out_of_place_cost(child3.get_mat(), final))  # cost my misplaced tile function
                if not check_repeat(child3):
                    pq.put(child3)
            if is_safe(b_x+0, b_y+1):  # right
                child4 = new_node(b_x, b_y, (b_x+0), (b_y+1), 0, (m.get_level()+1), m.get_mat(), m)
                child4.set_cost(cal_out_of_place_cost(child4.get_mat(), final))  # cost my misplaced tile function
                if not check_repeat(child4):
                    pq.put(child4)

        else:  # Implementation of Manhattan Distance Heuristic
            if is_safe(b_x - 1, b_y + 0):  # up
                child1 = new_node(b_x, b_y, (b_x - 1), (b_y + 0), 0, (m.get_level() + 1), m.get_mat(), m)
                child1.set_cost(cal_man_dist(child1.get_mat(), final))  # cost my manhattan distance function
                if not check_repeat(child1):
                    pq.put(child1)
            if is_safe(b_x + 1, b_y + 0):  # down
                child2 = new_node(b_x, b_y, (b_x + 1), (b_y + 0), 0, (m.get_level() + 1), m.get_mat(), m)
                child2.set_cost(cal_man_dist(child2.get_mat(), final))  # cost my manhattan distance function
                if not check_repeat(child2):
                    pq.put(child2)
            if is_safe(b_x + 0, b_y - 1):  # left
                child3 = new_node(b_x, b_y, (b_x + 0), (b_y - 1), 0, (m.get_level() + 1), m.get_mat(), m)
                child3.set_cost(cal_man_dist(child3.get_mat(), final))  # cost my manhattan distance function
                if not check_repeat(child3):
                    pq.put(child3)
            if is_safe(b_x + 0, b_y + 1):  # right
                child4 = new_node(b_x, b_y, (b_x + 0), (b_y + 1), 0, (m.get_level() + 1), m.get_mat(), m)
                child4.set_cost(cal_man_dist(child4.get_mat(), final))  # cost my manhattan distance function
                if not check_repeat(child4):
                    pq.put(child4)


# ----------------------------
# main function to run program
# ----------------------------

def main():
    _final = [[0, 1, 2],
              [3, 4, 5],
              [6, 7, 8]]
    print("Algorithms used to solve 8 Puzzle Problem: \n"
          "(Code: dfs)Depth-First Search (Takes a lot of time)\n"
          "(Code: bfs)Breadth-First Search (Takes a lot of time)\n"
          "(Code: mth)A* with Misplaced Tile Heuristic (Efficient)\n"
          "(Code: mdh)A* with Manhattan Distance Heuristic (More Efficient)\n")
    print("Given final state is: ")
    print_matrix(_final)
    print("Input arguments in this format: <algorithm-code> [array-of-initial-state separated by comma]")
    print("For Example: mth 8, 7, 5, 4, 1, 2, 3, 0, 6")
    arg = input("\nEnter: ").split()            # split by white spaces
    for _ in range(0, len(arg)):                # delete all comma
        arg[_] = arg[_].replace(',', '')
    if len(arg) != 10:                          # if discrete items in not 10 then input is wrong
        print("please provide correct arguments")
    else:
        if isinstance(arg[0], str):
            func = arg[0]                       # first element of list is the function code
            init = []
            for _ in range(1, 10):              # convert the rest elements into integer list
                init.append(int(arg[_]))
            _initial = get_2d(init)             # get the 2D matrix from the list
            _x, _y = get_zero_pos(_initial)     # get the 0 tile coordinate of the provided matrix
            if func == "dfs":                   # Depth-First Search
                print_result(solve_dfs(_initial, _x, _y, _final))
            if func == "bfs":                   # Breadth-First Search
                print_result(solve_bfs(_initial, _x, _y, _final))
            if func == "mth":                   # A* with Misplaced Tile Heuristic
                print_result(solve_a_star(_initial, _x, _y, _final, 'o'))
            if func == "mdh":                   # )A* with Manhattan Distance Heuristic
                print_result(solve_a_star(_initial, _x, _y, _final, 'm'))
        else:
            print("please provide correct arguments")


if __name__ == "__main__":
    main()
