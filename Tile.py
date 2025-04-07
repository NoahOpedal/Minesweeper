import pygame

import functions


class Tile():
    def __init__(self, is_mine):
        self.clicked = False
        self.flagged = False
        self.is_mine = is_mine
        self.number_of_mines_around = None


    def draw(self, x, y, width, height, screen):
        if self.flagged:
            color = "red"
        #elif self.is_mine:     # For debugging
        #    color = "black"    #
        elif self.clicked:
            color = "white"                       
        else:
            color = "light grey"

        pygame.draw.rect(screen, color, (x, y, width, height))        

        if self.number_of_mines_around != 0 and self.clicked:
            font = pygame.font.Font(None, 12)
            number_text = font.render(str(self.number_of_mines_around), True, "black")
            text_rect = number_text.get_rect(center=((width//2)+x, (height//2)+y))
            screen.blit(number_text, text_rect)


    def click(self, tiles, tile_x, tile_y):
        self.clicked = True
        if self.is_mine:
            print("*explosion*")
            return "exploded"
        self.number_of_mines_around = functions.calculate_number_of_mines_around(tiles, tile_x, tile_y)


    def flag(self, x, y, tiles):
        if not self.clicked:
            if self.flagged:
                self.flagged = False
            else:
                self.flagged = True
                
            #functions.update_number_of_mines(not self.flagged)

        else:
            if functions.spacebar_functionality(x, y, tiles) == "exploded":
                return "exploded"

