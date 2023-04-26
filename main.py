import pygame
from classes import Pokemon, Engine, PokemonTrainer, waitPress
from random import randint

import warnings
warnings.filterwarnings("ignore")
# pygame setup


######################################################################

# model_path = "./models/pokemon_decision_tree_d5.pkl"
# model_path = "./models/RL_model3.h5"
model_path = None

######################################################################

win_num = 0
total_num_battle = 0

for i in range(10):
    pygame.init()
    font = pygame.font.SysFont("Arial", 20)
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True


    Pokemon.sprite_sheet = pygame.image.load("./pokemon.png").convert()
    Pokemon.status_img = pygame.image.load("./status.png").convert()
    game_record = []
    team1 = [Pokemon(5, ai_strategy="dt")] # ai_strategy choose from ["rl", "dt", "rbes", "random"]
    trainer1 = PokemonTrainer("trainer1", team=team1)
    team2 = [Pokemon(randint(1,151), ai_strategy="rbes")]
    trainer2 = PokemonTrainer("trainer2", team=team2)

    engine = Engine(screen, font, trainer1, trainer2)
    Engine.pokeball_img = pygame.transform.scale(pygame.image.load("./pokeball.png").convert(), (50,50))
    Engine.pokeballfaint_img = pygame.transform.scale(pygame.image.load("./pokeball_faint.png").convert(), (50,50))

    total_num_battle += 1
    engine.init_render()
    game_won = False
    init_seq = False
    while running:
        pygame.display.flip()
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if game_won:
            data = engine.GAME_RECORD
            if data["win"]:
                win_num += 1
            running = False
        
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
        

        game_won = engine.run_turn()
        clock.tick(20)  # limits FPS to 20
    print(f"{i+1} : {100 * win_num / total_num_battle:.2f}%")


pygame.quit()
