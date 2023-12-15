
NAME_TO_TABLE = {'t': [[1,1,1],[0,1,0]], 
                 'T': [[1,1,1],[0,1,0],[0,1,0]], 
                 'z': [[1,1,0],[0,1,1]],
                 'c': [[1,1],[1,0],[1,1]],
                 'f': [[1,1],[1,0],[1,1], [1,0]],
                 'L': [[1,0,0],[1,1,1]],
                 'l':[[1,0], [1,1]]}
EMPTY_SPOT = '-'
BLOCKER_SPOT = 'o'

def transpose(M):
    return [[ M[col][row] for col in range(len(M))] for row in range(len(M[0]))]

def rev_row(M):
    return M[::-1]

def rev_column(M):
    return [M[row][::-1] for row in range(len(M)) ]

def help_message():
    print("- 'help' to display commands")
    print("- 'quit' to quit the game" )
    print("- 'a <piece name> <row> <col>' to add a piece to the board at the position ")
    print("\teg: a L 2 2") 
    print("- 'r <piece name>' to remove a piece")
    
class Shape:
    __slots__ = ['__table', '__position'] 
    
    def __init__(self, table, position=None):
        self.__table = table
        self.__position = position        
    
    def get_table(self):
        return self.__table

    def get_position(self):
        return self.__position

    # 3a
    def __repr__(self):
        return str(self.__table) + " " + str(self.__position)

    def __hash__(self):
        return hash(repr(self))      

    def __eq__(self, other):
        if type(self) == type(other):
            return self.__table == other.__table
        else: 
            return False

    #3b
    def fit(self, board, position):
        row, col = position
        shape = self.__table
        for i in range(len(shape)):
            for j in range(len(shape[0])):
                try:
                    if shape[i][j] == 1 and board[i+row][j+col] != EMPTY_SPOT:
                        return False
                except IndexError:
                    return False
        return True

    #3c
    def add(self, board, position, symbol):
        self.__position = position
        self.__update_board(board, symbol)

    def __update_board(self, board, symbol):
        row, col = self.__position
        shape = self.__table
        if self.fit(board, self.__position):
            for i in range(len(shape)):
                for j in range(len(shape[0])):
                    if shape[i][j] == 1:
                        board[i+row][j+col] = symbol
        else:
            return "doesnt fit"

    def remove(self, board):
        row, col = self.__position
        shape = self.__table
        for i in range(len(shape)):
            for j in range(len(shape[0])):
                if shape[i][j] == 1:
                    board[i+row][j+col] = EMPTY_SPOT


class Puzzle:
    __slots__ = ['__board', '__pieces', '__pieces_on_board', '__game_over']
    
    def __init__(self, blockers):
        self.__board = [[EMPTY_SPOT for _ in range(6)] for _ in range(6)]
        for r, c in blockers:
            self.__board[r][c] = BLOCKER_SPOT
        self.__pieces = {value: value for value in NAME_TO_TABLE}
        self.__pieces_on_board = dict()
        self.__game_over = True
               
    def play(self):
        print(self)
        remaining = self.__pieces
        for value in self.__pieces_on_board:
            remaining.pop(value)

        try:
            while len(self.__pieces_on_board) < 7:
                print()
                print("Remaining pieces:", [value for value in remaining])
                response = input("Enter a command or 'help': ")
                response = response.strip()
                if response == "quit":
                    print("Bye!")
                    break
                elif response == "help":
                    help_message()
                elif response[0] == "a" and len(response) == 7:
                    position = (int(response[4]), int(response[6]))
                    if self.add(remaining, response[2],position):
                        print(response[2]+ " added!")
                elif response[0] == "a" and len(response) != 7:
                    print()
                    print("Incomplete Command. Try Again")
                elif response[0] == "r" and len(response) == 3:
                    if self.remove(remaining, response[2]):
                        print(response[2] + " removed.")
                        print()
                        print(self)
                elif response[0] == "r" and len(response) != 3:
                    print()
                    print("Incomplete Command. Try Again")
            
            if len(self.__pieces_on_board) == 7:
                return self.__game_over
        
        except KeyError:
            response = input("Invalid Shape. Do you want to try again? (y/n): ")
            if response.lower().strip() == "n":
                    print("Bye!")
                    return
            elif response.lower().strip() == "y":
                self.play()

    
    def __str__(self):
        s = '    0 1 2 3 4 5\n'
        s +='   ------------\n'
        for index in range(len(self.__board)):
            s += str(index) + " | "
            for elt in self.__board[index]:
                s += elt + " "
            s += "\n"
        return s

    #5
    def add(self, remaining, name, position):
        if name in self.__pieces_on_board:
            print(name + " already on the board. Try Again")
            return False

        piece = Piece(name)

        piece.set_fit_shapes(self.__board, position)
        set = piece.get_fit_shapes()

        if len(piece.get_fit_shapes()) == 0:
            print()
            print("no shapes of the piece fit in the position. Try Again")
            print()
            return False
        
            
        while len(set) > 0:
            fits = piece.get_fit_shape()
            fits.add(self.__board, position, name)
            print()
            print(self)
            confirm = input(name + ": like this? (y/n/q): ")
            if confirm.lower().strip() == "n":
                fits.remove(self.__board)
            elif confirm.lower().strip() == "y":
                piece.add(self.__board, fits, position)
                remaining.pop(name)
                print(self)
                self.__pieces_on_board[name] = [position, fits]
                break
            elif confirm.lower().strip() == "q":
                    break

        return True

    def remove(self, remaining, name):
        if name not in self.__pieces_on_board:
            print(name + " doesnt exist on the board. Try Again")
            return False
        else:
            identity = self.__pieces_on_board[name]
            shape = identity[1]
            piece = Piece(name, shape) 
            piece = Piece(name, shape) 
            piece = Piece(name, shape) 
            self.__pieces_on_board.pop(name)
            remaining[name] = NAME_TO_TABLE[name]
            piece.remove(self.__board)
        return True
            

#4
class Piece:
    __slots__ = ["__name", "__fit_shapes", "__current_shape", "__index"]

    def __init__(self, name, current_shape = None):
        self.__name = name
        self.__current_shape = current_shape
        self.__fit_shapes = []
        self.__index = 0

    def get_name(self):
        return self.__name

    def get_current_shape(self):
        return self.__current_shape

    def set_fit_shapes(self, board, position):
        standard = NAME_TO_TABLE[self.__name]
        rr = rev_row(standard)      # rev row:
        rrt = transpose(rr)         # rev row + transpose
        rc = rev_column(standard)   # rev col:
        rcrr = rev_row(rc)          # rev col + rev row
        rcrrt = transpose (rcrr)    # rev col + rev row + transpose
        t = transpose(standard)     # transpose
        trr = rev_row(t)            # transpose + rev_row
        tables = [standard, rr, rrt, rc, rcrr, rcrrt, t, trr]

        fit_shapes = self.__fit_shapes
        for value in tables:
            if Shape(value, position).fit(board, position):
                fit_shapes.append(Shape(value, position))

    def get_fit_shapes(self):
        return self.__fit_shapes

    #4e
    def get_fit_shape(self):
        if self.__fit_shapes == []:
            return None

        fit_shape = self.__fit_shapes[self.__index]

        if self.__index == len(self.__fit_shapes) - 1:
            self.__index = 0
        elif self.__index < len(self.__fit_shapes):
            self.__index += 1 

        return fit_shape

    #4f
    def add(self, board, shape, position):
        self.__current_shape = shape
        self.__current_shape.add(board, position, self.__name)

    #4g
    def remove(self, board):
        self.__current_shape.remove(board)
        self.__current_shape = None


     
def main(): 
    # blocker_locations = ((0,1), (0,5), (2,0), (5,1), (5,4))
    blocker_locations = ((0,0), (0,1), (3,4), (4,0), (5,5))
    # blocker_locations = ((0,1), (0,3), (4,3), (5,3), (5,5)) 
    
    a_puzzle = Puzzle(blocker_locations)
    if a_puzzle.play():
        print("You Won!")

if __name__ == '__main__':     
    main()