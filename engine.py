#This is the engine file.
#Evaluation of a position is the main part
#The rest is basically just choosing moves to check, search trees maybe. Maybe it is a lot.
#remember, stockfish exists and is open source, so could snag some ideas from there. (as to process, not actual code)

#The big thing will be deciding when to stop searching a line. Otherwise it will continue forever.
#I think a hard limit on depth is a good idea, but also a time limit.
# best move will obviously be the one that has the highest eval increase/total (doesnt matter, whichever turns out easier)
#dev tools will be used to just change parameters. Like, at what eval limit do you stop looking down a line, stuff like that.

#V1 can literally just make random moves, and improve from there; take an iterative approach.

#actually, will this work in its own file? you'll need to import moves from main.py, and then import this file into main.py, to be able to play them, unless a file for moves?
from get_moves import *
from settings import *
import random # for random moves, temporary






def get_value(piece):
    if piece == "pawn":
        value = pawn_value
    elif piece == "knight":
        value = knight_value
    elif piece == "bishop":
        value = bishop_value
    elif piece == "rook":
        value = rook_value
    elif piece == "queen":
        value = queen_value
    elif piece == "king":
        value = king_value
    return value




def evaluate_position(white_locaitons, black_locations, white_pieces, black_pieces):
    white_score = 0
    black_score = 0
    # in future, maybe just evalung changes could improve performance
    for i in range(len(white_pieces)):
        white_score+= get_value(white_pieces[i])
        
    for i in range(len(black_pieces)):
        black_score+= get_value(black_pieces[i])
    
    return white_score - black_score


def get_best_move(pieces, locations, turn):
    """
    returns a list of 2 coords
    the first one is the moved pieces current location
    the second one is the destination
    The flipin foresight my days. Perfect for PC move indicator
    Also, just very helpful in general (especially for unambiguous move notation later on maybe? (i.e. exd5))
    """
    

    # for now, just return a random move
    #the piece being moved
    indices = []
    best_move = []
    moves = find_moves(pieces, locations, turn)
    for i in range(len(moves)):
        if moves[i] != []:
            indices.append(i)
    index = random.choice(indices)
    move_list = moves[index]
    best_move.append(random.choice(move_list))
    best_move.insert(0, locations[index])
    print(best_move)
    return best_move