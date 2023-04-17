import pygame
from classes import Pokemon, Engine, PokemonTrainer, waitPress

# pygame setup
pygame.init()
font = pygame.font.SysFont("Arial", 20)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True


Pokemon.sprite_sheet = pygame.image.load("./pokemon.png").convert()
Pokemon.status_img = pygame.image.load("./status.png").convert()


game_won = False
team1 = [Pokemon(6), Pokemon(10), Pokemon(57)]
trainer1 = PokemonTrainer("Ash", team=team1)
team2 = [Pokemon(41), Pokemon(73), Pokemon(66)]
trainer2 = PokemonTrainer("Misty", team=team2)

engine = Engine(screen, font, trainer1, trainer2)
Engine.pokeball_img = pygame.transform.scale(pygame.image.load("./pokeball.png").convert(), (50,50))
Engine.pokeballfaint_img = pygame.transform.scale(pygame.image.load("./pokeball_faint.png").convert(), (50,50))

engine.init_render()

init_seq = False
while running:
    pygame.display.flip()
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_won:
        continue
    
    if not init_seq:
        #inital sequence
        waitPress()
        engine.render_text(f"{trainer1.name} sent out {trainer1.active_pokemon().name}", refresh=True)
        trainer1.active_pokemon().load_sprite(screen, 0, 250, flip = True)


        pygame.display.flip()
        waitPress()
        engine.render_text(f"{trainer2.name} sent out {trainer2.active_pokemon().name}", refresh=True)
        trainer2.active_pokemon().load_sprite(screen, 900, 250, flip = False)
    
        init_seq = True
    

    engine.run_turn()


    clock.tick(20)  # limits FPS to 20


pygame.quit()
