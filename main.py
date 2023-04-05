import pygame
from classes import Pokemon, Engine
from time import sleep



# pygame setup
pygame.init()
font = pygame.font.SysFont("Arial", 20)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

Pokemon.sprite_sheet = pygame.image.load("./pokemon.png").convert()


game_won = False
main = Pokemon(1)
opponent = Pokemon(2)

engine = Engine(screen, font, main, opponent)
engine.init_render()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_won:
        continue

    game_won = engine.run_turn()
    pygame.display.flip()
    sleep(1) 
    clock.tick(20)  # limits FPS to 20


pygame.quit()
