import pygame

all_locations = []
black_in_check = False
white_in_check = False


#game variables
white_pieces = ["rook","knight", "bishop", "king", "queen", "bishop", "knight", "rook",
                "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"]
white_locations = [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),
                   (0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1)]

black_pieces = ["rook","knight", "bishop", "king", "queen", "bishop", "knight", "rook",
                "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"]
black_locations = [(0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),
                   (0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6)]

taken_by_white_pieces = []
taken_by_black_pieces = []
white_moves = []
black_moves = []

# 0 is white to play, 1 is white piece selected, 2 is black to play, 3 is black piece selected
turn_step = 0
turn_count = 0 #total mvoves made, (total turn_steps / 2)
selected_piece = 65

pin_ray_squares = []
#if 1 piece giving check, can block it
in_check_by = []
in_check = False
pinned_pieces = []

black_moved = [False, False, False, False, False, False, False, False,
               False, False, False, False, False, False, False, False]
white_moved = [False, False, False, False, False, False, False, False,
               False, False, False, False, False, False, False, False]



def check_pinned(check_location):
    """
    if piece is pinned, returns the piece that is pinning it
    if more than 1 piece pinning, returns (9,9) 
    if not pinned, returns ()
    """
    pinned = False
    pinning_pieces = 0
    pinning_piece = ""
    for i in range(len(pinned_pieces)):
        if pinned_pieces[i][0] == check_location:
            pinned = True
            pinning_pieces+=1  #finds number of pieces pinning
            pinning_piece = pinned_pieces[i][1] #finds pinning piece
            
    if pinning_pieces > 1:
        #if more than 1 piece pinning, it CANNOT move (special case)
        return (9,9)
    else:
        #if 1 or 0 pieces pinning
        return pinning_piece
    
def slider_move_loop(location, colour,moves,x,y):
    global pin_ray_squares
    
    if colour == "white":
        opposite_colour_locations = black_locations
        same_colour_locations = white_locations
        opposite_pieces = black_pieces
    else:
        same_colour_locations = black_locations
        opposite_colour_locations = white_locations
        opposite_pieces = white_pieces
    
    #checks if empty, if not, stops checking that direction
    #then checks if same colour, if not, then taking it is possible
    chain = 1
    first = False
    second = False #(checking for pins)
    pin_location = () #(i.e. no pin location. It resets for each direction) (who you pin)
    new_pin_ray_squares = []
    return_pin_ray_squares = False
    while second == False and chain < 8:            
        #if not same colour (empty or other colour)
        if (location[0] + (chain * x), location[1] + (chain * y)) not in same_colour_locations and \
                -1 < location[0] + (chain * x) < 8 and -1 < location[1] + (chain * y) < 8: # and on board
            
            #if not seen piece yet, add move
            if first == False:
                moves.append((location[0] + (chain * x), location[1] + (chain * y)))   
            #need to get a seperate list for each piece, with loc. as index 0
            #is only not set back to what it was before looping if there is a pin detected
            if second == False:
                new_pin_ray_squares.append((location[0] + (chain * x), location[1] + (chain * y)))
            
            #if enemy, stop appending moves (since not empty)
            if (location[0] + (chain * x), location[1] + (chain * y)) in opposite_colour_locations:
                #gets the location of the piece being pinned.
                #ignored if no pin is found
                if first == False:
                    pinned_location = (location[0] + (chain * x), location[1] + (chain * y))
                
                if (location[0] + (chain * x), location[1] + (chain * y)) == opposite_colour_locations[opposite_pieces.index("king")]:
                        #if check
                        if first == False:
                            in_check = True
                            in_check_by.append((location[0], location[1], turn_count))
                            print("check")
                        
                        #if pin
                        elif second == False:
                            #pinned piece if piece behind it is king (cannot be moved)
                            new_pin_ray_squares.insert(0, location)
                            return_pin_ray_squares = True
                            new_pin_ray_squares.pop()
                            if [pinned_location, location, turn_count] not in pinned_pieces:
                                pinned_pieces.append([pinned_location, location, turn_count])
                
                if first == True:
                    second = True
                else:
                    first = True   
        else:
            #if own team, cannot pin or take
            second = True
        chain+=1

    if return_pin_ray_squares == True:
        if new_pin_ray_squares != [] and new_pin_ray_squares not in pin_ray_squares:
            pin_ray_squares.append(new_pin_ray_squares)
    return moves

#check for legal rook moves
def rook_moves(location, colour):
    moves = []
    # //TODO clean up if statement
    if colour == "white":
        opposite_colour_locations = black_locations
        same_colour_locations = white_locations
        opposite_pieces = black_pieces
    else:
        same_colour_locations = black_locations
        opposite_colour_locations = white_locations
        opposite_pieces = white_pieces
    #if pinned
    pinned_by = check_pinned(location)
    if pinned_by == (9,9): #if pinned by 2+ pieces
        #cannot move
        return moves
    elif pinned_by != (): #if pinned by 1 piece
        # //TODO get while_pinned moves R
        # it also only needs to check if *itself* is pinned
        for i in range(len(pinned_pieces)):
            pinning_piece = pinned_pieces[i][1]
            if opposite_pieces(opposite_colour_locations.index(pinning_piece)) == "rook":
                #moves between pinned and pinning
                pass
                #dont need to keep looping after finding the right pinning piece
                break
        
    #loops through right, left, down up:
    #in that order, since then the evens are increases, oddds are decreases
    for i in range(4):
        #assigns a multiplier which is later applied
        #this allows to check for moves in a line in all 4 directions
        #if right, down
        x = 0
        y = 0
        if i % 2 == 0:
            #if down
            if i == 0:
                y = 1
            else:
                x = 1
        #if left, up
        else:
            #if up
            if i == 1:
                y = -1
            else:
                x = -1
        
        moves = slider_move_loop(location, colour, moves,x,y)
    return moves

#check bishop moves
def bishop_moves(location, colour):
    moves = []
    #this is so that pin_ray_squares is only added for this piece if it is pinning something

   #if pinned
    pinned_by = check_pinned(location)
    if pinned_by == (9,9): #if pinned by 2+ pieces
        #cannot move
        return moves
    elif pinned_by != (): #if pinned by 1 piece
        # //TODO get while_pinned moves B
        #need to find moves that are also in the corresponding pin_ray_squares (of pinning piece)
        # find pin_ray_squares
        #check which direction the piece is pinned in
        #some shenanigans and can basically add pin_ray_squares to moves (if same piece or queen
        pass
    #loops through a,b,c,d:
    #a = 1,1 b = -1,-1, c = 1,-1 , d = -1,1
    #in that order, since then the evens are increases, odds are decreases
    for i in range(4):
        #assigns a multiplier which is later applied
        #this allows to check for moves in a line in all 4 directions
        #tried to have as few lines and checks as possible for file size and run speed
        x = 0; y = 0
        #if a or c
        if i % 2 == 0:
            if i == 0:
                x = 1; y = 1
            else:
                x = 1; y = -1
        #if b or d
        else:
            if i == 1:
                x = -1; y = -1
            else:
                x = -1; y = 1
        
        moves = slider_move_loop(location, colour, moves,x,y)
        
    return moves

#find knight moves
def knight_moves(location, colour):
    moves = []
    #if pinned
    pinned_by = check_pinned(location)
    if pinned_by == (): #if pinned
        #knights cannot move if pinned, since cannot move onto its own pin_ray_squares
       return moves

    if colour == "white":
        team_locations = white_locations
        opposite_colour = black_locations
        opposite_pieces = black_pieces
    else:
        team_locations = black_locations
        opposite_colour = white_locations
        opposite_pieces = white_pieces

    x_counts = [1,2,2,1,-1,-2,-2,-1]
    y_counts = [2,1,-1,-2,-2,-1,1,2]
    for i in range(8):
        #if dest square on board and not of same colour
        if -1 < location[0]+x_counts[i] < 8 and -1 < location[1]+y_counts[i] < 8 \
                and (location[0]+x_counts[i], location[1]+y_counts[i]) not in team_locations:
            moves.append((location[0]+x_counts[i],location[1]+y_counts[i]))
            #if giving check:
            if (location[0]+x_counts[i], location[1]+y_counts[i]) in opposite_colour:
                if opposite_pieces.index("king") == opposite_colour.index((location[0]+x_counts[i], location[1]+y_counts[i])):
                    in_check = True
                    in_check_by.append((location[0], location[1], turn_count))
                    print("check")          
    return moves

#find queen moves
def queen_moves(location, colour):
    #just uses bishop and roook move finders
    moves = rook_moves(location, colour)
    moves2 = bishop_moves(location, colour)
    
    for i in range(len(moves2)):
        moves.append(moves2[i])
    return moves

#finding king moves
def king_moves(location, colour):
    
    possible_x_changes = [-1,0,1,1,1,0,-1,-1]
    possible_y_changes = [1,1,1,0,-1,-1,-1,0]
    moves_list = []
    if colour == "white":
        opposite_colour_moves = black_moves
    else:
        opposite_colour_moves = white_moves
    
    if colour == "white":
        opposite_colour_locations = black_locations
        same_colour_locations = white_locations
    else:
        same_colour_locations = black_locations
        opposite_colour_locations = white_locations

    #checks if squares are empty
    for i in range(8):
        target_square = (location[0] + possible_x_changes[i], location[1] + possible_y_changes[i])
        if target_square not in same_colour_locations and -1 < target_square[0] < 8 and -1 < target_square[1] < 8 and target_square not in opposite_colour_moves:
            if in_check == True:
                #if square is in check, cannot move there
                if target_square not in pin_ray_squares:
                    moves_list.append(target_square)
            else:
                moves_list.append(target_square)
            
    return moves_list

#pawn moves
def pawn_moves(location, colour):
    moves = []
    max = 1
   #if pinned
    pinned_by = check_pinned(location)
    if pinned_by == (9,9): #if pinned by 2+ pieces
        #cannot move
        return moves
    elif pinned_by != (): #if pinned by 1 piece
        # //TODO get while_pinned moves P
        #need to find moves that are also in the corresponding pin_ray_squares (of pinning piece)
        # find pin_ray_squares
        #check which direction the piece is pinned in
        #some shenanigans and can basically add pin_ray_squares to moves (if same piece or queen
        pass
    
        if colour == "white":
            opposite_colour_locations = black_locations ; same_colour_locations = white_locations ; direction = 1
            if location in white_locations:
                pawn_index = white_locations.index(location)
                if white_moved[pawn_index] == False:
                    max = 2
        else:
            same_colour_locations = black_locations ; opposite_colour_locations = white_locations ; direction = -1
            if location in black_locations:
                pawn_index = black_locations.index(location)
                if black_moved[pawn_index] == False:
                    max = 2
            
        # checks 1 in front (and 2 if not moved). If square is empty can move there (+1 bc goes to 1 less than given num)
        for i in range(max+1):
            if -1 < location[1] + (i * direction) < 8 and (location[0], location[1] + (i * direction)) not in same_colour_locations \
                    and (location[0], location[1] + (i * direction)) not in opposite_colour_locations:
                moves.append((location[0], location[1] + (i * direction)))
        # checking diagonals for taking
        #from -1 to 1 (basically just to get -1 and 1 values)
        for i in range(-1,2):
            if i != 0:
                target_square = (location[0] + i, location[1] + direction)
                #if target square is on board, and ocupied by oppo colour
                if -1 < target_square[0] < 8 and -1 < target_square[1] < 8 and target_square in opposite_colour_locations:
                    moves.append(target_square)
                    if black_pieces.index("king") == opposite_colour_locations.index(target_square):
                        in_check = True
                        in_check_by.append((location[0], location[1], turn_count))
                        print("check")
        
    #en passant
    return moves


#check options for pieces to move
def find_moves(pieces, locations, turn):
    ##print("finding moves")
    moves = []
    all_moves = []
    
    #for every piece, finds their moves
    for i in range(len(pieces)):
        
        location = locations[i]
        ##print("location", location)
        piece = pieces[i]
        ##print("piece", piece)

        if piece == "pawn":
            moves = pawn_moves(location, turn)
        
        elif piece == "rook":
            moves = rook_moves(location, turn)
        
        elif piece == "knight":
            moves = knight_moves(location, turn)
        
        elif piece == "bishop":
            moves = bishop_moves(location, turn)

        elif piece == "queen":
            moves = queen_moves(location, turn)

        elif piece == "king":
            moves = king_moves(location, turn)
            
        all_moves.append(moves)
    return all_moves

