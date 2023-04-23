import pygame
from classes import Pokemon, Engine, PokemonTrainer, waitPress
from random import randint
import csv
import os

# pygame setup
pygame.init()
font = pygame.font.SysFont("Arial", 20)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True


Pokemon.sprite_sheet = pygame.image.load("./pokemon.png").convert()
Pokemon.status_img = pygame.image.load("./status.png").convert()

win_num = 0
total = 0
def add_dict_to_csv_rows(data_dict, csv_rows, created_file):
    max_len = max([len(value) if isinstance(value, list) else 1 for value in data_dict.values()])
    header_row = ["turn_num", *list(data_dict.keys())]

    if not created_file:
        if not csv_rows:  # If csv_rows is empty, add header row
            csv_rows.append(header_row)
        elif header_row != csv_rows[0]:  # Check if the headers are the same, if not, raise an exception
            raise ValueError("The dictionaries have different keys, cannot merge into a single CSV file.")

    for i in range(max_len):
        data_row = [f"turn{i+1}"]
        for key in data_dict:
            value = data_dict[key]
            if isinstance(value, list):
                data_row.append(value[i] if i < len(value) else '')
            else:
                data_row.append(value)

        csv_rows.append(data_row)

store_path = '/Users/zch/Downloads/train_data_output.csv'
created_file = os.path.exists(store_path)

for i in range(100):
    # pygame setup
    try:
        total += 1
        pygame.init()
        font = pygame.font.SysFont("Arial", 20)
        screen = pygame.display.set_mode((1280, 720))
        clock = pygame.time.Clock()
        running = True

        Pokemon.sprite_sheet = pygame.image.load("./pokemon.png").convert()
        Pokemon.status_img = pygame.image.load("./status.png").convert()
        game_won = False

        team1 = [Pokemon(6)]
        trainer1 = PokemonTrainer("trainer1", team=team1)
        team2 = [Pokemon(randint(1,151))]
        trainer2 = PokemonTrainer("trainer2", team=team2)

        engine = Engine(screen, font, trainer1, trainer2)
        Engine.pokeball_img = pygame.transform.scale(pygame.image.load("./pokeball.png").convert(), (50,50))
        Engine.pokeballfaint_img = pygame.transform.scale(pygame.image.load("./pokeball_faint.png").convert(), (50,50))

        engine.init_render()
        init_seq = False

        engine.GAME_RECORD["my_type1"] = team1[0].type1
        engine.GAME_RECORD["my_type2"] = team1[0].type2
        engine.GAME_RECORD["op_type1"] = team2[0].type1
        engine.GAME_RECORD["op_type2"] = team2[0].type2

        while running:
            pygame.display.flip()
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if game_won:
                break

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
        # print(engine.GAME_RECORD)
        if engine.GAME_RECORD["win"]:
            win_num += 1
    #     if True:
    #
    #         csv_rows = []
    #         add_dict_to_csv_rows(engine.GAME_RECORD, csv_rows, created_file)
    #         created_file = True
    #         with open(store_path, 'a', newline='', encoding='utf-8') as csvfile:
    #             csv_writer = csv.writer(csvfile)
    #             csv_writer.writerows(csv_rows)
        print(i, win_num/total)
    except:
        pass


pygame.quit()



