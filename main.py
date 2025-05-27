import pygame, sys
from settings import *
from get_moves import *
from engine import evaluate_position

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

pygame.init()

screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
pygame.display.set_caption('Le Chess')
#ygame.display.set_icon(pygame.image.load('assets/images/chess_icon.png'))

timer = pygame.time.Clock()
fps = 60

#asset laoding
# load in game piece images (queen, king, rook, bishop, knight, pawn) x 2
#NOTE: need to get some decent images
black_queen = pygame.image.load('assets/images/black queen.png')
#black_queen = pygame.transform.scale(black_queen, (200, 200))
small_black_queen = pygame.transform.scale(black_queen, (100, 100))
black_king = pygame.image.load('assets/images/black king.png')
#black_king = pygame.transform.scale(black_king, (200, 200))
small_black_king = pygame.transform.scale(black_king, (100, 100))
black_rook = pygame.image.load('assets/images/black rook.png')
#black_rook = pygame.transform.scale(black_rook, (200, 200))
small_black_rook = pygame.transform.scale(black_rook, (100, 100))
black_bishop = pygame.image.load('assets/images/black bishop.png')
#black_bishop = pygame.transform.scale(black_bishop, (200, 200))
small_black_bishop = pygame.transform.scale(black_bishop, (100, 100))
black_knight = pygame.image.load('assets/images/black knight.png')
##=black_knight = pygame.transform.scale(black_knight, (200, 200))
small_black_knight = pygame.transform.scale(black_knight, (100, 100))
black_pawn = pygame.image.load('assets/images/black pawn.png')
#black_pawn = pygame.transform.scale(black_pawn, (200, 200))
small_black_pawn = pygame.transform.scale(black_pawn, (100, 100))
white_queen = pygame.image.load('assets/images/white queen.png')
#white_queen = pygame.transform.scale(white_queen, (200, 200))
small_white_queen = pygame.transform.scale(white_queen, (100, 100))
white_king = pygame.image.load('assets/images/white king.png')
#white_king = pygame.transform.scale(white_king, (200, 200))
small_white_king = pygame.transform.scale(white_king, (100, 100))
white_rook = pygame.image.load('assets/images/white rook.png')
#white_rook = pygame.transform.scale(white_rook, (200, 200))
small_white_rook = pygame.transform.scale(white_rook, (100, 100))
white_bishop = pygame.image.load('assets/images/white bishop.png')
#white_bishop = pygame.transform.scale(white_bishop, (200, 200))
small_white_bishop = pygame.transform.scale(white_bishop, (100, 100))
white_knight = pygame.image.load('assets/images/white knight.png')
#white_knight = pygame.transform.scale(white_knight, (200, 200))
small_white_knight = pygame.transform.scale(white_knight, (100, 100))
white_pawn = pygame.image.load('assets/images/white pawn.png')
#white_pawn = pygame.transform.scale(white_pawn, (200, 200))
small_white_pawn = pygame.transform.scale(white_pawn, (100, 100))
white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
white_promotions = ['bishop', 'knight', 'rook', 'queen']

small_white_images = [small_white_pawn, small_white_queen, small_white_king, small_white_knight,
                      small_white_rook, small_white_bishop]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
small_black_images = [small_black_pawn, small_black_queen, small_black_king, small_black_knight,
                      small_black_rook, small_black_bishop]
black_promotions = ['bishop', 'knight', 'rook', 'queen']

piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']




def menu():
    
    """
    DESIGN
    Colour:
    main: rgb(17,128,26))
    highlight (dark): rgb(14,105,21)
    highlight (light): rgb(20,150,30)6
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
    #must be here despite performance due to having to be able to resize the window
    #cannot resize fonts, so have to recreate them each time
    font = pygame.font.Font('freesansbold.ttf',(height+width)//64)
    big_font = pygame.font.Font('freesansbold.ttf',(height+width)//32)
    global coordinate_font
    coordinate_font = pygame.font.Font('freesansbold.ttf',(height+width)//96) #get font for the A-B, 1-8 on the sides
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
            run = False
        if event.type == pygame.VIDEORESIZE:
            # There's some code to add back window content here.
            screen = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE)
            

#board drawing
def board():
    width = screen.get_width()
    height = screen.get_height()
    global x_offset
    global y_offset
    
    #to ensure gameboard is square
    b = min(width, height)/5
    a=b
    board_size = min(width, height) - a
    if width > height:
        width_greater = True
        height_greater = False
        a = width - (board_size)
    elif height > width:
        height_greater = True
        width_greater = False
        b = height - (board_size)
    else:
        same = True
        width_greater = False
        height_greater = False
    #pretty sure ^^ all works

    if width_greater:
        x_offset = a/2
        y_offset = b/2
        for i in range(16): #rows
            if i % 2 == 0:
                for j in range(4): #squares
                    pygame.draw.rect(screen, 'light gray', [(a / 2) + ((j*2) * (board_size / 8)), (b/2)+(2*(i // 4) * (board_size / 8)), board_size / 8, board_size / 8 ])
            else:
                for j in range(4):
                    pygame.draw.rect(screen, 'light gray', [(a / 2) + ((j*2 + 1) * (board_size / 8)), (b/2)+(2*(i // 4)+1) * (board_size / 8), board_size / 8, board_size / 8 ])
            
                    
    elif height_greater:
        x_offset = board_size/40
        y_offset = b/2
        for i in range(16):
            if i % 2 == 0:
                for j in range(4): #squares
                    pygame.draw.rect(screen, 'light gray', [x_offset + (j*2) * (board_size / 8), (b/2)+(2*(i // 4) * (board_size / 8)), board_size / 8, board_size / 8 ])
            else:
                for j in range(4):
                    pygame.draw.rect(screen, 'light gray', [x_offset + (j*2 + 1) * (board_size / 8), (b/2)+((2*(i // 4)+1) * (board_size / 8)), board_size / 8, board_size / 8 ])
    else:
        x_offset = board_size/40
        y_offset = b/2
        for i in range(16):
            if i % 2 == 0:
                for j in range(4): #squares
                    pygame.draw.rect(screen, 'light gray', [x_offset + (j*2) * (board_size / 8), (b/2)+(2*(i // 4) * (board_size / 8)), board_size / 8, board_size / 8 ])
            else:
                for j in range(4):
                    pygame.draw.rect(screen, 'light gray', [x_offset + (j*2 + 1) * (board_size / 8), (b/2)+((2*(i // 4)+1) * (board_size / 8)), board_size / 8, board_size / 8 ])
            
    #draw margin lines
           
    #board lines
    for i in range(9):
        #edge lines are thicker
        if i == 0 or i == 8:
            line_width = 2
        else:
            line_width = 1
        #draw vertical lines
        pygame.draw.line(screen, 'black',(x_offset + (i * board_size/8), y_offset), (x_offset + (i * board_size/8), y_offset + board_size) , line_width)
        #draw horizontal lines
        pygame.draw.line(screen, 'black',(x_offset, y_offset + (i * board_size/8)), (x_offset + board_size, y_offset + (i * board_size/8)) , line_width)
    

#draw pieces
def pieces():
    
    w = screen.get_width()
    h = screen.get_height()
    board_size = min(w, h) * 4/5
    global piece_size
    piece_size = board_size / 10 #(not /8 since should fit nicely in square, not be the exact same size as the square)
    pawn_piece_size = piece_size * 13/16
    
    scaled_white_pawn = pygame.transform.smoothscale(white_pawn, (pawn_piece_size, pawn_piece_size))
    scaled_black_pawn = pygame.transform.smoothscale(black_pawn, (pawn_piece_size, pawn_piece_size))
    scaled_white_king = pygame.transform.smoothscale(white_king, (piece_size, piece_size))
    scaled_black_king = pygame.transform.smoothscale(black_king, (piece_size, piece_size))
    scaled_white_queen = pygame.transform.smoothscale(white_queen, (piece_size, piece_size))
    scaled_black_queen = pygame.transform.smoothscale(black_queen, (piece_size, piece_size))
    scaled_white_rook = pygame.transform.smoothscale(white_rook, (piece_size, piece_size))
    scaled_black_rook = pygame.transform.smoothscale(black_rook, (piece_size, piece_size))
    scaled_white_bishop = pygame.transform.smoothscale(white_bishop, (piece_size, piece_size))
    scaled_black_bishop = pygame.transform.smoothscale(black_bishop, (piece_size, piece_size))
    scaled_white_knight = pygame.transform.smoothscale(white_knight, (piece_size, piece_size))
    scaled_black_knight = pygame.transform.smoothscale(black_knight, (piece_size, piece_size))
    scaled_white_images = [scaled_white_pawn, scaled_white_queen, scaled_white_king, scaled_white_knight, scaled_white_rook, scaled_white_bishop]
    scaled_black_images = [scaled_black_pawn, scaled_black_queen, scaled_black_king, scaled_black_knight, scaled_black_rook, scaled_black_bishop]

    #white pieces
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == "pawn":
            #pawns are smaller images, so need special placement to get central
            screen.blit(scaled_white_pawn,(x_offset + ((white_locations[i][0]+0.175) * board_size/8), y_offset + ((white_locations[i][1]+0.2) * board_size/8)))
        else:
            screen.blit(scaled_white_images[index],(x_offset + ((white_locations[i][0]+0.1) * board_size/8), y_offset + ((white_locations[i][1]+0.1) * board_size/8)))
        
        #selecting "animation"
        if turn_step < 2:
            if selected_piece == i:
                #could try scaling up the piece by a factor? like chess.com does
                pygame.draw.rect(screen, 'green', [x_offset + (white_locations[i][0] * board_size/8 + 1), y_offset + (white_locations[i][1] * board_size/8 + 1), board_size/8, board_size/8], 2)
    
    #black pieces
    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == "pawn":
            #pawns are smaller images, so need special placement to get central
            screen.blit(scaled_black_pawn,(x_offset + ((black_locations[i][0]+0.1) * board_size/8 + piece_size/7), y_offset + ((black_locations[i][1]+0.2) * board_size/8)))
        else:
            screen.blit(scaled_black_images[index],(x_offset + ((black_locations[i][0]+0.1) * board_size/8), y_offset + ((black_locations[i][1]+0.1) * board_size/8)))

        #selecting "animation"
        if turn_step > 1:
            if selected_piece == i:
                #could try scaling up the piece by a factor? like chess.com does
                pygame.draw.rect(screen, 'green', [x_offset + (black_locations[i][0] * board_size/8 + 1), y_offset + (black_locations[i][1] * board_size/8 + 1), board_size/8, board_size/8], 2)

#drawing material taken
def draw_material():
    # //TODO draw material taken
    #this should draw the material taken by each player, in a list, with the total material worth
    #it should be draw on the correct side (above/below)
    return 0       
#drawing valid movses
def draw_legal_moves(moves):
    global piece_size
    # //FIXME at small window sizes, these are offset drastically
    #it also happens at larger sizes, just less noticably
    for i in range(len(moves)):
        pygame.draw.circle(screen, "green", (x_offset + piece_size/8+ (moves[i][0] * (piece_size*5/4) + 50), y_offset + (moves[i][1] * (piece_size*5/4) + 50)), 5)

#drawing coordinates
def draw_coordinates():
    #draws little text on the sides of the board, to show coordinates (bottom, top, left and right, not just 2 of them  
    for i in range(8):
        letter_text = coordinate_font.render(chr(65+i), False, (0, 0, 0))   # A-H
        number_text = coordinate_font.render(str(1 + i), False, (0, 0, 0))  # 1-8
        
        screen.blit(letter_text, (x_offset + (i * piece_size * 5/4) + piece_size*5/8, y_offset - piece_size/4))
        screen.blit(letter_text, (x_offset + (i * piece_size * 5/4) + piece_size*5/8, y_offset + piece_size*10 + piece_size/8))
        
        screen.blit(number_text, (x_offset - piece_size/4 + 3, y_offset + (i * piece_size * 5/4) + piece_size*5/8))
        screen.blit(number_text, (x_offset + piece_size*10 + piece_size/8, y_offset + (i * piece_size * 5/4) + piece_size*5/8))

#choosing which side you are playing as (i.e. which is at bottom of board)
def choose_side(side_setting):
    #if random side
    if side_setting == "random":
        if pygame.time.get_ticks() % 2 == 0:
            return "white"
        else:
            return "black"
    #if selected black/white in settings:
    # //TODO make this a setting in the settings menu
    # also remember to check if second bit needs to be elif or not
    if side_setting == "white":
        return "white"
    elif side_setting == "black":
        return "black"

#game loop
black_moves = find_moves(black_pieces, black_locations, "black")
white_moves = find_moves(white_pieces, white_locations, "white")
def gameloop():
    global run
    if run:        
        global turn_step, white_pieces, black_pieces, white_locations, black_locations
        global moves, turn_count, selected_piece, white_moves, black_moves, in_check
        
        #draw everything
        screen.fill('dark gray')
        board()
        pieces()
        draw_coordinates()
        draw_material()
        
        evaluate_position(white_locations, black_locations, white_pieces, black_pieces)

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
            pygame.quit()
        
        #if left click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #pixel clicked on window // 100 => square clicked on
            x_coord = (event.pos[0] - x_offset) // (piece_size * 5/4)
            y_coord = (event.pos[1] - y_offset) // (piece_size * 5/4)
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
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == pygame.VIDEORESIZE:
                    # There's some code to add back window content here.
                    screen = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE)
            gameloop()
           
            
            
    elif menu() == "options":
        # //TODO options menu
        pygame.quit()
        run = False
    elif menu() == "dev_tools":
        # //TODO dev tools menu
        pygame.quit()
        run = False

           
pygame.quit()
