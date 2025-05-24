import pygame


WIDTH = 500
HEIGHT = 500


pygame.init()

screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
pygame.display.set_caption('Le Chess')
#ygame.display.set_icon(pygame.image.load('assets/images/chess_icon.png'))

font = pygame.font.Font('freesansbold.ttf',20)
big_font = pygame.font.Font('freesansbold.ttf',50)
coordinate_font = "" #get font for the A-B, 1-8 on the sides
menu_font = "" #get font for the menu
menu_font_big = "" #get font for the menu (like for titles)

timer = pygame.time.Clock()
fps = 60


#asset laoding
# load in game piece images (queen, king, rook, bishop, knight, pawn) x 2
#NOTE: need to get some decent images
black_queen = pygame.image.load('assets/images/black_queen.png')
black_queen = pygame.transform.scale(black_queen, (80, 80))
small_black_queen = pygame.transform.scale(black_queen, (45, 45))
black_king = pygame.image.load('assets/images/black_king.png')
black_king = pygame.transform.scale(black_king, (80, 80))
small_black_king = pygame.transform.scale(black_king, (45, 45))
black_rook = pygame.image.load('assets/images/black_rook.png')
black_rook = pygame.transform.scale(black_rook, (80, 80))
small_black_rook = pygame.transform.scale(black_rook, (45, 45))
black_bishop = pygame.image.load('assets/images/black_bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (80, 80))
small_black_bishop = pygame.transform.scale(black_bishop, (45, 45))
black_knight = pygame.image.load('assets/images/black_knight.png')
black_knight = pygame.transform.scale(black_knight, (80, 80))
small_black_knight = pygame.transform.scale(black_knight, (45, 45))
black_pawn = pygame.image.load('assets/images/black_pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (65, 65))
small_black_pawn = pygame.transform.scale(black_pawn, (45, 45))
white_queen = pygame.image.load('assets/images/white_queen.png')
white_queen = pygame.transform.scale(white_queen, (80, 80))
small_white_queen = pygame.transform.scale(white_queen, (45, 45))
white_king = pygame.image.load('assets/images/white_king.png')
white_king = pygame.transform.scale(white_king, (80, 80))
small_white_king = pygame.transform.scale(white_king, (45, 45))
white_rook = pygame.image.load('assets/images/white_rook.png')
white_rook = pygame.transform.scale(white_rook, (80, 80))
small_white_rook = pygame.transform.scale(white_rook, (45, 45))
white_bishop = pygame.image.load('assets/images/white_bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (80, 80))
small_white_bishop = pygame.transform.scale(white_bishop, (45, 45))
white_knight = pygame.image.load('assets/images/white_knight.png')
white_knight = pygame.transform.scale(white_knight, (80, 80))
small_white_knight = pygame.transform.scale(white_knight, (45, 45))
white_pawn = pygame.image.load('assets/images/white_pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (65, 65))
small_white_pawn = pygame.transform.scale(white_pawn, (45, 45))
white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
white_promotions = ['bishop', 'knight', 'rook', 'queen']
white_moved = [False, False, False, False, False, False, False, False,
               False, False, False, False, False, False, False, False]
small_white_images = [small_white_pawn, small_white_queen, small_white_king, small_white_knight,
                      small_white_rook, small_white_bishop]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
small_black_images = [small_black_pawn, small_black_queen, small_black_king, small_black_knight,
                      small_black_rook, small_black_bishop]
black_promotions = ['bishop', 'knight', 'rook', 'queen']
black_moved = [False, False, False, False, False, False, False, False,
               False, False, False, False, False, False, False, False]
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

all_locations = []
black_in_check = False
white_in_check = False
