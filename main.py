import pygame
import sys
from helper import SIZE, FPS
from board import draw_board, draw_pieces, set_click_state, move, draw_overlay
pygame.init()

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

run = True

while run:
    click = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True
    
    set_click_state(click)
    
    move()
    draw_board(screen)
    draw_overlay(screen)
    draw_pieces(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
sys.exit()