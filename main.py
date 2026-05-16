import pygame
import sys
from helper import SIZE, FPS
from board import draw_board, draw_pieces
pygame.init()

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

run = True
    
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    draw_board(screen)
    draw_pieces(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
sys.exit()