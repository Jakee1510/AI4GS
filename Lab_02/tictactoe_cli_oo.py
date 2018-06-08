'''Tic-Tac-Toe

Object Oriented Version 1

Created for HIT3046 AI for Games
By Clinton Woodward cwoodward@swin.edu.au

Notes/Tips:
* Exactly the same behaviour as the function based version (tictactoe_cli.py).
* Very simple single class conversion of functions and global variables
* Game loop still controlled by the three input/update/render methods
* Internal class helper functions are marked by a leading "_"
* All class methods also have "self" as their first parameter
* All class variables/methods need to have a leading "self." 

'''

from random import randrange
import random



class TicTacToe(object):

    # class variables - belong to the *class* - NOT an object instance.
    WIN_SET = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), 
        (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)
    )

    print(WIN_SET)
                
    HR = '-' * 40
    
    def __init__(self):
    
        # global variables for game data
        self.board = [' '] * 9
        
        self.players = {'x': 'Human', 'o': 'Super AI' }
        self.winner = None
        self.move = None
        self.previous_move = 0
        self.ai_level = 3
        
        
        # by default the human player starts. This could be random or a choice.
        self.current_player = 'x'

        # Welcome ...
        print ('Welcome to the amazing+awesome tic-tac-toe!')
        # Show help (number) details
        self.show_human_help()
        #Select Difficulty: 0 = easy, 1 = Easy, 2 = Medium, 3 = Hard.
        proceed = False
        while proceed == False:
            print('Select Difficulty: 0 = easy, 1 = Easy, 2 = Medium, 3 = Hard.')
            difficulty = input()
            if difficulty == '0':
                self.ai_level = 0
                proceed = True
            if difficulty == '1':
                self.ai_level = 1
                proceed = True
            if difficulty == '2':
                self.ai_level = 2
                proceed = True
            if difficulty == '3':
                self.ai_level = 3
                proceed = True
            else:
                print("Please enter a value between 0-3.")
        # show the initial board and the current player's move
        self.render_board()
        # show the AI_difficulty you are vsing.
        print('You are challenged by a level %s computer player.' % self.ai_level)
        
        
    def _check_move(self):
        '''This function will return True if ``move`` is valid (in the board range 
        and free cell), or print an error message and return False if not valid. 
        ``move`` is an int board position [0..8].
        '''
        try:
            self.move = int(self.move)
            if self.board[self.move] == ' ':
                return True
            else:
                print ('>> Sorry - that position is already taken!')
                return False
        except:
            print ('>> %s is not a valid position! Must be int between 0 and 8.' % self.move)
            return False
        
        
    def _check_for_result(self):
        '''Checks the current board to see if there is a winner, tie or not.
        Returns a 'x' or 'o' to indicate a winner, 'tie' for a stale-mate game, or
        simply False if the game is still going.
        '''
        board = self.board
        for row in self.WIN_SET:
            if board[row[0]] == board[row[1]] == board[row[2]] != ' ':
                return board[row[0]] # return an 'x' or 'o' to indicate winner
    
        if ' ' not in board:
            return 'tie'
    
        return None
    
    #===========================================================================
    # agent (human or AI) functions
    
    def get_human_move(self):
        '''Get a human players raw input '''
        previous_move = input('[0-8] >> ')
        return previous_move

    
    def get_ai_move(self):
        '''Get the AI's next move '''
        # A simple dumb random move - valid or NOT! LEVEL 0 
        # Note: It is the models responsibility to check for valid moves...
        board = self.board
        if self.ai_level == 0:
            return randrange(9) # [0..8]

        
        elif self.ai_level == 1:

            #GOAL IS TO FIND WIN CONDITION
            for row in self.WIN_SET:
                if (board[row[0]]  == 'o' and board[row[1]] == 'o') and (board[row[2]] == ' '):
                    return row[2]
                if (board[row[0]]  == 'o' and board[row[2]] == 'o') and (board[row[1]] == ' '):
                    return row[1]
                if (board[row[1]]  == 'o' and board[row[2]] == 'o') and (board[row[0]] == ' '):
                    return row[0]      
            else:
               return randrange(9)

        elif self.ai_level == 2:

            #GOAL IS TO BLOCK PLAYER'S WIN CONDITION
           for row in self.WIN_SET:
                if (board[row[0]] == 'x' and board[row[1]] == 'x') and (board[row[2]] == ' '):
                    return row[2]
                if (board[row[0]] == 'x' and board[row[2]] == 'x') and (board[row[1]] == ' '):
                    return row[1]
                if (board[row[1]] == 'x' and board[row[2]] == 'x') and (board[row[0]] == ' '):
                    return row[0]      
           else:
               return randrange(9)
               
        elif self.ai_level == 3:

            #MIXES BOTH GOALS ABOVE, BUT PRIORITISES TO WIN OVER BLOCKING.
            for row in self.WIN_SET:
                if (board[row[0]]  == 'o' and board[row[1]] == 'o') and (board[row[2]] == ' '):
                    return row[2]
                if (board[row[0]]  == 'o' and board[row[2]] == 'o') and (board[row[1]] == ' '):
                    return row[1]
                if (board[row[1]]  == 'o' and board[row[2]] == 'o') and (board[row[0]] == ' '):
                    return row[0]                    
            else:
                for row in self.WIN_SET:
                    if (board[row[0]] == 'x' and board[row[1]] == 'x') and (board[row[2]] == ' '):
                        return row[2]
                    if (board[row[0]] == 'x' and board[row[2]] == 'x') and (board[row[1]] == ' '):
                        return row[1]
                    if (board[row[1]] == 'x' and board[row[2]] == 'x') and (board[row[0]] == ' '):
                        return row[0]

            return randrange(9)
            
                    
           
    
    #===========================================================================
    # Standard trinity of game loop methods (functions)
    
    def process_input(self):
        '''Get the current players next move.'''
        if self.current_player == 'x':
            self.move = self.get_human_move()
        else:
            self.move = self.get_ai_move()
    
    
    def update_model(self):
        '''If the current players input is a valid move, update the board and check 
        the game model for a winning player. If the game is still going, change the
        current player and continue. If the input was not valid, let the player
        have another go.
        '''
        if self._check_move():
            # do the new move (which is stored in the instance 'move' variable)
            self.board[self.move] = self.current_player
            # check board for winner (now that it's been updated)
            self.winner = self._check_for_result()
            # change the current player (regardless of the outcome)
            if self.current_player == 'x':
                self.current_player = 'o'
            else:
                self.current_player = 'x'
        else:
            print ('Try again')
        
    
    def render_board(self):
        '''Display the current game board to screen.'''
        board = self.board
        print ('    %s | %s | %s' % tuple(self.board[:3]))
        print ('   -----------')
        print ('    %s | %s | %s' % tuple(self.board[3:6]))
        print ('   -----------')
        print ('    %s | %s | %s' % tuple(self.board[6:]))
        
        # pretty print the current player name
        if self.winner is None:
            print ('The current player is: %s' % self.players[self.current_player])
    
    #===========================================================================
     
    def show_human_help(self):
        '''Show the player help/instructions. '''
        tmp = '''
    To make a move enter a number between 0 - 8 and press enter.  
    The number corresponds to a board position as illustrated:
    
        0 | 1 | 2
        ---------
        3 | 4 | 5
        ---------
        6 | 7 | 8
        '''
        print (tmp)
        print (self.HR)
    
    def show_gameresult(self):
        '''Show the game result winner/tie details'''
        print (self.HR)
        if self.winner == 'tie':
            print ('TIE!')
        else:
            print ('%s is the WINNER!!!' % self.players[self.winner])
        print (self.HR)    
        print ('Game over. Goodbye')


#==============================================================================
# Separate the running of the game using a __name__ test. Allows the use of this
# file as an imported module
#==============================================================================
       
if __name__ == '__main__':
    
    game = TicTacToe()
   
    
    # Standard game loop structure
    while game.winner is None:
        game.process_input()
        game.update_model()
        game.render_board()
        

    # Some pretty messages for the result
    game.show_gameresult()
