# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# file:    board.py
# date:    2016-10-30
# author:  koromodako (16201434)
# purpose:
#   This file contains the implementation of Board class which represent a
#   Yavalath board with associated game state data.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#==============================================================================
#  GLOBALS
#==============================================================================
OFFSET = [4,3,2,1,0,0,0,0,0]
#==============================================================================
#  FUNCTIONS/CLASSES
#==============================================================================
class Board(object):
    """Board"""
    # players IDs
    PR_1=1
    PR_2=2
    # board size
    SIDE=9
    # end game states
    EG_DRAW=0
    EG_WIN=1
    EG_LOSE=2
    EG_NEXT=3
    # impossible moves
    IMPOSSIBLE = [
        (0,0), (0,1), (0,2), (0,3), (1,0),
        (1,1), (1,2), (2,0), (2,1), (3,0),
        (5,8), (6,7), (6,8), (7,6), (7,8),
        (7,8), (8,5), (8,6), (8,7), (8,8)
    ]

    def __init__(self):
        """Constructs the Board object"""
        super(Board, self).__init__()
        self.reset()

    def reset(self):
        """Resets board object"""
        self.board = [
            [-1,-1,-1,-1, 0, 0, 0, 0, 0],
            [-1,-1,-1, 0, 0, 0, 0, 0, 0],
            [-1,-1, 0, 0, 0, 0, 0, 0, 0],
            [-1, 0, 0, 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0, 0, 0, 0,-1],
            [ 0, 0, 0, 0, 0, 0, 0,-1,-1],
            [ 0, 0, 0, 0, 0, 0,-1,-1,-1],
            [ 0, 0, 0, 0, 0,-1,-1,-1,-1]
        ]
        self.next_player = self.PR_1
        self.fst_mv_taken = False
        self.move_count = 0

    def print_line(self, ridx, indent, detailed=False):
        """Prints a line of the board
           arguments:
               ridx   -- integer value of the index of the row (zero-based)
               indent -- integer value of the indent to be printed before the
                         row
        """
        if detailed:
            print('%c: ' % chr(ridx+65), end='')
        print(' '*indent, end='')
        for i in range(0,self.SIDE):
            v=self.board[ridx][i]
            if v!=-1:
                c=' '
                if v==self.PR_1:
                    c='X'
                elif v==self.PR_2:
                    c='O'
                print('| {} '.format(c), end='')
        if detailed and ridx < 4:
            print('| %d' % (ridx+6))
        else:
            print('|')

    def print_up(self, count, indent, detailed=False):
        s = ''
        if detailed:
            s += ' ' * 3
        s += ' ' * indent
        s += ' / \\' * count
        print(s)

    def print_down(self, count, indent, detailed=False):
        s = ''
        if detailed:
            s += ' ' * 3
        s += ' ' * indent
        s += ' \\ /' * count
        print(s)

    def print(self, detailed=False):
        """Prints the board"""
        if detailed:
            print('               1   2   3   4   5')
        self.print_up(  5, 8, detailed)
        self.print_line(0, 8, detailed)
        self.print_up(  6, 6, detailed)
        self.print_line(1, 6, detailed)
        self.print_up(  7, 4, detailed)
        self.print_line(2, 4, detailed)
        self.print_up(  8, 2, detailed)
        self.print_line(3, 2, detailed)
        self.print_up(  9, 0, detailed)
        self.print_line(4, 0, detailed)
        self.print_down(9, 0, detailed)
        self.print_line(5, 2, detailed)
        self.print_down(8, 2, detailed)
        self.print_line(6, 4, detailed)
        self.print_down(7, 4, detailed)
        self.print_line(7, 6, detailed)
        self.print_down(6, 6, detailed)
        self.print_line(8, 8, detailed)
        self.print_down(5, 8, detailed)

    def print_pos(self,x,y):
        c = chr(x+65)
        d = y + 1 - OFFSET[x] 
        print('Latest move: %c%d' % (c,d))

    def take_first_move(self):
        """Retrieves and returns coordinates of the first move"""
        for x in range(0, self.SIDE):
            for y in range(0, self.SIDE):
                v = self.board[x][y]
                if v != 0 and v != -1:
                    return (x,y)
        return (None,None)

    def is_playable(self, r, c):
        """Assert the existance and availability of the position
           arguments:
               r -- row to be considered (zero-based)
               c -- number of playable column (one-based)
           returns:
               a tuple of a boolean and two integer values indicating if the
               cell can be played and the real coordinates of the cell in the
               matrix
        """
        valid = False
        y = c
        for k in range(0, self.SIDE):
            v = self.board[r][k]
            if v != -1:
                y -= 1
                if y == 0:
                    if v == 0:
                        y = k
                        valid = True
                    break
        return (valid, r, y)

    def update_next_player(self):
        """Updates next player value swapping from 1-to-2 and 2-to-1"""
        if self.next_player == self.PR_2:
            self.next_player = self.PR_1
        else:
            self.next_player = self.PR_2

    def do(self, x, y):
        """Executes a move and updates board-related variables
           arguments:
               x -- index of the row in the matrix (zero-based)
               y -- index of the column in the matrix (zero-based)
        """
        if self.move_count == 1 and self.board[x][y] != 0:
            self.fst_mv_taken = True
        self.board[x][y] = self.next_player
        self.update_next_player()
        self.move_count += 1

    def undo(self, x, y):
        """Reverts a move and updates board-related variables
           arguments:
               x -- index of the row in the matrix (zero-based)
               y -- index of the column in the matrix (zero-based)
        """
        if self.move_count == 2 and self.fst_mv_taken:
            self.board[x][y] = self.next_player
            self.fst_mv_taken = False
        else:
            self.board[x][y] = 0
        self.update_next_player()
        self.move_count -= 1

    def end_game(self, x, y):
        """Detects if the board is in an end game state
           arguments:
               x -- index of the row in the matrix (zero-based)
               y -- index of the column in the matrix (zero-based)
        """
        # -- initialise variables
        player = self.board[x][y]
        mx_seq = 0
        seq = 1
        k = 1
        # -- check draw
        if self.fst_mv_taken and self.move_count == 62:
            return self.EG_DRAW
        elif not self.fst_mv_taken and self.move_count == 61:
            return self.EG_DRAW
        # -- check for a winner or a loser
        # ---- check line
        while True:
            if y+k >= self.SIDE:
                break
            if self.board[x][y+k] != player:
                break
            seq += 1
            k += 1
        k = 1
        while True:
            if y-k < 0:
                break
            if self.board[x][y-k] != player:
                break
            seq += 1
            k += 1
        mx_seq = max(mx_seq, seq)
        seq = 1
        # ---- check column
        k = 1
        while True:
            if x+k >= self.SIDE:
                break
            if self.board[x+k][y] != player:
                break
            seq += 1
            k += 1
        k = 1
        while True:
            if x-k < 0:
                break
            if self.board[x-k][y] != player:
                break
            seq += 1
            k += 1
        mx_seq = max(mx_seq, seq)
        seq = 1
        # ---- check diagonal
        k = 1
        while True:
            if x+k >= self.SIDE or y-k < 0:
                break
            if self.board[x+k][y-k] != player:
                break
            seq += 1
            k += 1
        k = 1
        while True:
            if x-k < 0 or y+k >= self.SIDE:
                break
            if self.board[x-k][y+k] != player:
                break
            seq += 1
            k += 1
        mx_seq = max(mx_seq, seq)
        # -- determine case
        if mx_seq >= 4:
            return self.EG_WIN
        elif mx_seq == 3:
            return self.EG_LOSE
        return self.EG_NEXT

    def ai_is_playable(self, x, y):
        """Tests if the cell is playable for the AI
           arguments:
               x -- index of the row in the matrix (zero-based)
               y -- index of the column in the matrix (zero-based)
        """
        v = self.board[x][y]
        if v == 0:
            return True
        return (self.move_count == 1 and v != -1 and not self.fst_mv_taken)

    def ai_board_lines(self):
        """Convert the board matrix to a list of strings representing 
           lines, the two diagonals of the hexagonal board
        """
        board_lines = [ '' for i in range(0,3*self.SIDE) ]
        # convert lines and columns
        for x in range(0, self.SIDE):
            for y in range(0, self.SIDE):
                v = self.board[x][y]
                if v != -1:
                    board_lines[x] += str(v)
                    board_lines[self.SIDE+y] += str(v)
        # convert diagonals
        for c in range(4, self.SIDE):
            for r in range(0, self.SIDE):
                y = c - r
                if y >= self.SIDE or y < 0:
                    break
                board_lines[2*self.SIDE+c-4] += str(self.board[r][y])
        for r in range(1,5):
            for c in range(0, self.SIDE):
                x = r + c
                y = self.SIDE-1-c
                if x >= self.SIDE or x < 0 or y >= self.SIDE or y < 0:
                    break
                board_lines[3*self.SIDE-r] += str(self.board[x][y])
        return board_lines

