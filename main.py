import pygame
import sys
from helper import SIZE, FPS
from board import draw_board, draw_pieces, set_click_state, move, draw_selected_overlay, draw_highlighted_overlay
pygame.init()

window = pygame.display.set_mode(SIZE)
screen = pygame.Surface(SIZE, pygame.SRCALPHA)
clock = pygame.time.Clock()

run = True

while run:
    click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True

    screen.fill((0, 0, 0, 0))

    set_click_state(click)
    move()
    draw_board(screen)
    draw_selected_overlay(screen)
    draw_highlighted_overlay(screen)
    draw_pieces(screen)
    window.blit(screen, (0, 0))
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
sys.exit()