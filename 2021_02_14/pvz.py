from scripts.game import Game

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
