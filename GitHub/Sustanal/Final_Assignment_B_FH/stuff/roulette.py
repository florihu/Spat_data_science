from random import randint


class Roulette:
    # class variables
    red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    black_numbers = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]

    """
    A simple roulette game.
    """

    # initialize one game

    def __init__(self):
        # ATTRIBUTES / PROPERTIES
        self.color = None  # red, black, or green
        self.result = None  # True/False (i.e. win or loose)
        self.money = 10  # your start balance
        self.won = 0  # times won
        self.lost = 0  # times lost
        print("Object of Roulette class created.")

    def place_bet(self, color):
        self.new_round()
        self.result = color == self.color  # True if user won, False otherwise
        self.adjust_money_and_stats()
        
    def new_round(self):
        ball_position = randint(0, 36)  # rolling the roulette ball over the numbers (i.e. get a random result)
        if ball_position in self.red_numbers:  # even
            self.color = 'red'
        elif ball_position in self.black_numbers:  # odd
            self.color = 'black'
        else:
            self.color = 'green'  # zero

    def adjust_money_and_stats(self):
        # money transaction and statistics
        if self.result:  # win situation
            self.won += 1
            if self.color == 'green':  # zero wins 35
                self.money +=35
            else:
                self.money +=1  # red or black win 1
        else:  # loose situation
            self.lost += 1
            self.money -=1  # player looses his bet


class CLI_Roulette(Roulette):
    """ Extends the roulette game with a Command Line Interface (CLI).
    All functionality of the Roulette class is inherited. """

    def __init__(self):
        super().__init__()
        self.play_from_command_line()

    def play_from_command_line(self):
        """ Game loop and command line interaction with user. """

        print('Welcome to Roulette, now place your bet! You have {} dollars in your wallet.'.format(self.money))
        print('Press "q" to quit the game.')

        while True:  # game loop
            user_input = input("\nPlace red (r), black (b), or green (g): ")  # PROMPT THE USER FOR INPUT

            # complete so user can just type first letter
            if user_input == 'r':
                user_input = 'red'
            elif user_input == 'b':
                user_input = 'black'
            elif user_input == 'g':
                user_input = 'green'

            # evaluate user input
            if user_input in ['red', 'black', 'green']:
                self.place_bet(user_input)
                print('Result: {}'.format(self.color))
                if self.result:
                    print('You win!')
                else:
                    print('You loose.')
                print('Money: {}. Won/Lost: {}/{}'.format(self.money, self.won, self.lost))  # print statistics
            elif user_input == 'q':
                print('You have quit the game.')
                break  # exit the while loop (and thus quit the game)
            else:  # handle unrecognized user input
                print('Please type "r" for red, "b" for black, "g" for green, or "q" to quit.')

game = Roulette()  # create single instance (necessary for the GUI)

if __name__ == "__main__":
    # to demonstrate the capabilities of the Roulette class
    # show attributes
    print("Color: {}. Win: {}. Money: {}, Stats (won/lost): {}/{}.".format(game.color, game.result, game.money, game.won, game.lost))
    game.place_bet('red')  # play one round
    print("Color: {}. Win: {}. Money: {}, Stats (won/lost): {}/{}.".format(game.color, game.result, game.money, game.won, game.lost))

    # start command-line-Roulette
    print('\nNow starting the game from a command-line interface...')
    cli_game = CLI_Roulette()
