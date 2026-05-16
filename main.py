import pygame
import sys
from settings import SIZE, FPS

pygame.init()

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

run = True
print(type(screen))
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    
    clock.tick(FPS)
pygame.quit()
sys.exit()