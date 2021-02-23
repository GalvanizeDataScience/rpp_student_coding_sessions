import numpy as np

# not implemented: 
# Problem with the way S shooters are working (some zombies make it past s shooter)
# actually print loss or win when game over true

class Game:

    def __init__(self, inputs):
        '''
        Inputs include:
        
        '''
        self.game_over = False
        self.parse(inputs)
        self.turn = 0

    def parse(self, inputs):
        self.parse_lawn(inputs[0])
        self.parse_zombies(inputs[1])        

    def parse_lawn(self, lawn):
        '''
        convert string into an array that holds information about plants
        ----
        params:
            lawn: list of strings that describes the 'lawn'

        returns:
            None
        '''
        # Parse one line at a time?
        print('parsing the lawn')
        self.lawn = np.array([list(row) for row in lawn])

    def parse_zombies(self, zombies):
        '''
        convert list into a numpy array that holds information about zombies
        ----
        params:
            zombies: list of lists that contain integers describing the zombie

        returns:
            None
        '''    
        # we could use a dictionary {zombie_id: int, location: tuple (row,col), hp:int}
        # we could use a numpy array for the zombies with location by row/col and value = hp
        # we could leave as is, and reference it later
        print('parsing zombies')
        self.zombie_waiting_list = zombies
        self.zombies = np.zeros(self.lawn.shape)

    def play(self):
        '''
        plays game to completion

        '''
        while self.game_over is False: 
            self.play_one_turn()



    def play_one_turn(self):
        '''
        plays one turn of the game

        ''' 
        self.check_loss()
        # print('Playing turn', self.turn)
        self.move_zombies()
        self.enter_zombies()
        self.eat_plant()
        self.plants_shoot()
        self.turn += 1
        if not self.game_over:
            print('Playing turn', self.turn)
            print('Turn', self.turn)
            print('Lawn:')
            print(self.lawn)
            print('Zombies:')        
            print(self.zombies)

        


    def check_loss(self):
        '''
        decided if the game ends or not
        get's called in play_one_turn method
        Ways the game ends:
            zombies all gone
            one zombie makes it to zero column
            or lawn all spaces
        '''

        #if zombie zero column sums to not zero game is not on
        if self.turn >0:
            if np.sum(self.zombies[:0]) > 0:
                print('You Lose! Zombies Have Won...shit sucks')
                self.game_over = True

            #this needs to be called after zombies have entered the board/moved the first turn
            elif np.sum(self.zombies) == 0:
                print('Plants win! There is still good in the world :)')
                self.game_over = True  
            else:
                pass
            

    def enter_zombies(self):
        '''
        bring zombies onto the board if it's their turn
        '''
        # loop through zombie waiting list
        # if zombie[0] is this turn, move it onto board

        # for every zombie in the waiting list
        for zombie in self.zombie_waiting_list:
            # if it's the zombie's turn
            if zombie[0] == self.turn:
                # print('Placing zombie', zombie, 'at row', zombie[1], 'on turn', self.turn, 'with', zombie[2], 'hp')
                # the row it should enter in is zombie[1]
                row = zombie[1]
                # place this zombie on the board at row, in the last column.
                # the value we are putting there is the zombie's health
                self.zombies[row, -1] = zombie[2] 

    def move_zombies(self):
        '''
        moves zombies forward
        '''
        # print('Moving Zombies')
        # if the first item in zombie list is the right turn, then put it on the board
        if self.zombies[:, 0].sum() > 0:
            self.game_over = True
        else:
            # shift all zombies to the left one square
            new_board = np.zeros_like(self.zombies)
            new_board[:, :-1] = self.zombies[:, 1:]
            self.zombies = new_board


    def plants_shoot(self):
        '''
        makes all plants shoot
        shooting should decrease zombie hp
        'number' shooters go first
        then 'S' shooters, right to left then top to bottom

        '''
        # print('Plants are shooting')
        self.number_shooters()
        self.s_shooters()

    def number_shooters(self):
        # if the row of shooter is row of zombie, then health points decrease by the amount shooter is
        # if shots > zombie hp, then overflow to next zombie
        # get shots per row, and do things to zombies based on that
        for row in range(self.lawn.shape[0]):
            # get number of shots
            # decrement zombie health by number of shots
            self.shots_shots_shots(row)

    def shots_shots_shots(self, row):
        '''
        handles shots on a single row.
        ---
        params:
            row: intger specifying row of the lawn numpy array
        '''
        shots = sum([int(item) for item in self.lawn[row] if item.isdigit()])
        # print('Firing', shots, 'shots on row', row)

        # have we hit any zombies?

        while (shots > 0) & (sum(self.zombies[row, :]) > 0):
            # then we need to do shots
            for i, zombie in enumerate(self.zombies[row, :]):
                if zombie <= shots:
                    self.zombies[row, :][i] = 0
                    shots = shots - zombie            
                else:
                    self.zombies[row, :][i] = zombie - shots
                    shots = 0      

    def s_shooters(self):
        # 1. scan board from right to left and then top to bottom
        # 2. for each of these S shooters, shoot in 3 directions
        s_coords = self.get_s_shooters()
        for pos in s_coords:
            self.s_shots(pos)

        for pos in s_coords:
            pass
        pass

    def get_s_shooters(self):
        # for each row in the matrix return the indices of the s shooters
        # output rightmost and then topmost
        s_coords = []
        for col in range(self.lawn.shape[1])[::-1]:
            for row in range(self.lawn.shape[0]):
                if self.lawn[row,col] == 'S':
                    s_coords.append([row,col])
        return s_coords

    def s_shots(self, pos):
        #shoot diagonally up
        self.shoot_diag(pos, row_inc = -1)
        #shoot straight
        self.shoot_diag(pos, row_inc = 0)
        #shoot diagnoally down
        self.shoot_diag(pos, row_inc = 1)

    def shoot_diag(self, pos, row_inc):
        '''
        handles shooting for a single s-shooter (shooting up)
        ----
        params
            pos: position of the s shooter
        '''
        # reduce row increase col each time
        # otherwise go to next square
        max_row, max_col = self.lawn.shape
        # if we are outside the board
        while not ((pos[0] < 0) | (pos[0] >= max_row) | (pos[1] >= max_col)):
            # print('shooting at pos', pos)
            # if zombie in this square, take away 1 hp
            if self.zombies[tuple(pos)] != 0:
                self.zombies[tuple(pos)] -= 1
                return

            pos[0] += row_inc
            pos[1] += 1

    def eat_plant(self):
        '''
        Check if a zombie will eat a plant on the lawn
        '''
        # loop through our indicies (rows and columns) (lawn zombie)
        num_rows = self.lawn.shape[0]
        num_cols = self.lawn.shape[1]

        for row in range(num_rows):

            for col in range(num_cols):
                
                if self.zombies[row,col] != 0.0:
                    if self.lawn[row,col] is not ' ':
                        self.lawn[row,col] = ' '
                
            



if __name__ == '__main__':

    sample_inputs = [[
    '2   S   ',
    '  S     ',
    '21  S   ',
    '13      ',
    '2 3     '],
    [
        # on round 0 (the first round), a zombie will appear in row 4.
        [0,4,28],
        # on round 1, a zombie will appear in row 1.
        [1,1,6],
        # on round 2, a zombie will appear in rows 0 and 4
        [2,0,10],
        [2,4,15],
        # on round 3, a zombie will appear in rows 2 and 3
        [3,2,16],
        [3,3,13]]]

    game = Game(sample_inputs)


    game.play()


    ordered_shooters = []
    s_shooter_positions = np.where(game.lawn == 'S')
    for i in s_shooter_positions:
        col = game.lawn[:, -1]

    if 'S' in col:
        print('S-Shooter')

    list(range(10))[::-1]

    for i in range(10)[::-1]:
        print(i)

    for i in range(10):
        print(9-i)    

    for col in game.lawn[:,::-1]:
        print(col)

    for col_no, col in enumerate(game.lawn.T):
        print(col_no)
        print(col)

    game.lawn

    np.flip(game.lawn, axis=1).T

    np.flip(game.lawn, axis=0)

    start = 6
    stop = 3
    step = -1
    list(range(10)[start:stop:step])

    s_coords = []
    for col in range(game.lawn.shape[1])[::-1]:
        for row in range(game.lawn.shape[0]):
            if game.lawn[row,col] == 'S':
                s_coords.append([row,col])

    s_coords = []
    for col in range(game.lawn.shape[1]-1, -1, -1):
        for row in range(game.lawn.shape[0]):
            if game.lawn[row,col] == 'S':
                s_coords.append([row,col])            