import pygame
from classes import Pokemon, Engine, PokemonTrainer, waitPress
from random import randint
import csv

# pygame setup


win_num = 0

def write_battle_to_csv(data_dict, csv_writer_inst):
    csv_rows = []
    max_len = max([len(value) if isinstance(value, list) else 1 for value in data_dict.values()])

    for i in range(max_len):
        data_row = [f"turn{i+1}"]
        for key in data_dict:
            value = data_dict[key]
            if isinstance(value, list):
                data_row.append(value[i] if i < len(value) else '')
            else:
                data_row.append(value)

        csv_rows.append(data_row)
    csv_writer_inst.writerows(csv_rows)
        
##data collection
empty_file = True
file = open('./charizard_battle_data.csv', "w")
header_row = ['turn_num', 'op_name', 'my_hp', 'op_hp', 'my_type1', 'my_type2', 'op_type1', 'op_type2', 'my_status', 'op_status', 'my_speed', 'win']
csv_writer = csv.writer(file)
csv_writer.writerow(header_row)

for i in range(100):
    pygame.init()
    font = pygame.font.SysFont("Arial", 20)
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True


    Pokemon.sprite_sheet = pygame.image.load("./pokemon.png").convert()
    Pokemon.status_img = pygame.image.load("./status.png").convert()
    game_record = []
    team1 = [Pokemon(6)]
    trainer1 = PokemonTrainer("trainer1", team=team1)
    team2 = [Pokemon(randint(1,151))]
    trainer2 = PokemonTrainer("trainer2", team=team2)

    engine = Engine(screen, font, trainer1, trainer2)
    Engine.pokeball_img = pygame.transform.scale(pygame.image.load("./pokeball.png").convert(), (50,50))
    Engine.pokeballfaint_img = pygame.transform.scale(pygame.image.load("./pokeball_faint.png").convert(), (50,50))


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
            write_battle_to_csv(data, csv_writer)
    
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
file.close()

pygame.quit()
