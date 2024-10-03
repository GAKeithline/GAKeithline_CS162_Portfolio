# Author: -Redacted-
# GitHub username: GAKeithline
# Date: 12/06/2023
# Description: Program introduces a class, ChessVar, that allows users to play a modified version of chess that features
#              no specialty movements (castling, en passant, etc.) and no 'check' or 'checkmate.' Victory is declared by
#              capturing all opposing pieces of a single type: two Knights, two Bishops, two Rooks, one King, one Queen
#              or eight Pawns. All other standard chess rules apply. Program also features support classes for ChessVar:
#              ChessBoard and GamePiece. GamePiece has a separate subclass for each standard chess piece.


# noinspection PyTypeChecker
class ChessBoard:
    """
    represents a chess board with white and black sides fully populated in starting position.
    Board is comprised of a list of lists with each item in the list either being 'None' or a unique GamePiece item
    Contains methods for checking movement paths between two points along vertical, horizontal, and diagonal axis.
    Board also has a dictionary with letters A-H as keys assigned ascending numeric values starting at 1 for use
    in coordinate crafting.
    """
    def __init__(self):
        self._board = []
        self._letters = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8}
        # this dictionary is for assigning numerics to letters. 'A5' to 'C5' translates to (1, 5) to (3, 5)

        for num in range(8):
            self._board.append([num+1])  # this sets the '0' element of every row to the number of that row for organization’s sake
        for list in self._board:
            for fill in range(8):
                list.append(None)       # Populate all the spaces on the 'board' with none.

        self._board[0][1] = Rook('White', 'A1')  # populate the white pieces
        self._board[0][2] = Knight('White', 'B1')
        self._board[0][3] = Bishop('White', 'C1')
        self._board[0][4] = Queen('White', 'D1')
        self._board[0][5] = King('White', 'E1')
        self._board[0][6] = Bishop('White', 'F1')
        self._board[0][7] = Knight('White', 'G1')
        self._board[0][8] = Rook('White', 'H1')

        self._board[7][1] = Rook('Black', 'A8')  # populate the black pieces
        self._board[7][2] = Knight('Black', 'B8')
        self._board[7][3] = Bishop('Black', 'C8')
        self._board[7][4] = Queen('Black', 'D8')
        self._board[7][5] = King('Black', 'E8')
        self._board[7][6] = Bishop('Black', 'F8')
        self._board[7][7] = Knight('Black', 'G8')
        self._board[7][8] = Rook('Black', 'H8')

        self._board[1][1] = Pawn('White', 'A2')  # populate the pawns
        self._board[1][2] = Pawn('White', 'B2')
        self._board[1][3] = Pawn('White', 'C2')
        self._board[1][4] = Pawn('White', 'D2')
        self._board[1][5] = Pawn('White', 'E2')
        self._board[1][6] = Pawn('White', 'F2')
        self._board[1][7] = Pawn('White', 'G2')
        self._board[1][8] = Pawn('White', 'H2')

        self._board[6][1] = Pawn('Black', 'A7')
        self._board[6][2] = Pawn('Black', 'B7')
        self._board[6][3] = Pawn('Black', 'C7')
        self._board[6][4] = Pawn('Black', 'D7')
        self._board[6][5] = Pawn('Black', 'E7')
        self._board[6][6] = Pawn('Black', 'F7')
        self._board[6][7] = Pawn('Black', 'G7')
        self._board[6][8] = Pawn('Black', 'H7')

        self._board.insert(0, [' ', ' A ', ' B ', ' C ', ' D ', ' E ', ' F ', ' G ', ' H '])  # add column markers for ease
        self._board.append([' ', ' A ', ' B ', ' C ', ' D ', ' E ', ' F ', ' G ', ' H '])

    def get_board(self):
        """returns the game board in its natural Python List format"""
        return self._board

    def get_position(self, location):
        letter = self._letters[location[0].upper()]
        return self._board[int(location[1])][letter]

    def display_board(self):
        """
        prints out the board with row 1/white pieces at the bottom and row 8/black pieces at the top.
        'spaces' on the board are separated by pipes and newlines
        """
        for row in range(10)[::-1]:  # reverse print so we don't have to translate white pieces at 'A1' to 'A8'
            print('\n')
            for space in self._board[row]:
                if space is None:
                    print(str(space) + ' | ', end=" ")
                if space is not None:
                    if space == GamePiece:
                        print(space.get_shorthand() + '  | ', end=" ")  # a nice little naming scheme to keep the board neat
                    else:
                        print(str(space) + '  | ', end=" ")
        print('\n')

    def get_letters(self):
        """
        returns the special letter-> number conversion dictionary for coordinate building
        """
        return self._letters

    def check_rook_path(self, start_loc, end_loc, start_letter=None, end_letter=None, start_number=None, end_number=None):
        """
        checks for obstructions along an x/y-axis between a starting and ending point on the board using recursion
        """
        if start_letter is None:  # base case for first square check
            start_letter = self._letters[start_loc[0].upper()]  # useful block that converts the letter portion of a board coordinate into a numeric
            end_letter = self._letters[end_loc[0].upper()]  # by defaulting everything to upper() we can take either 'A5' or 'a5' and have the same result
            start_number = int(start_loc[1])
            end_number = int(end_loc[1])
        if end_letter != start_letter and start_number != end_number:  # Rooks can only move X or Y. One of the coordinates must be the same
            return False
        if start_letter == end_letter and start_number == end_number:  # I'm not sure why this needs to be here. I thought my code had outgrown this branch
            return True                                                 # but it seems to still be necessary for adjacent space movements

        if start_number < end_number:  # re: moving 'up' along a letter column
            if start_number + 1 == end_number:  # using an 'up to but not including' approach, so the recursion will terminate one space before the landing zone
                return True
            if self._board[start_number + 1][start_letter] is not None:  # check next space
                return False
            else:
                start_number += 1  # move up one
                return self.check_rook_path(start_loc, end_loc, start_letter, end_letter, start_number, end_number)

        if start_number > end_number:  # re: moving 'down' along a letter column
            if start_number - 1 == end_number:
                return True
            if self._board[start_number - 1][start_letter] is not None:  # check next space
                return False
            else:
                start_number -= 1  # move down one
                return self.check_rook_path(start_loc, end_loc, start_letter, end_letter, start_number, end_number)

        if start_letter < end_letter:  # re: moving 'right' along a row
            if start_letter + 1 == end_letter:
                return True
            if self._board[start_number][start_letter + 1] is not None:  # check next space
                return False
            else:
                start_letter += 1  # move right one
                return self.check_rook_path(start_loc, end_loc, start_letter, end_letter, start_number, end_number)

        if start_letter > end_letter:  # re: moving 'left' along a row
            if start_letter - 1 == end_letter:
                return True
            if self._board[start_number][start_letter - 1] is not None:  # check next space
                return False
            else:
                start_letter -= 1  # move left one
                return self.check_rook_path(start_loc, end_loc, start_letter, end_letter, start_number, end_number)

    def check_bishop_path(self, start_loc, end_loc, start_letter = None, end_letter = None, start_number = None, end_number = None):
        """
        Checks for obstructions along a diagonal axis between a starting and ending point on the board using recursion
        """
        if start_letter is None:  # base case for first square check
            start_letter = self._letters[start_loc[0].upper()]
            end_letter = self._letters[end_loc[0].upper()]
            start_number = int(start_loc[1])
            end_number = int(end_loc[1])
        if abs(start_letter - end_letter) != abs(start_number - end_number):  # this was a fun bit of math, I actually stumbled on the formula while reviewing chess rules (math formula, not code).
            return False
        if start_letter == end_letter and start_number == end_number:
            return True
        if start_letter < end_letter and start_number < end_number:  # re: up and to the right
            if start_letter + 1 == end_letter and start_number + 1 == end_number:  # using an 'up to but not including' approach, so the recursion will terminate one space before the landing zone
                return True
            if self._board[start_number+1][start_letter+1] is not None:  # check next space
                return False
            else:
                start_letter += 1  # move right one
                start_number += 1  # move up one
                return self.check_bishop_path(start_loc, end_loc, start_letter, end_letter, start_number, end_number)

        if start_letter < end_letter and start_number > end_number:  # re: down and to the right
            if start_letter + 1 == end_letter and start_number - 1 == end_number:
                return True
            if self._board[start_number-1][start_letter+1] is not None:
                return False
            else:
                start_letter += 1  # move right one
                start_number -= 1  # move down one
                return self.check_bishop_path(start_loc, end_loc, start_letter, end_letter, start_number, end_number)

        if start_letter > end_letter and start_number > end_number:  # re: down and to the left
            if start_letter - 1 == end_letter and start_number - 1 == end_number:
                return True
            if self._board[start_number-1][start_letter-1] is not None:
                return False
            else:
                start_letter -= 1  # move left one
                start_number -= 1  # move down one
                return self.check_bishop_path(start_loc, end_loc, start_letter, end_letter, start_number, end_number)

        if start_letter > end_letter and start_number < end_number:  # re: up and to the left
            if start_letter - 1 == end_letter and start_number + 1 == end_number:
                return True
            if self._board[start_number+1][start_letter-1] is not None:
                return False
            else:
                start_letter -= 1  # move left one
                start_number += 1  # move up one
                return self.check_bishop_path(start_loc, end_loc, start_letter, end_letter, start_number, end_number)


class GamePiece:
    """
    creates a GamePiece item with name, team, and location. Includes get_() and set_() methods for name, team, and
    location. Designed to be inheritable for use in a small range of virtual boardgames
    Also features a convenient dictionary for converting letters to numerics. Dictionary is tailored to chess
    """

    def __init__(self):
        self._name = None
        self._team = None
        self._location = None
        self._letters = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8}  # this dictionary is a lifesaver

    def __str__(self):
        """
        returns the first letter of the piece color and the first two letters of the piece type as a string.
        Example: 'White Rook' = 'WRo', 'Black Knight' = 'BKn', etc.
        """
        return self._team[0] + self._name[0:2]

    def get_name(self):
        """returns the value of self._name"""
        return self._name

    def get_team(self):
        """returns the value of self._team"""
        return self._team

    def get_shorthand(self):
        """returns the shorthand used in the __str__ method"""
        return self._team[0] + self._name[0:2]

    def get_location(self):
        """returns the value of self._location"""
        return self._location

    def set_location(self, new_loc):
        """allows user to change the value of self._location"""
        self._location = new_loc.upper()

    def get_letters(self):
        """returns the letter dictionary used for numeric conversion"""
        return self._letters


class King(GamePiece):
    """
    Represents a GamePiece that is the King in a game of Chess. Inherits methods and members from GamePiece class.
    Initializes members to determine which team (white or black) the King is playing for and where it will start on
    the board. Introduces additional method, move(), which uses logical computing to determine if a proposed movement is
    legal or not. Designed specifically for use with the ChessVar class and its methods
    """

    def __init__(self, color, location):
        super().__init__()  # recovers the dictionary
        self._name = 'King'
        self._team = color
        self._location = location

    def check_move(self, start_loc, end_loc):
        """
        outlines the movement limitations of the King-piece (one square in any direction) and returns False if the
        proposed new location (end_loc) is illegal.
        """
        start_letter = self._letters[start_loc[0].upper()]  # this block (or a variant) is present in most classes and methods going forward
        end_letter = self._letters[end_loc[0].upper()]      # This makes it so that all letter coordinates are turned into a callable numeric
        start_number = int(start_loc[1])
        end_number = int(end_loc[1])
        if self._location != start_loc.upper():
            return False
        if end_letter > start_letter + 1 or end_letter < start_letter - 1:
            return False
        if end_number > start_number + 1 or end_number < start_number - 1:
            return False
        else:
            return True


class Queen(GamePiece):
    """
    Represents a GamePiece that is the Queen in a game of Chess. Inherits methods and members from GamePiece class.
    Initializes members to determine which team (white or black) the Queen is playing for and where it will start on
    the board. Introduces additional method, move(), which uses logical computing to determine if a proposed movement is
    legal or not. Designed specifically for use with the ChessVar class and its methods
    """

    def __init__(self, color, location):
        super().__init__()
        self._name = 'Queen'
        self._team = color
        self._location = location

    def check_move(self, start_loc, end_loc):
        """
        outlines the movement limitations of the Queen-piece (unlimited squares in any direction, unobstructed)
        and returns False if the proposed new location (end_loc) is illegal.
        """
        start_letter = self._letters[start_loc[0].upper()]
        end_letter = self._letters[end_loc[0].upper()]
        start_number = int(start_loc[1])
        end_number = int(end_loc[1])
        if self._location != start_loc.upper():
            return False
        if abs(start_letter - end_letter) == abs(start_number - end_number):  # the queen is just a bishop/rook hybrid so the same rules from the check_?_path() method will suffice
            return True
        if end_letter == start_letter or end_number == start_number:
            return True
        else:
            return False


class Rook(GamePiece):
    """
    Represents a GamePiece that is a Rook in a game of Chess. Inherits methods and members from GamePiece class.
    Initializes members to determine which team (white or black) the Rook is playing for and where it will start on
    the board. Introduces additional method, move(), which uses logical computing to determine if a proposed movement is
    legal or not. Designed specifically for use with the ChessVar class and its methods
    """

    def __init__(self, color, location):
        super().__init__()
        self._name = 'Rook'
        self._team = color
        self._location = location

    def check_move(self, start_loc, end_loc):
        """
        outlines the movement limitations of the Rook-piece (unlimited squares in any direction along an x or y-axis,
        unobstructed) and returns False if the proposed new location (new_loc) is illegal.
        """
        start_letter = self._letters[start_loc[0].upper()]
        end_letter = self._letters[end_loc[0].upper()]
        start_number = int(start_loc[1])
        end_number = int(end_loc[1])
        if self._location != start_loc.upper():
            return False
        if end_letter == start_letter or end_number == start_number:  # same as 'rook section' on Queen
            return True
        else:
            return False


class Knight(GamePiece):
    """
    Represents a GamePiece that is a Knight in a game of Chess. Inherits methods and members from GamePiece class.
    Initializes members to determine which team (white or black) the Knight is playing for and where it will start on
    the board. Introduces additional method, move(), which uses logical computing to determine if a proposed movement is
    legal or not. Designed specifically for use with the ChessVar class and its methods
    """

    def __init__(self, color, location):
        super().__init__()
        self._name = 'Knight'
        self._team = color
        self._location = location

    def check_move(self, start_loc, end_loc):
        """
        outlines the movement limitations of the Knight-piece (two spaces + one space to 90 degrees or one
        space + two spaces to 90 degrees any direction) and returns False if the proposed new location (new_loc) is
        illegal. Knights are the only piece in chess that may disregard path obstructions.
        """
        start_letter = self._letters[start_loc[0].upper()]
        end_letter = self._letters[end_loc[0].upper()]
        start_number = int(start_loc[1])
        end_number = int(end_loc[1])
        if self._location != start_loc.upper():
            return False
        if abs(start_letter - end_letter) == 2 and abs(start_number - end_number) == 1:  # knights move 2 vert and 1 horizontal or 1 vert and two horizontal in any direction. abs() saves the day again
            return True
        if abs(start_letter - end_letter) == 1 and abs(start_number - end_number) == 2:
            return True
        else:
            return False


class Bishop(GamePiece):
    """
    Represents a GamePiece that is a Bishop in a game of Chess. Inherits methods and members from GamePiece class.
    Initializes members to determine which team (white or black) the Bishop is playing for and where it will start on
    the board. Introduces additional method, move(), which uses logical computing to determine if a proposed movement is
    legal or not. Designed specifically for use with the ChessVar class and its methods
    """

    def __init__(self, color, location):
        super().__init__()
        self._name = 'Bishop'
        self._team = color
        self._location = location


    def check_move(self, start_loc, end_loc):
        """
        outlines the movement limitations of the Bishop-piece (unlimited squares along a diagonal axis, unobstructed)
        and returns False if the proposed new location (new_loc) is illegal.
        """
        start_letter = self._letters[start_loc[0].upper()]
        end_letter = self._letters[end_loc[0].upper()]
        start_number = int(start_loc[1])
        end_number = int(end_loc[1])
        if self._location != start_loc.upper():
            return False
        if abs(start_letter - end_letter) == abs(start_number - end_number):  # same as 'bishop section' on Queen
            return True
        else:
            return False


class Pawn(GamePiece):
    """
    Represents a GamePiece that is a Pawn in a game of Chess. Inherits methods and members from GamePiece class.
    Initializes members to determine which team (white or black) the Pawn is playing for and where it will start on
    the board. Pawn introduces an additional member, first_move, that is initialized to True, reflecting that the piece
    has not made any moves to start the game. Introduces additional method, move(), which uses logical computing to
    determine if a proposed movement is legal or not. Designed specifically for use with the ChessVar class and its
    methods
    """

    def __init__(self, color, location):
        super().__init__()
        self._name = 'Pawn'
        self._team = color
        self._location = location
        self._first_move = True  # used by ChessVar make_move() method to determine pawn movement legality

    def get_move(self):
        """
        Called by ChessVar when a pawn makes a move.
        Used to determine legality of Pawn multi-square moves
        """
        return self._first_move

    def check_move(self, start_loc, end_loc, take):
        """
        outlines the movement limitations of the Pawn-piece (two squares on first turn, one square on subsequent turns,
        may only 'take' diagonally. All moves must be forward from starting side) and returns False if the proposed new
        location (new_loc) is illegal.
        """
        start_letter = self._letters[start_loc[0].upper()]
        end_letter = self._letters[end_loc[0].upper()]
        start_number = int(start_loc[1])
        end_number = int(end_loc[1])
        if self._location != start_loc.upper():
            return False
        if self._first_move is True and self._team == 'White':
            if end_number > 4 or end_number < start_number:
                return False
        if self._first_move is True and self._team == 'Black':
            if end_number < 5 or end_number > start_number:
                return False
        if self._first_move is False and self._team == 'White':
            if end_number > start_number + 1 or end_number < start_number:
                return False
        if self._first_move is False and self._team == 'Black':
            if end_number < start_number - 1 or end_number > start_number:
                return False
        if take is True:
            if end_letter > start_letter + 1 or end_letter < start_letter - 1 or end_letter == start_letter:
                return False
            else:
                if self._first_move is True:
                    self._first_move = False
                return True
        if take is False:
            if end_letter != start_letter:
                return False
            else:
                if self._first_move is True:
                    self._first_move = False
                return True


class ChessVar:
    """
    represents an interactive chess game with the same primary rules as standard chess, but without specialized
    movements (castling, en passant, etc.) and modified victory conditions (game ends with one team's capture of all
    opponent pieces of the same type). The 'game board' is represented by a 2D dictionary array wherein the keys
    represent a space on the board and the values are either 'None' (indicating an open space) or a GamePiece item.
    """

    def __init__(self):
        self._game_state = 'UNFINISHED'
        self._black_taken = []  # these will be the repositories for taken pieces. Eventually we'll use these lists to determine victory conditions
        self._white_taken = []
        self._which_turn = 'White'
        self._board = ChessBoard()
        self._letters = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8}

    def get_game_state(self):
        """returns the value of self._game_state"""
        return self._game_state

    def get_turn(self):
        """returns value of self._which_turn"""
        return self._which_turn

    def get_white_captures(self):
        """returns the list of pieces that white has captured"""
        taken = []
        for piece in self._white_taken:
            taken.append(piece.get_shorthand())  # save the massive item handle
        return taken

    def get_black_captures(self):
        """returns the list of pieces that white has captured"""
        taken = []
        for piece in self._black_taken:
            taken.append(piece.get_shorthand())
        return taken

    def display_board(self):
        """
        displays the gameboard by calling the ChessBoard display_board() method on the self._board data member
        """
        return self._board.display_board()

    def make_move(self, start_loc, end_loc):
        """
        checks start_loc on game board for a piece and uses piece method get_team() to verify against self._which_turn
        that the piece may legally move this turn. The start and end loc's are fed to piece method check_move() to
        determine if the move is legal. make_mov then checks board for obstructions using ChessBoard methods
        before updating the game board to reflect the move and exchange the turn count while calling piece method
        set_location() to reflect the move in the piece itself.
        Illegal moves return 'False' and legal moves return 'True'
        """
        if self._game_state != 'UNFINISHED':  # If the game is complete, simply return False
            return False

        start_letter = self._letters[start_loc[0].upper()]
        end_letter = self._letters[end_loc[0].upper()]
        start_number = int(start_loc[1])
        end_number = int(end_loc[1])
        start = self._board.get_board()[start_number][start_letter]  # the represents the actual value (GamePiece or None) at the starting position of the board
        end = self._board.get_board()[end_number][end_letter]  # the represents the actual value (GamePiece or None) at the end position of the board
        if start is None or start.get_team() != self._which_turn:
            return False  # accounts for an empty starting space or for the wrong color piece
        if end is None:  # moving to an empty space

            if start.get_name() == 'King' or start.get_name() == 'Knight':
                if start.check_move(start_loc, end_loc) is True:  # these pieces don't have special path checks
                    self._board.get_board()[end_number][end_letter] = start  # move piece to end_loc
                    self._board.get_board()[start_number][start_letter] = None  # leave an empty space behind at start_loc
                    self._board.get_board()[end_number][end_letter].set_location(end_loc.upper())  # update the GamePiece's own location data member
                    if self._which_turn == 'White':
                        self._which_turn = 'Black'  # adjust for next turn
                        return True
                    elif self._which_turn == 'Black':
                        self._which_turn = 'White'
                        return True
                return False

            if start.get_name() == 'Pawn':
                if start.check_move(start_loc, end_loc, False) is True:  # False because not taking
                    self._board.get_board()[end_number][end_letter] = start
                    self._board.get_board()[start_number][start_letter] = None
                    self._board.get_board()[end_number][end_letter].set_location(end_loc.upper())
                    if self._which_turn == 'White':
                        self._which_turn = 'Black'
                        return True
                    elif self._which_turn == 'Black':
                        self._which_turn = 'White'
                        return True
                return False

            if start.get_name() == 'Queen':
                if start.check_move(start_loc, end_loc) is True:
                    if self._board.check_bishop_path(start_loc, end_loc) is True or self._board.check_rook_path(start_loc, end_loc) is True:  # call the GameBoard path check methods to ensure a clear path
                        self._board.get_board()[end_number][end_letter] = start
                        self._board.get_board()[start_number][start_letter] = None
                        self._board.get_board()[end_number][end_letter].set_location(end_loc.upper())
                        if self._which_turn == 'White':
                            self._which_turn = 'Black'
                            return True
                        elif self._which_turn == 'Black':
                            self._which_turn = 'White'
                            return True
                return False

            if start.get_name() == 'Rook':
                if start.check_move(start_loc, end_loc) is True:
                    if self._board.check_rook_path(start_loc, end_loc) is True:
                        self._board.get_board()[end_number][end_letter] = start
                        self._board.get_board()[start_number][start_letter] = None
                        self._board.get_board()[end_number][end_letter].set_location(end_loc.upper())
                        if self._which_turn == 'White':
                            self._which_turn = 'Black'
                            return True
                        elif self._which_turn == 'Black':
                            self._which_turn = 'White'
                            return True
                return False

            if start.get_name() == 'Bishop':
                if start.check_move(start_loc, end_loc) is True:
                    if self._board.check_bishop_path(start_loc, end_loc) is True:
                        self._board.get_board()[end_number][end_letter] = start
                        self._board.get_board()[start_number][start_letter] = None
                        self._board.get_board()[end_number][end_letter].set_location(end_loc.upper())
                        if self._which_turn == 'White':
                            self._which_turn = 'Black'
                            return True
                        elif self._which_turn == 'Black':
                            self._which_turn = 'White'
                            return True
                return False

        if end is not None:  # uses the same general structure as the 'if end is None' branch with some minor changes for taking pieces.
            if end.get_team() == self._which_turn:
                return False  # we can't land on a space with our own pieces

            if start.get_name() == 'King' or start.get_name() == 'Knight':
                if start.check_move(start_loc, end_loc) is True:
                    self.take_piece(end_loc)  # call the take_piece() method to capture and evaluate for victory conditions
                    self._board.get_board()[end_number][end_letter] = start
                    self._board.get_board()[start_number][start_letter] = None
                    self._board.get_board()[end_number][end_letter].set_location(end_loc.upper())
                    if self._which_turn == 'White':
                        self._which_turn = 'Black'
                        return True
                    elif self._which_turn == 'Black':
                        self._which_turn = 'White'
                        return True
                return False

            if start.get_name() == 'Pawn':
                if start.check_move(start_loc, end_loc, True) is True:  # True because we are taking
                    self.take_piece(end_loc)
                    self._board.get_board()[end_number][end_letter] = start
                    self._board.get_board()[start_number][start_letter] = None
                    self._board.get_board()[end_number][end_letter].set_location(end_loc.upper())
                    if self._which_turn == 'White':
                        self._which_turn = 'Black'
                        return True
                    elif self._which_turn == 'Black':
                        self._which_turn = 'White'
                        return True
                return False

            if start.get_name() == 'Queen':
                if start.check_move(start_loc, end_loc) is True:
                    if self._board.check_bishop_path(start_loc, end_loc) is True or self._board.check_rook_path(start_loc, end_loc) is True:
                        self.take_piece(end_loc)
                        self._board.get_board()[end_number][end_letter] = start
                        self._board.get_board()[start_number][start_letter] = None
                        self._board.get_board()[end_number][end_letter].set_location(end_loc.upper())
                        if self._which_turn == 'White':
                            self._which_turn = 'Black'
                            return True
                        elif self._which_turn == 'Black':
                            self._which_turn = 'White'
                            return True
                return False

            if start.get_name() == 'Rook':
                if start.check_move(start_loc, end_loc) is True:
                    if self._board.check_rook_path(start_loc, end_loc) is True:
                        self.take_piece(end_loc)
                        self._board.get_board()[end_number][end_letter] = start
                        self._board.get_board()[start_number][start_letter] = None
                        self._board.get_board()[end_number][end_letter].set_location(end_loc.upper())
                        if self._which_turn == 'White':
                            self._which_turn = 'Black'
                            return True
                        elif self._which_turn == 'Black':
                            self._which_turn = 'White'
                            return True
                return False

            if start.get_name() == 'Bishop':
                if start.check_move(start_loc, end_loc) is True:
                    if self._board.check_bishop_path(start_loc, end_loc) is True:
                        self.take_piece(end_loc)
                        self._board.get_board()[end_number][end_letter] = start
                        self._board.get_board()[start_number][start_letter] = None
                        self._board.get_board()[end_number][end_letter].set_location(end_loc.upper())
                        if self._which_turn == 'White':
                            self._which_turn = 'Black'
                            return True
                        elif self._which_turn == 'Black':
                            self._which_turn = 'White'
                            return True
                return False

    def take_piece(self, end_loc):
        """
        adds value found at location (end_loc) of self._board to the appropriate team 'taken' repository and combs
        said repositories at the time of deposit to determine if the game victory conditions have been met.
        """
        end_letter = self._letters[end_loc[0].upper()]  # take_piece only deals with the end location of a move
        end_number = int(end_loc[1])
        end = self._board.get_board()[end_number][end_letter]

        if self._which_turn == 'White':
            self._white_taken.append(end)  # pop the pieces in the taken repository
            pawns = []  # sub-lists used for some logic operations
            doubles = []
            knights = []
            rooks = []
            bishops = []
            for piece in self._white_taken:
                if piece.get_name() == 'Pawn':
                    pawns.append(piece)
                    if len(pawns) == 8:  # capturing all 8 pawns wins the game.
                        self._game_state = 'WHITE_WON'  # ends game
                if piece.get_name() == 'Rook':
                    rooks.append(piece)
                if piece.get_name() == 'Bishop':
                    bishops.append(piece)
                if piece.get_name() == 'Knight':
                    knights.append(piece)
                if len(bishops) == 2 or len(rooks) == 2 or len(knights) == 2: # capture two of the paired pieces wins the game
                    self._game_state = 'WHITE_WON'
                elif piece.get_name() == 'King' or piece.get_name() == 'Queen':
                    self._game_state = 'WHITE_WON'

        if self._which_turn == 'Black':  # same as previous block, but for the black taken pieces
            self._black_taken.append(end)
            pawns = []
            knights = []
            rooks = []
            bishops = []
            for piece in self._black_taken:
                if piece.get_name() == 'Pawn':
                    pawns.append(piece)
                    if len(pawns) == 8:
                        self._game_state = 'BLACK_WON'
                if piece.get_name() == 'Rook':
                    rooks.append(piece)
                if piece.get_name() == 'Bishop':
                    bishops.append(piece)
                if piece.get_name() == 'Knight':
                    knights.append(piece)
                if len(bishops) == 2 or len(rooks) == 2 or len(knights) == 2: # capture two of the paired pieces wins the game
                    self._game_state = 'BLACK_WON'
                elif piece.get_name() == 'King' or piece.get_name() == 'Queen':
                    self._game_state = 'BLACK_WON'

    def reset_game(self):
        """resets all data members to default status so the game may be played again."""
        self._board = None
        self._game_state = 'UNFINISHED'
        self._black_taken = []
        self._white_taken = []
        self._which_turn = 'White'
        self._board = ChessBoard()


def main():
    game = ChessVar()
    print(game.make_move('a2', 'a4'))
    print(game.make_move('h7', 'h4'))
    print(game.make_move('e7', 'e6'))
    print(game.make_move('e2', 'd3'))
    print(game.make_move('a1', 'a5'))
    print(game.make_move('a1', 'a3'))
    print(game.make_move('f8', 'h6'))
    print(game.make_move('f8', 'c5'))
    print(game.make_move('a3', 'b4'))
    print(game.make_move('f1', 'h3'))
    print(game.make_move('a3', 'h3'))
    print(game.make_move('d8', 'h4'))
    """
    print(game.make_move('g7', 'f7'))
    print('the next move will be obstructed by a piece of the same color (black)')
    print(game.make_move('a8', 'b8'))
    print(game.make_move('e7', 'e5'))
    print('the next move will be out of turn')
    print(game.make_move('c7', 'c5'))
    print(game.make_move('f2', 'f4'))
    print(game.make_move('e8', 'e6'))
    print('the next move will be obstructed by a piece of the same color (white)')
    print(game.make_move('c1', 'd2'))
    print(game.make_move('e1', 'g3'))
    print(game.make_move('a7', 'a6'))
    print(game.make_move('g3', 'h3'))
    print('the next move will be illegal (pawn backwards)')
    print(game.make_move('e5', 'e7'))
    print(game.make_move('e6', 'h3'))
    print(game.get_game_state())
    print(game.make_move('b1', 'c3'))
    """
    game.display_board()
    print(game.get_game_state())
    print(game.get_white_captures())
    print(game.get_black_captures())

if __name__ == '__main__':
    main()
