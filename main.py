import pygame, sys
from settings import *


# TODO
# - en passant checker for pawn moves
# - castling checker for king moves
# - win check
    # - if king is in check, and cannot get out of check, lose
    # - if no moves and king not in check, draw
    # - if certain pieces are all the pieces, draw
    # - stalemate
    
# - win condition

# - check checker
    # - cant move king into check
    # - if king is in check, only moves that get out of check are valid
# - pin checker which is currently in progress. This counts as part of check checker since it stops you from making illegal moves due to attack on king

# - be able to flip board based on white colour you are playing
    # - not sure how rn or if possible at all with current board setup
# - mirror opponents pieces? Some sort of indication of your colour?
# - have a start menu, to be able to select settings, etc.
    # - when load up game, menu is presented.
    # - have options button, play game button, select opening button
        # - options leads to options, such as set resizes, play black, white, black/white, time formats
        # - play game obviously starts a game
        # - select opening button opens a list of openings with a search bar
            # - you can search (some simple search nothing complex)
            # - can select an opening that the bot will play (first few moves, until you force them to make differing move, or smt, decide criteria later)
            # - that opening is then played when you start your next game
# - when playing, only be able to select your own pieces (one-player, not 2, maybe even have this as an option)
# - add a graphic showing what pieces taken, etc. along botttom
    # - have pieces taken list, just render them basically, and have a little text line saying what the material worth is, and stuff
    
# - add list of prev. moves to the right. 
# - can save games in database?
    # - can access and reply later? or is that too much?
    
# - redo the sizes so fits nicer on the screen, maybe even allow certain resizes in a settings menu
    # - this will take time and be tough but yeah
    # - for piece images, just have a "big_image_size" and small one, which are variables, and can be changed in the future settings menu (set values
    # not like a slider)
    # - for board and stuff, a multiplier, would be needed.
    # - the variables may just be the current sizes, multiplied by the multiplier mentioned above, so everything is of a constant scale.    

# CHESSBOT TODO
# - evaluate a position, make ghost moves, reevaluate, and so on until best move found (move that causes biggest increase in evaluation)
# - find all possible moves for all pieces and add to a list
# - cycle through list, make those moves on a ghost board
# - reevaluate position, and store increase/decreases in a list.
# - find index of max value (of change of eval), and use that to find the possible moves in the moves list
# - the bot then plays that move, and things happen in the gui

"""
EVALUATING A POSITION
- assign each piece a static value, depending on what piece type. Add up static value of a position, gives the most rudamentary position eval
- if 2 positions have the same eval, randomly select which one to go for
- Dynamic Evaluation and Value Assignment of Piece (DEVAP)
    - this is the tough stuff
    - add up the number of possible moves higher is better
        - some moves are more important. Castling is worth at least 6x as much as a random rook move
    - if protecting piece, better
    - if attacking enemy piece, better
    - if under attack, worse (since then something has to defend it, locking up your pieces)
    - if more central, better
    - if directed towards enemy king, even better
    - if can trap enemy piece, very good better
    - if further up board, better
    - if your king is exposed, worse
    - if their king exposed, better
    That should give a decent bot, like at least like 600 chess.com Elo
    (especially with opening knowledge) (databases or smt)

For making better, allow multiple look-ahead moves. 2 is 4x better than 1, 3 is 3.5x better than 2, etc. But careful of moves taking too long.
    - this will be v. v. tough due to having to also predict your moves, however, as long as it looks for your best move also, it should just make solid moves, rather than having you like blunder smt, and it thinking ohhhhh yhhhh
"""
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

#counter
counter = 0
#pygame setup
pygame.init() 


def menu():
    
    """
    DESIGN
    Colour:
    main: rgb(17,128,26))
    highlight (dark): rgb(14,105,21)
    highlight (light): rgb(20,150,30)
    alt colour (blue): rgb(20,150,30)
    alt colour (purple): rgb(20,150,30)
    #need a couple more I think
    
    Menu:
    horizontal 3rds - (No button), (Button), (No button)
    vertical 11ths - (Empty), (Title*3), (Empty), (Button), (No button), (Button), (No button), (Button), (No button) Giving 3 buttons equally spaced
    Background is main
    button background is #highlight(dark)#
    button background (selected) is #highlight(light)#
    title is #alt colour (purple)#
    
    #need to have the button change slightly when clicked I think idrk rn
    
    
    """
    
    global screen
    #background or smt
    width = screen.get_width()
    height = screen.get_height()
    background = pygame.draw.rect(screen, (17,128,26), (0,0, width, height))
    
    
    #fonts
    font = pygame.font.Font('freesansbold.ttf',(height+width)//64 -2)
    big_font = pygame.font.Font('freesansbold.ttf',(height+width)//32 -2)
    coordinate_font = pygame.font.Font('freesansbold.ttf',(height+width)//96 -2) #get font for the A-B, 1-8 on the sides
    menu_font = pygame.font.Font('freesansbold.ttf',height//14) #get font for the menu
    menu_font_big = pygame.font.Font('freesansbold.ttf',(height+width)//16) #get font for the menu (like for titles)


    
    #title text
    menu_font_big.set_bold(True)
    title_text = menu_font_big.render('CHESSBOT', False, (0, 0, 0))
    screen.blit(title_text, ((width - title_text.get_width())/2,5))
    
    #menu buttons
    #if mouse is not over any button
    #menu button outlines
    pygame.draw.rect(screen, (14,105,21), (width/3, 5*height/11, width/3, height/11))
    pygame.draw.rect(screen, (20,150,30), (width/3, 5*height/11, width/3, height/11), 3, 3)
    
    pygame.draw.rect(screen, (14,105,21), (width/3, 7*height/11, width/3, height/11))
    pygame.draw.rect(screen, (20,150,30), (width/3, 7*height/11, width/3, height/11), 3, 3)
    
    pygame.draw.rect(screen, (14,105,21), (width/3, 9*height/11, width/3, height/11))
    pygame.draw.rect(screen, (20,150,30), (width/3, 9*height/11, width/3, height/11), 3, 3)
    
    
    mouse_pos = pygame.mouse.get_pos()
    if mouse_pos[0] > width/3 and mouse_pos[0] < (width/3 + width/3) and mouse_pos[1] > 5*height/11 and mouse_pos[1] < (5*height/11 + height/11):
        #if mouse is over start button, highlight it
        pygame.draw.rect(screen, (14,105,21), (width/3, 5*height/11, width/3, height/11), 3, 3)
        pygame.draw.rect(screen, (20,150,30), (width/3, 5*height/11, width/3, height/11))
        if pygame.mouse.get_pressed()[0]:
            #if mouse is clicked, start game
            print("start game")
            return "start"
        
    elif mouse_pos[0] > width/3 and mouse_pos[0] < (width/3 + width/3) and mouse_pos[1] > 7*height/11 and mouse_pos[1] < (7*height/11 + height/11):
        #if mouse is over options button, highlight it
        pygame.draw.rect(screen, (14,105,21), (width/3, 7*height/11, width/3, height/11), 3, 3)
        pygame.draw.rect(screen, (20,150,30), (width/3, 7*height/11, width/3, height/11))
        if pygame.mouse.get_pressed()[0]:
            #if mouse is clicked, open options menu
            return "options"
    
    elif mouse_pos[0] > width/3 and mouse_pos[0] < (width/3 + width/3) and mouse_pos[1] > 9*height/11 and mouse_pos[1] < (9*height/11 + height/11):
        #if mouse is over dev tools button, highlight it
        pygame.draw.rect(screen, (14,105,21), (width/3, 9*height/11, width/3, height/11), 3, 3)
        pygame.draw.rect(screen, (20,150,30), (width/3, 9*height/11, width/3, height/11))
        if pygame.mouse.get_pressed()[0]:
            #if mouse is clicked, open dev tools
            return "dev_tools"
        
        
    dev_tools_button_text = menu_font.render('dev tools', False, (0, 0, 0))
    screen.blit(dev_tools_button_text, ((width - dev_tools_button_text.get_width())/2, 9 * height/11 + 5))
    start_button_text = menu_font.render('start', False, (0, 0, 0))
    screen.blit(start_button_text, ((width - start_button_text.get_width())/2, height * 5/11 + 5))
    options_button_text = menu_font.render('options', False, (0, 0, 0))
    screen.blit(options_button_text, ((width - options_button_text.get_width())/2, height * 7/11 + 5))
    
    #to resize
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            # There's some code to add back window content here.
            screen = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE)
            
    
    


#board drawing
def board():
    width = screen.get_width()
    height = screen.get_height()
    
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [(width-200)-(column*(width/5)),(height-200)-(column*(width/5)),(width/10), (height/10)])
        else:
            pygame.draw.rect(screen, 'light gray', [700-(column*200),row*100,100,100])
            
        
    pygame.draw.rect(screen, 'gray', [0,800,WIDTH,100])
    pygame.draw.rect(screen, 'red', [0,800,WIDTH,100],5)
    pygame.draw.rect(screen, 'red', [800,0,200,HEIGHT],5)
        
    
    #lines
    for i in range(9):
        pygame.draw.line(screen, 'black', (0, 100*i), (800, 100*i),1)
        pygame.draw.line(screen, 'black', (100*i, 0), (100*i, 800),1)
    
      
#draw pieces
def pieces():

    #white pieces
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == "pawn":
            #pawns are smaller images, so need special placement to get central
            screen.blit(white_pawn,(white_locations[i][0] * 100 + 17, white_locations[i][1] * 100 + 30))
        else:
            screen.blit(white_images[index],(white_locations[i][0] * 100 + 10, white_locations[i][1] * 100 + 10))
        
        #selecting "animation"
        if turn_step < 2:
            if selected_piece == i:
                #could try scaling up the piece by a factor? like chess.com does
                pygame.draw.rect(screen, 'green', [white_locations[i][0] * 100 + 1, white_locations[i][1] * 100 + 1, 100, 100], 2)
    
    #black pieces
    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == "pawn":
            #pawns are smaller images, so need special placement to get central
            screen.blit(black_pawn,(black_locations[i][0] * 100 + 22, black_locations[i][1] * 100 + 30))
        else:
            screen.blit(black_images[index],(black_locations[i][0] * 100 + 10, black_locations[i][1] * 100 + 10))

        #selecting "animation"
        if turn_step > 1:
            if selected_piece == i:
                #could try scaling up the piece by a factor? like chess.com does
                pygame.draw.rect(screen, 'green', [black_locations[i][0] * 100 + 1, black_locations[i][1] * 100 + 1, 100, 100], 2)
                
#drawing valid movses
def draw_legal_moves(moves):
    for i in range(len(moves)):
        pygame.draw.circle(screen, "green", (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)

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

#game loop
black_moves = find_moves(black_pieces, black_locations, "black")
white_moves = find_moves(white_pieces, white_locations, "white")
def gameloop():
    global turn_step, white_pieces, black_pieces, white_locations, black_locations
    global moves, turn_count, selected_piece, white_moves, black_moves, in_check
    
    screen.fill('dark gray')
    board()
    pieces()

    if turn_step < 2:
        all_moves = white_moves
    else:
        all_moves = black_moves
    if selected_piece != 65 and 0 <= selected_piece < len(all_moves):
        moves = all_moves[selected_piece]
        draw_legal_moves(moves)
    else:
        moves = []

    ##print("before event loop")
    #events
    for event in pygame.event.get():      
        if event.type == pygame.QUIT:
            run = False  
        
        #if left click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #pixel clicked on window // 100 => square clicked on
            x_coord = event.pos[0] // 100 
            y_coord = event.pos[1] // 100
            click_coord = (x_coord, y_coord)
            ##print("left click")
            
            #check logic (and pinned pieces)
            if in_check == True:
                print(in_check_by)
                if turn_count == in_check_by[0][2] + 2: #resets checks for check recheck.
                    in_check = False
                    in_check_by = []
                        
            #if its been more than a turn since pinned, reset pinned pieces, and will recheck for them (before recheck, its reset)
            if pinned_pieces != []:
                print("turn count", turn_count, "\n pinned_pieces", pinned_pieces, "\n pin_ray_squares", pin_ray_squares)
                #should remove pinned pieces and pin_ray_squares from 2 turn_counts ago (i.e. if white pins, then it should remove when its white turn again)
                change = 0
                for i in range(len(pinned_pieces)):
                    if turn_count == pinned_pieces[i-change][2] +1:
                        i+=1 #accounts for deleted item in looping
                        change += 1 #finds how many items have been deleted, so can account for index changes
                        del(pinned_pieces[i-change])
                        del(pin_ray_squares[i-change])
                        
                
            #if whites turn
            if turn_step < 2:
                ##print("white turn")
                #if select white piece
                if click_coord in white_locations:
                    ##print("selected white piece")
                    selected_piece = white_locations.index(click_coord)
                    moves = find_moves(white_pieces, white_locations, 'white')[selected_piece]
                    #if on piece selection, move to dest. select
                    if turn_step == 0:
                        turn_step = 1
                #if dest. is valid
                ##print("move to dest.")
                if click_coord in moves and selected_piece != 65:
                    white_locations[selected_piece] = click_coord
                    ##print("moved")
                    white_moved[selected_piece] = True
                    ##print("set as moved")
                    #if dest is black
                    
                    if click_coord in black_locations:
                        ##print("take")
                        black_piece = black_locations.index(click_coord)
                        taken_by_white_pieces.append(black_pieces[black_piece])
                        
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                        black_moved.pop(black_piece)
                    
                    #resets for next turn
                    selected_piece = 65
                    turn_step = 2
                    moves = []
                    black_moves = find_moves(black_pieces, black_locations, 'black')
                    white_moves = find_moves(white_pieces, white_locations, 'white')
                    turn_count += 1



            #if blacks turn                
            if turn_step > 1:
                if click_coord in black_locations:
                    selected_piece = black_locations.index(click_coord)
                    moves = find_moves(black_pieces, black_locations, 'black')[selected_piece]
                    
                    if turn_step == 2:
                        turn_step = 3
                        
                if click_coord in moves and selected_piece != 65:
                    black_locations[selected_piece] = click_coord
                    black_moved[selected_piece] = True
                    
                    if click_coord in white_locations:
                        white_piece = white_locations.index(click_coord)
                        taken_by_black_pieces.append(white_pieces[white_piece])
                            
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                        white_moved.pop(white_piece)

                    selected_piece = 65
                    moves = []
                    turn_step = 0
                    black_moves = find_moves(black_pieces, black_locations, 'black')
                    white_moves = find_moves(white_pieces, white_locations, 'white')
                    turn_count += 1



run = True
while run:
    menu()
    if menu() == "start":
        #if start game, run game loop
        while run:
            gameloop()
            
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.VIDEORESIZE:
                    # There's some code to add back window content here.
                    screen = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE)
            
            
    elif menu() == "options":
        # //TODO options menu
        pygame.quit()
    elif menu() == "dev_tools":
        # //TODO dev tools menu
        pygame.quit()

    pygame.display.flip()
pygame.quit()
