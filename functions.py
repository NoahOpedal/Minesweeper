import pygame
import random

import Tile


def generate_board(board_size):
    board = []
    new_number_of_mines = 150
    new_number_of_tiles = board_size[0]*board_size[1]
    new_number_of_non_mines = new_number_of_tiles-new_number_of_mines
    
    for row in range(board_size[1]):
        new_row = []
    
        for column in range(board_size[0]):
            is_mine = random.choice([False]*new_number_of_non_mines+[True]*new_number_of_mines)
            new_mine = Tile.Tile(is_mine)

            if is_mine:
                new_number_of_mines -= 1
            else:
                new_number_of_non_mines -= 1 
            new_number_of_tiles -= 1

            new_row.append(new_mine)

        board.append(new_row)

    return board


def calculate_number_of_mines_around(tiles, tile_x, tile_y):
    number_of_mines_around = 0

    # Calculate x and y for tiles around the relevant tile
    adjacent_columns = [tile_x]
    adjacent_rows = [tile_y]
    
    if tile_x > 0:
        adjacent_columns.append(tile_x - 1)
    if tile_x < board_width-1:
        adjacent_columns.append(tile_x + 1)
    if tile_y > 0:
        adjacent_rows.append(tile_y - 1)
    if tile_y < board_height-1:
        adjacent_rows.append(tile_y + 1)
    
    for x in adjacent_columns:
        for y in adjacent_rows:
            if tiles[y][x].is_mine:
                number_of_mines_around += 1

    return number_of_mines_around


def open_adjacent_zeroes(tile_x, tile_y, tiles):

    # Calculate x and y for tiles around the relevant tile
    adjacent_columns = [tile_x]
    adjacent_rows = [tile_y]
    
    if tile_x > 0:
        adjacent_columns.append(tile_x - 1)
    if tile_x < board_width-1:
        adjacent_columns.append(tile_x + 1)
    if tile_y > 0:
        adjacent_rows.append(tile_y - 1)
    if tile_y < board_height-1:
        adjacent_rows.append(tile_y + 1)


    for row in adjacent_rows:
        for column in adjacent_columns:
            current_tile = tiles[row][column]

            if not current_tile.clicked:
                current_tile.click(tiles, column, row)
             
                if current_tile.number_of_mines_around==0 and not current_tile.is_mine:
                    open_adjacent_zeroes(column, row, tiles)


def update_screen(screen, tiles, tile_width, tile_height):
    screen.fill("dark grey")

    tile_x = 1
    tile_y = 1
    for row in tiles:
        for tile in row:
            tile.draw(tile_x+1, tile_y+1, tile_width-2, tile_height-2, screen)
            tile_x += tile_width
        
        tile_x = 1
        tile_y += tile_height
        

def spacebar_functionality(tile_x, tile_y, tiles):                                      
    """When spacebar is pressed while hovering over an opened tile, 
    clicks all tiles around if number of flags around math the number
    on the tile"""

    # Calculate x and y for tiles around the relevant tile
    adjacent_columns = [tile_x]
    adjacent_rows = [tile_y]
    
    if tile_x > 0:
        adjacent_columns.append(tile_x - 1)
    if tile_x < board_width-1:
        adjacent_columns.append(tile_x + 1)
    if tile_y > 0:
        adjacent_rows.append(tile_y - 1)
    if tile_y < board_height-1:
        adjacent_rows.append(tile_y + 1)

    number_of_adjacent_flags = 0
    number_of_mines_around = tiles[tile_y][tile_x].number_of_mines_around

    for column in adjacent_columns:
        for row in adjacent_rows:
            if tiles[row][column].flagged:
                number_of_adjacent_flags += 1
    
    if number_of_adjacent_flags == number_of_mines_around:
        for row in adjacent_rows:
            for column in adjacent_columns:
                if not tiles[row][column].flagged:
                    if tiles[row][column].click(tiles, column, row) == "exploded":
                        return "exploded"
                    elif tiles[row][column].number_of_mines_around == 0:
                        open_adjacent_zeroes(column, row, tiles)


def update_game(tile_width, tile_height, tiles, click, flag):
    mouse_position = pygame.mouse.get_pos()
    row_index = int((mouse_position[1])//tile_height)
    column_index = int(mouse_position[0]//tile_width)
    if click:
        current_tile = tiles[row_index][column_index]
        
        if current_tile.click(tiles, column_index, row_index) == "exploded":
            return "exploded"
        
        elif current_tile.number_of_mines_around == 0:
            open_adjacent_zeroes(column_index, row_index, tiles)

    if flag:
        if tiles[row_index][column_index].flag(column_index, row_index, tiles) == "exploded":
            return "exploded"


def game_loop():
    global board_width
    global board_height
    board_width = 40    # Measured in tiles
    board_height = 40
    window_width = 800  # Because of a pygame rounding error the window width must be a multiple of the board width
    window_height = 800 # The same is true for the board and window heights, except for 200px for title and number of mines display
    tile_width = (window_width/board_width)
    tile_height = (window_height/board_height)

    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Minesweeper")
    tiles = generate_board((board_width, board_height))

    running = True
    while running:
        click = False
        flag = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False            
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                flag = True
        if update_game(tile_width, tile_height, tiles, click, flag) == "exploded":
            running = False

        else: 
            update_screen(screen, tiles, tile_width, tile_height)

        pygame.display.update()