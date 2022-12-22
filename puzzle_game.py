'''
    CS5001 - Fall 2021
    Chanon (Am) Bovornvirakit
    Final Project: Puzzle Slider Game
'''

import turtle
import random
import time
import os
from glob import glob
from datetime import datetime


class Board:
    def __init__(self, puzzle):
        self.screen = self.initialize()
        self.name, self.max_moves = self.prompt_info(self.screen)
        self.puzzle = puzzle
        self.puz_file = self.process_puz_file(self.puzzle)
        self.puz_files = self.get_puzzles()
        self.images_folders = self.get_folders()
        self.image_path = self.get_image_path(self.puz_file)
        self.upper_limit, self.puzzle_size = self.puzzle_numbers()
        self.draw_UI(self.screen)
        self.scores = self.get_leaderboard(puzzle)
        self.draw_leaderboard(self.scores)
        self.board, self.solution = self.draw_puzzle()
        self.current_moves = 0
        self.moves_drawing = self.draw_moves()

    # Boots up the turtle screen and the opening splash image
    def initialize(self):
        window = turtle.Screen()
        window.title("CS5001 Puzzle Slider Game - Am")
        window.setup(1000, 750)
        window.addshape("Resources/splash_screen.gif")
        window.clear()
        splash = turtle.Turtle()
        splash.speed(0)
        splash.shape("Resources/splash_screen.gif")
        time.sleep(5)
        return window

    # Prompts the user for their name and how many moves they want to limit
    def prompt_info(self, window):
        name = window.textinput("Name", "Please enter your name.")
        while name == None or name == "":
            name = window.textinput("Name", "Please enter your name.")
        moves = window.numinput("Moves", "Please enter the allowed number of moves.")
        while moves == None or moves <= 0:
            moves = window.numinput("Moves", "Please enter the allowed number of moves.")
        window.clear()
        return name, moves

    # Returns a list of all .puz files
    def get_puzzles(self):
        puzzles = []
        for file in glob("*.puz"):
            puzzles.append(file)
        return puzzles

    # Returns a list of all folders in the Images folder
    def get_folders(self):
        directories = []
        for directory in os.walk("Images"):
            directories.append(directory)
        images = []
        for folder in directories[0][1]:
            images.append(folder)
        return images

    # Loads the information from the .puz file into a list
    def process_puz_file(self, puzzle):
        puz_file = puzzle + '.puz'
        with open(puz_file, mode='r') as file:
            puz_info = file.readlines()
        return puz_info

    # On the offchance the images aren't stored in "Images/[puzzlename]/..."
    def get_image_path(self, puz_file):
        line = puz_file[3]
        line = line.split(" ")[1]
        directory = ''
        for i in range(0, len(line)):
            if line[i:i+4] == ".gif":
                break
            directory += line[i]
        directory = directory.split("/")
        path = ''
        for i in range(0, len(directory) - 1):
            path += directory[i]
            path += "/"
        return path

    # Gets the size of the puzzle and the number of rows/columns
    def puzzle_numbers(self):
        puz_info = self.puz_file[1].split(" ")
        puzzle_size = int(puz_info[1])
        if puzzle_size == 4:
            upper_limit = 1
        elif puzzle_size == 9:
            upper_limit = 2
        else:
            upper_limit = 3
        return upper_limit, puzzle_size

    # Draws the boxes and buttons
    def draw_UI(self, window):
        pointer = turtle.Turtle()
        pointer.hideturtle()
        pointer.speed(0)
        pointer.penup()
        pointer.goto(200, 300)
        pointer.pendown()
        pointer.fd(200)
        pointer.right(90)
        pointer.fd(450)
        pointer.right(90)
        pointer.fd(200)
        pointer.right(90)
        pointer.fd(450)

        pointer.penup()
        pointer.goto(400, -200)
        pointer.pendown()
        pointer.right(180)
        pointer.fd(100)
        pointer.right(90)
        pointer.fd(800)
        pointer.right(90)
        pointer.fd(100)
        pointer.right(90)
        pointer.fd(800)

        window.addshape("Resources/quitbutton.gif")
        quitbutton = turtle.Turtle()
        quitbutton.hideturtle()
        quitbutton.speed(0)
        quitbutton.penup()
        quitbutton.goto(346.97, -253.03)
        quitbutton.shape("Resources/quitbutton.gif")
        quitbutton.showturtle()
        quitbutton.onclick(self.goodbye)

        window.addshape("Resources/loadbutton.gif")
        loadbutton = turtle.Turtle()
        loadbutton.hideturtle()
        loadbutton.speed(0)
        loadbutton.penup()
        loadbutton.goto(246.97, -253.03)
        loadbutton.shape("Resources/loadbutton.gif")
        loadbutton.showturtle()
        loadbutton.onclick(self.new_puzzle)

        window.addshape("Resources/resetbutton.gif")
        resetbutton = turtle.Turtle()
        resetbutton.hideturtle()
        resetbutton.speed(0)
        resetbutton.penup()
        resetbutton.goto(146.97, -253.03)
        resetbutton.shape("Resources/resetbutton.gif")
        resetbutton.showturtle()
        resetbutton.onclick(self.reset)

        puz_file = self.puz_file[3]
        thumbnail = puz_file.split(" ")[1][0:-1]
        window.addshape(thumbnail)
        logo = turtle.Turtle()
        logo.hideturtle()
        logo.speed(0)
        logo.penup()
        logo.goto(400, 310)
        logo.showturtle()
        logo.shape(thumbnail)

        puz_file = self.puz_file[4:]
        image_list = []
        for line in puz_file:
            # Checks for if the .puz file has "\n" on the last line
            if "\n" in line.split(" ")[1]:
                image_list.append(line.split(" ")[1][0:-1])
            else:
                image_list.append(line.split(" ")[1])
        for image in image_list:
            window.addshape(image)

    def get_leaderboard(self, puzzle):
        # If there isn't a text file made, create one and return a blank leaderboard
        scores = []
        filename = "leaderboard_" + puzzle + ".txt"
        try:
            with open(filename, mode='r') as leaderboard:
                for score in leaderboard:
                    scores.append(score)
        except FileNotFoundError as e:
            f = open(filename, mode='w')
            f.close()
            scores = []
            return scores

        # If a text file exists, return a list of scores
        scores = []
        with open(filename, mode='r') as leaderboard:
            for score in leaderboard:
                score_split = score.split(' - ')
                moves = score_split[0]
                name = score_split[1][0:len(score_split[1]) - 1]
                scores.append([moves, name])
        scores.sort(key=lambda x: int(x[0]))
        return scores

    # Draws the leaderboard on the side
    def draw_leaderboard(self, leaderboard):
        style = ('Comic Sans MS', 20)
        pointer = turtle.Turtle()
        pointer.hideturtle()
        pointer.color('blue')
        pointer.speed(0)
        pointer.penup()
        pointer.goto(210, 260)
        pointer.write("Hi-Scores:", font=style)
        pointer.goto(220, 230)

        if len(leaderboard) == 0:
            return True

        # If there are more than 10 people and scores stored, only include
        # the 10 best scores. Otherwise, draw the whole thing.
        top10 = []
        if len(leaderboard) > 10:
            for i in range(0, 10):
                top10.append(leaderboard[i])
        else:
            top10 = leaderboard.copy()
        for score in top10:
            style = ('Comic Sans', 18)
            pointer.write(score[1], font=style)
            pointer.fd(120)
            pointer.write(score[0], font=style)
            pointer.right(90)
            pointer.fd(40)
            pointer.right(90)
            pointer.fd(120)
            pointer.right(180)

    # Draws the puzzle and returns the initial board state and the solution
    def draw_puzzle(self):
        # Draw the grid around the puzzle pieces
        length = 105 * (self.upper_limit + 1)
        t = turtle.Turtle()
        t.hideturtle()
        t.speed(0)
        t.penup()
        t.goto(-352, 277)
        t.pendown()
        i = 0
        while i < 4:
            t.fd(length)
            t.right(90)
            i += 1
        i = 0
        while i < self.upper_limit:
            t.fd(105)
            t.right(90)
            t.fd(length)
            t.right(180)
            t.fd(length)
            t.right(90)
            i += 1
        t.fd(105)
        t.right(90)
        i = 0
        while i < self.upper_limit:
            t.fd(105)
            t.right(90)
            t.fd(length)
            t.right(180)
            t.fd(length)
            t.right(90)
            i += 1

        # Gets a list of all the image numbers
        puz_file = self.puz_file[4:]
        image_list = []
        for line in puz_file:
            if "\n" in line.split(" ")[1]:
                image_list.append(line.split(" ")[1][0:-5])
            else:
                image_list.append(line.split(" ")[1][0:-4])
        image_numbers = []
        for line in image_list:
            image_numbers.append(line.split("/")[2])

        # Saves a copy for later use in making the initial board
        # image_numbers will be used with .pop() to make the solution board
        pieces = image_numbers.copy()
        random.shuffle(pieces)

        solution = []
        while len(solution) != self.upper_limit + 1:
            row = []
            while len(row) != self.upper_limit + 1:
                row.append(image_numbers.pop(0))
            solution.append(row)

        # Making the initial board with the shuffled pieces list
        board = []
        while len(board) != self.upper_limit + 1:
            row = []
            while len(row) != self.upper_limit + 1:
                row.append(pieces.pop())
            board.append(row)

        # Actually visually drawing the board
        x = -300
        y = 225
        for row in board:
            for piece in row:
                shapename = self.image_path + str(piece) + ".gif"
                piece = turtle.Turtle()
                piece.hideturtle()
                piece.speed(0)
                piece.penup()
                piece.goto(x, y)
                piece.shape(shapename)
                piece.showturtle()
                piece.onclick(self.move_piece)
                x += 105
            x = -300
            y -= 105

        return board, solution

    # Updates the visual board after a valid click.
    def update_board(self, new_blank, new_piece):
        x = -300
        y = 225
        for row in self.board:
            for piece in row:
                if piece != 'blank' and piece != self.board[new_piece[0]][new_piece[1]]:
                    x += 105
                    continue
                elif piece == 'blank':
                    shapename = self.image_path + "blank.gif"
                elif piece == self.board[new_piece[0]][new_piece[1]]:
                    shapename = self.image_path + str(piece) + ".gif"
                piece = turtle.Turtle()
                piece.hideturtle()
                piece.penup()
                piece.speed(0)
                piece.goto(x, y)
                piece.shape(shapename)
                piece.showturtle()
                piece.onclick(self.move_piece)
                x += 105
            x = -300
            y -= 105
        self.current_moves += 1
        self.update_moves()

        if self.check_winner():
            self.congrats()

        if self.check_loser():
            self.you_lose()

    # Convert click coordinates into column numbers
    def get_column(self, x):
        if -350 <= x <= -250:
            return 0
        elif -245 <= x <= -145:
            return 1
        elif -140 <= x <= -40:
            return 2
        else:
            return 3

    # Convert click coordinates into row numbers
    def get_row(self, y):
        if 275 >= y >= 175:
            return 0
        elif 170 >= y >= 70:
            return 1
        elif 65 >= y >= -65:
            return 2
        else:
            return 3

    # Swaps the clicked on piece with the blank spot in self.board
    def move_piece(self, x, y):
        row = self.get_row(y)
        column = self.get_column(x)
        blank_temp = self.moveable(row, column)
        if blank_temp:
            self.board[blank_temp[0]][blank_temp[1]] = self.board[row][column]
            self.board[row][column] = 'blank'
            self.update_board([row, column], blank_temp)

    # Returns a list of all the adjacent pieces to the clicked piece
    def get_adjacent(self, x, y):
        corner_pieces = [[0, 0], [0, self.upper_limit],
                         [self.upper_limit, 0],
                         [self.upper_limit, self.upper_limit]]
        center_pieces = []
        for i in range(1, self.upper_limit):
            for j in range(1, self.upper_limit):
                piece = [i, j]
                if piece not in center_pieces and piece not in corner_pieces:
                    center_pieces.append(piece)

        if [x, y] in center_pieces:
            adjacent = [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]
        elif [x, y] in corner_pieces:
            if [x, y] == [0, 0]:
                adjacent = [[1, 0], [0, 1]]
            elif [x, y] == [0, self.upper_limit]:
                adjacent = [[0, self.upper_limit - 1], [1, self.upper_limit]]
            elif [x, y] == [self.upper_limit, 0]:
                adjacent = [[self.upper_limit, 1], [self.upper_limit - 1, 0]]
            elif [x, y] == [self.upper_limit, self.upper_limit]:
                adjacent = [[self.upper_limit, self.upper_limit - 1],
                            [self.upper_limit - 1, self.upper_limit]]
        else:
            if y == 0:
                adjacent = [[x + 1, y], [x - 1, y], [x, y + 1]]
            elif y == self.upper_limit:
                adjacent = [[x + 1, y], [x - 1, y], [x, y - 1]]
            elif x == 0:
                adjacent = [[x, y + 1], [x, y - 1], [x + 1, y]]
            elif x == self.upper_limit:
                adjacent = [[x, y + 1], [x, y - 1], [x - 1, y]]
        return adjacent

    # Checks if the clicked piece is adjacent to an empty space
    def moveable(self, x, y):
        adjacent = self.get_adjacent(x, y)
        for piece in adjacent:
            if self.board[piece[0]][piece[1]] == 'blank':
                return [piece[0], piece[1]]
        return False

    # Draws the move counter in the bottom left
    # Also returns a "number" turtle object for later clearing and rewriting
    def draw_moves(self):
        style = ('Comic Sans MS', 20)
        moves = turtle.Turtle()
        moves.hideturtle()
        moves.penup()
        moves.speed(0)
        moves.color('Red')
        moves.goto(-350, -265)
        moves.write("Number of Moves: ", font=style)
        moves_drawing = turtle.Turtle()
        moves_drawing.hideturtle()
        moves_drawing.penup()
        moves_drawing.speed(0)
        moves_drawing.color('Red')
        moves_drawing.goto(-170, -265)
        moves_drawing.write(str(self.current_moves), font=style)
        return moves_drawing

    # Updates the move counter in the bottom left
    def update_moves(self):
        self.moves_drawing.clear()
        style = ('Comic Sans MS', 20)
        moves_drawing = turtle.Turtle()
        moves_drawing.hideturtle()
        moves_drawing.penup()
        moves_drawing.speed(0)
        moves_drawing.color('Red')
        moves_drawing.goto(-170, -265)
        moves_drawing.write(str(self.current_moves), font=style)
        self.moves_drawing = moves_drawing

    # Prompts for an input based on the .puz files in the directory
    # If the user inputs a name of either a missing .puz or image folder,
    # Draw an error message
    def new_puzzle(self, x, y):
        puzzle_list = "Please select from the following:\n"

        for puzzle in self.puz_files:
            puzzle_list += puzzle + "\n"
        new_puzzle = self.screen.textinput("New Puzzle", puzzle_list)

        try:
            puz_info = self.process_puz_file(new_puzzle[0:-4])
            path = self.image_path(puz_info)
        except FileNotFoundError as e:
            with open('5001_puzzle.err', mode='a') as error_file:
                error_file.write(str(datetime.now()) + str(e) + "\n")
        except TypeError as e:
            with open('5001_puzzle.err', mode='a') as error_file:
                error_file.write(str(datetime.now()) + str(e) + "\n")

        if new_puzzle == None or len(new_puzzle) == 0 or new_puzzle not in self.puz_files:
            self.draw_file_error()
        if new_puzzle[0:-4] not in self.images_folders:
            self.draw_file_error()
        else:
            Board(new_puzzle[0:-4])
            turtle.mainloop()

    # Draws file_error.gif
    def draw_file_error(self):
        self.screen.addshape("Resources/file_error.gif")
        error = turtle.Turtle()
        error.speed(0)
        error.shape("Resources/file_error.gif")
        self.screen.ontimer(error.hideturtle, 3000)

    # "Solves" the puzzle
    def reset(self, x, y):
        x = -300
        y = 225
        for row in self.solution:
            for piece in row:
                shapename = self.image_path + str(piece) + ".gif"
                piece = turtle.Turtle()
                piece.speed(0)
                piece.penup()
                piece.goto(x, y)
                piece.shape(shapename)
                piece.onclick(self.move_piece)
                x += 105
            x = -300
            y -= 105
        for i in range(0, len(self.board)):
            self.board[i] = self.solution[i].copy()

    # Checks if the current board state matches the solution
    def check_winner(self):
        for i in range(0, len(self.board)):
            if self.board[i] != self.solution[i]:
                return False
        return True

    # Checks if the user has attempted at least more moves than allowed
    def check_loser(self):
        if self.current_moves >= self.max_moves:
            return True
        return False

    # Updates the puzzle's respective leaderboard.txt file with the user's score
    def update_leaderboard(self, name, moves):
        leaderboard_name = "leaderboard_" + self.puzzle + ".txt"
        with open(leaderboard_name, mode='a') as leaderboard:
            leaderboard.write(str(moves) + ' - ' + name + '\n')

    # Update leaderboard, show winning message, then quit
    def congrats(self):
        self.update_leaderboard(self.name, self.current_moves)
        self.screen.addshape("Resources/winner.gif")
        win = turtle.Turtle()
        win.speed(0)
        win.shape("Resources/winner.gif")
        time.sleep(3)
        self.goodbye(0, 0)

    # Show losing message, then quit
    def you_lose(self):
        self.screen.addshape("Resources/Lose.gif")
        lose = turtle.Turtle()
        lose.speed(0)
        lose.shape("Resources/Lose.gif")
        time.sleep(3)
        self.goodbye(0, 0)

    # Display credits then quit
    def goodbye(self, x, y):
        credits = "Resources/credits.gif"
        self.screen.addshape(credits)
        pointer = turtle.Turtle()
        pointer.shape(credits)
        time.sleep(5)
        self.screen.bye()

    def __str__(self):
        return str(self.board)

    def __eq__(self, other):
        for i in range(0, len(self.board)):
            for j in range(0, i):
                if self.board[i][j] != other.board[i][j]:
                    return False
        if self.puzzle != other.puzzle:
            return False
        return True


def main():
    Board('mario')
    turtle.mainloop()


if __name__ == "__main__":
    main()