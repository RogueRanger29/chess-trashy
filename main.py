import pygame
import sys
import time
from helper import SIZE, FPS
from board import draw_board, draw_pieces, set_click_state, move, draw_selected_overlay, draw_highlighted_overlay, get_mate


print("Enjoy!")

pygame.init()

window = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Chess(not that great)")
screen = pygame.Surface(SIZE, pygame.SRCALPHA)
clock = pygame.time.Clock()

# bring window to front (pygame)
import ctypes
u32 = ctypes.WinDLL("user32")
kernel = ctypes.WinDLL("kernel32")
window_handlery = pygame.display.get_wm_info()["window"]
try:
    u32.ShowWindow(window_handlery, 9)
    u32.SetForegroundWindow(window_handlery)
    u32.SetWindowPos(window_handlery, -1, 0,0,0,0, 0x0002|0x0001)
except:
    print("no pygame window handle found.")


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