import pygame
import sys
from helper import SIZE, FPS
from board import draw_board, draw_pieces, get_event, draw_selected_overlay, draw_highlighted_overlay, get_mate, draw_promo_overlay, GameState, UIState

print("Enjoy!")

pygame.init()
window = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Chess(not that great)")
screen = pygame.Surface(SIZE, pygame.SRCALPHA)
clock = pygame.time.Clock()

gamestate = GameState()
uistate = UIState()

run = True

while run:
    click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        else:
            get_event(event, gamestate, uistate)


    screen.fill((0, 0, 0, 0))


    draw_board(screen)
    draw_selected_overlay(screen, uistate)
    draw_highlighted_overlay(screen, gamestate, uistate)
    draw_pieces(screen, gamestate)
    draw_promo_overlay(screen, gamestate)
    window.blit(screen, (0, 0))
    mate = get_mate(gamestate)
    pygame.display.flip()
    clock.tick(FPS)
    if mate != "":
        if mate == "d":
            print("Stalemate")
        if mate == "w":
            print("Black Wins!")
        if mate == 'b':
            print("White Wins!")
        pygame.time.wait(5000)
        run = False
pygame.quit()
sys.exit()