import pygame
import sys
import time
from helper import SIZE, FPS
from board import draw_board, draw_pieces, get_event, draw_selected_overlay, draw_highlighted_overlay, get_mate, draw_promo_overlay
pygame.init()
print("Please pay attention to this Terminal window as input for pawn promotion will begin here")
for i in range(3, 0, -1):
    print(i)
    time.sleep(1)

print("Enjoy!")



window = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Chess(not that great)")
screen = pygame.Surface(SIZE, pygame.SRCALPHA)
clock = pygame.time.Clock()

run = True

while run:
    click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        else:
            get_event(event)


    screen.fill((0, 0, 0, 0))


    draw_board(screen)
    draw_selected_overlay(screen)
    draw_highlighted_overlay(screen)
    draw_pieces(screen)
    draw_promo_overlay(screen)
    window.blit(screen, (0, 0))
    mate = get_mate()
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