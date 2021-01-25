import pygame, sys
from solver import Solver

#GUI
#Screen setup
pygame.init()
pygame.display.set_caption("Cryptarithm - 13519106 (Shifa Salsabiila)")

screen = pygame.display.set_mode((710, 410))
surface1 = pygame.Surface((700, 400)) 
surface2 = pygame.Surface((350, 400)) 
surface3 = pygame.Surface((350,400))
surface4 = pygame.Surface((350,350)) #Grid left
surface5 = pygame.Surface((350,350)) #Grid right
cell_width = 35

#Clock
clock = pygame.time.Clock()

#Colors
COLOR_BLACK = (0,0,0)
COLOR_WHITE = (255, 255, 255)
COLOR_DGREEN = (39,87,85)
COLOR_AQUA = (84,198,190)
COLOR_YELLOW = (247,177,92)
COLOR_LIGHT = (247,247,247)
COLOR_DARK = (207,207,207)

#MAIN GAME
class Cryptarithm:
    def __init__(self):
        self.new_game()

    def message_init(self, color, text, x_loc, y_loc, font_name, font_size, surface, centered): 
        path = "font/" + font_name
        font = pygame.font.Font(path, font_size)
        text = font.render(text, True, color)
        if centered:
            text_rect = text.get_rect()
            text_rect.center = (x_loc, y_loc)
            surface.blit(text, text_rect)
        else:
            surface.blit(text, (x_loc, y_loc))


    def update_display(self, board_no, mouse_loc):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if self.current_screen == 2:
                        if event.key == pygame.K_BACKSPACE:
                            self.backspace()
                        else:
                            self.get_input(event.unicode)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.current_screen == 1:
                        loc = pygame.mouse.get_pos()
                        if 290 <= loc[0] <= 290+120 and 175 <= loc[1] <= 175+50:
                            self.current_screen = 2
                        elif 245 <= loc[0] <= 245+205 and 245 <= loc[1] <= 245+50:
                            self.auto_solve = True
                            self.current_screen = 2
                    if self.current_screen == 2:
                        loc = pygame.mouse.get_pos()
                        if self.auto_solve:
                            if 550 <= loc[0] <= 550+50 and 177 <= loc[1] <= 177+36:
                                self.read_file(self.file_name)
                                #Calling Solver
                                self.solver = Solver(self.operands, self.result)
                                self.current_screen = 3
                        else:
                            pass
                    if self.current_screen == 3:
                        loc = pygame.mouse.get_pos()
                        if 5+10 <= loc[0] <= 5+10+70 and 55+295 <= loc[1] <= 55+295+40:
                            self.new_game()
                        if 355+265 <= loc[0] <= 355+265+70 and 55+295 <= loc[1] <= 55+295+40:
                            self.solver.solution_number += 1  
                        
            loc = pygame.mouse.get_pos()
            self.draw_board(self.current_screen, loc)
            pygame.display.update()
            clock.tick(60)

    def draw_board(self, board_no, mouse_loc):
        if board_no == 1:
            self.draw_board1(mouse_loc)
        elif board_no == 2:
            self.draw_board2(mouse_loc)
        elif board_no == 3:
            self.draw_board3(mouse_loc)

    def draw_board1(self, mouse_loc):
        screen.fill(COLOR_LIGHT)
        surface1.fill(COLOR_LIGHT)
        self.message_init(COLOR_AQUA, "CRYPTARITHM", 350, 100, "Gameplay.ttf", 60, surface1, True)
        button1_color, button2_color = COLOR_YELLOW,COLOR_YELLOW
        text1_color, text2_color = COLOR_DGREEN, COLOR_DGREEN

        if 290 <= mouse_loc[0] <= 290+120 and 175 <= mouse_loc[1] <= 175+50: 
            button1_color = COLOR_DGREEN
            text1_color = COLOR_AQUA
            
        if 245 <= mouse_loc[0] <= 245+205 and 245 <= mouse_loc[1] <= 245+50: 
            button2_color = COLOR_DGREEN
            text2_color = COLOR_AQUA

        pygame.draw.rect(surface1, button1_color, pygame.Rect(290, 175, 120, 50), border_radius = 25) 
        pygame.draw.rect(surface1, button2_color, pygame.Rect(245, 245, 205, 50), border_radius = 25)  
        self.message_init(text1_color, "Play", 350, 200, "Gameplay.ttf", 20, surface1, True)
        self.message_init(text2_color, "Auto Solve", 350, 270, "Gameplay.ttf", 20, surface1, True)
        screen.blit(surface1, (5,5))
        
    def draw_board2(self, mouse_loc):
        screen.fill(COLOR_LIGHT)
        surface1.fill(COLOR_LIGHT)
        self.message_init(COLOR_AQUA, "Enter file name: ", 350, 100, "Gameplay.ttf", 40, surface1, True)
        button_color = COLOR_DGREEN
        if 550 <= mouse_loc[0] <= 550+50 and 177 <= mouse_loc[1] <= 177+36: 
            button_color = COLOR_YELLOW

        pygame.draw.rect(surface1, COLOR_DARK, pygame.Rect(105, 177, 501, 40), border_radius=20)
        pygame.draw.rect(surface1, COLOR_WHITE, pygame.Rect(105, 175, 500, 40), border_radius=20)
        pygame.draw.rect(surface1, button_color, pygame.Rect(550, 177, 50, 36), border_radius=18)
        self.message_init(COLOR_DGREEN, self.file_name, 120, 185, "Consolas.ttf", 22, surface1, False)
        screen.blit(surface1, (5,5))

    def draw_board3(self, mouse_loc):
        screen.fill(COLOR_LIGHT)
        surface2.fill(COLOR_LIGHT)
        surface3.fill(COLOR_AQUA)
        surface4.fill(COLOR_LIGHT)
        surface5.fill(COLOR_AQUA)

        #LHS Answer Grid
        self.message_init(COLOR_AQUA, "ENCRYPTION", 75, 5, "Gameplay.ttf", 30, surface2, False)
        for i in range(len(self.operands)):
            for j in range(len(self.operands[i])):
                self.grid1[i][9-j] = self.operands[i][len(self.operands[i])-1-j]
        self.grid1[len(self.operands)][1] = '+'
        for j in range(2,10):
            self.grid1[len(self.operands)][j] = '_'
        for j in range(len(self.result)):
            self.grid1[len(self.operands)+1][9-j] = self.result[len(self.result)-1-j]
        self.draw_grid(COLOR_DGREEN, i, j, self.grid1, surface4)

        #RHS Answer Grid
        self.message_init(COLOR_LIGHT, "ANSWER", 112, 5, "Gameplay.ttf", 30, surface3, False)
        x = len(self.solver.final_results)
        cur = self.solver.final_results[self.solver.solution_number%x]
        for i in range(len(cur)-1):
            for j in range(len(cur[i])):
                self.grid2[i][9-j] = cur[i][len(cur[i])-1-j]
        self.grid2[len(self.operands)][1] = '+'
        for j in range(2,10):
            self.grid2[len(self.operands)][j] = '_'
        for j in range(len(cur[len(cur)-1])):
            self.grid2[len(cur)][9-j] = cur[len(cur)-1][len(cur[len(cur)-1])-1-j]
        self.draw_grid(COLOR_LIGHT, i, j, self.grid2, surface5)

        #Result Description
        self.message_init(COLOR_LIGHT, f'Runtime: {"%.5f" % round(self.solver.runtime,5)}', \
            10, 315, "Gameplay.ttf", 10, surface5, False)
        self.message_init(COLOR_LIGHT, f'Checks: {self.solver.checks}', \
            10, 330, "Gameplay.ttf", 10, surface5, False)

        #Main and next buttons
        button1_color, button2_color = COLOR_DGREEN, COLOR_YELLOW
        text1_color, text2_color = COLOR_LIGHT, COLOR_DGREEN
        if 5+10 <= mouse_loc[0] <= 5+10+70 and 55+295 <= mouse_loc[1] <= 55+295+40: 
            button1_color = COLOR_AQUA
        if 355+265 <= mouse_loc[0] <= 355+265+70 and 55+295 <= mouse_loc[1] <= 55+295+40: 
            button2_color = COLOR_LIGHT

        pygame.draw.rect(surface4, button1_color, pygame.Rect(10, 295, 70, 40), border_radius = 20)  
        self.message_init(text1_color, "MAIN", 45, 315, "Gameplay.ttf", 15, surface4, True)
        pygame.draw.rect(surface5, button2_color, pygame.Rect(265, 295, 70, 40), border_radius = 20)  
        self.message_init(text2_color, "NEXT", 300, 315, "Gameplay.ttf", 15, surface5, True)
        
        screen.blit(surface2, (5, 5))
        screen.blit(surface3, (355, 5))
        screen.blit(surface4, (5, 55))
        screen.blit(surface5, (355, 55))

    def draw_loading(self):
        screen.fill(COLOR_DGREEN)
        surface2.fill(COLOR_DGREEN)
        self.message_init(COLOR_LIGHT, "LOADING...", 350, 200, "Gameplay.ttf", 30, surface2, True)
        screen.blit(surface2, (5, 5))
    
    def draw_grid(self, color, x_loc, y_loc, grid, surface):
        for i in range(10):
            for j in range(10):
                self.message_init(color, grid[i][j], j*cell_width, i*cell_width, \
                    "Arial.ttf", 20, surface, False)

    def get_input(self, char):
        self.file_name += char

    def backspace(self):
        self.file_name = self.file_name[:-1]

    def read_file(self, file_name):
        path = "test/" + file_name
        f = open(path, 'r')
        lines = f.readlines()
        
        for i in range(len(lines) - 2):
            self.operands.append(lines[i].rstrip())
        self.operands[-1] = self.operands[-1][:-1]
        self.result = lines[-1].rstrip()
        
    def new_game(self):
        #Attribute instantiation
        self.current_screen = 1
        self.auto_solve = False
        self.file_name = ""
        self.grid1 = [["" for j in range(10)] for i in range(10)]
        self.grid2 = [["" for j in range(10)] for i in range(10)]
        self.operands = []
        self.result = ""

        #Methods
        loc = pygame.mouse.get_pos()
        self.update_display(self.current_screen, loc)

#DRIVER
game = Cryptarithm()

