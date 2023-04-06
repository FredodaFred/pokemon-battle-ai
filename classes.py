import pygame
from random import randint, choice
from data import pokemon_dict, moves, type_modifier, move_sets, Turn, Status
from pygame.locals import *
from time import sleep
pygame.init()

SPRITE_ROWS = 28
SPRIT_COLS = 6
SPRITE_WIDTH = SPRITE_HEIGHT = 80


def waitPress():
    '''
        Waits for user to hit enter to continue with game
        Returns - if key is pressed or not
    '''
    pressed = False
    while not pressed:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            pressed=  True
        elif event.type == pygame.QUIT:
            exit(0)
    
class Pokemon:
    sprite_sheet = None

    def __init__(self, pokemon_id):
        assert pokemon_id <= 151, "Invalid Pokemon ID"
        self.id = pokemon_id
        self.name = pokemon_dict[f'{pokemon_id}']["Name"]
        self.type1 = pokemon_dict[f'{pokemon_id}']["Type 1"]
        self.type2 = pokemon_dict[f'{pokemon_id}']["Type 2"]
        self.image = None
        self.damage_taken = 0  

        '''  HOW TO CALCULATE EACH STAT. EACH POKEMON WLL BE LEVEL 50 FOR PURPOSES
            https://pokemon.fandom.com/wiki/Statistics

            HP = floor(0.01 x (2 x Base + IV + floor(0.25 x EV)) x Level) + Level + 10
            Other Stats = (floor(0.01 x (2 x Base + IV + floor(0.25 x EV)) x Level) + 5) x Nature

            Let's modify this to make it more simple... (remove EV, IV, Nature), and hold level constant
            Note that 0.01*2*50 is 1

            HP = base_state + 50 + 10
            STAT = base_stat + 5
        '''

        self.hp = pokemon_dict[f'{pokemon_id}']["HP"]  + 60
        self.attack = pokemon_dict[f'{pokemon_id}']["Attack"] * 50 + 5
        self.defense = pokemon_dict[f'{pokemon_id}']["Defense"] * 50 + 5
        self.special_attack = pokemon_dict[f'{pokemon_id}']["Sp. Atk"] * 50 + 5
        self.special_defense = pokemon_dict[f'{pokemon_id}']["Sp. Def"] * 50 + 5
        self.speed = pokemon_dict[f'{pokemon_id}']["Speed"] * 50 + 5

        self.moves = []
        for move in move_sets[pokemon_id]:
            if not move == '':
                self.moves.append(moves[f'{move}'])

        self.status = Status.no_status

        
    def load_sprite(self, screen, x_loc, y_loc, flip = False):
        x = 80*((self.id-1) % 28)
        y = 80*((self.id-1) //28)
        # Extract portion of spritesheet as a sprite
        sprite_rect = pygame.Rect(x, y, SPRITE_WIDTH, SPRITE_HEIGHT)  # define rectangle of sprite on spritesheet
        sprite_image = Pokemon.sprite_sheet.subsurface(sprite_rect)  # extract portion of spritesheet as a sprite
        sprite_image = pygame.transform.scale(sprite_image, (80*5, 80*5))
        if flip:
            sprite_image = pygame.transform.flip(sprite_image, True, False)
        self.image = sprite_image
        screen.blit(self.image, (x_loc, y_loc))

    def match_type(pokemon_type):
        if pokemon_type == "Normal":
            return 0
        elif pokemon_type == "Fire":
            return 1
        elif pokemon_type == "Water":
            return 2
        elif pokemon_type == "Electric":
            return 3
        elif pokemon_type == "Grass":
            return 4
        elif pokemon_type == "Ice":
            return 5
        elif pokemon_type == "Fighting":
            return 6
        elif pokemon_type == "Poison":
            return 7
        elif pokemon_type == "Ground":
            return 8
        elif pokemon_type == "Flying":
            return 9
        elif pokemon_type == "Psychic":
            return 10
        elif pokemon_type == "Bug":
            return 11
        elif pokemon_type == "Rock":
            return 12
        elif pokemon_type == "Ghost":
            return 13
        return 14

    def compute_atk_damage(self, move, otherPokemon):
        ''' 
        DAMAGE FORMULA FROM GENERATION 1
        https://bulbapedia.bulbagarden.net/wiki/Damage

         damage = (((((1/5)*( 2 * level * critical)+2)*attack_power*(pokemon_attack)/(other_pokemon defense))/50 ))*(same_type_attack_bonus)*(attack adv on oppponet type1))*(attack adv on oppponet type2)*(randunif(217, 255)/255  )
         We will simplify this with no crits (critical == 1)

        '''
        assert type(otherPokemon) == Pokemon, "otherPokemon incorrect type"

        move_data = move
        power = int(move_data["Power"]) 
        pokemon_atk = self.attack if move_data["Category"] == "Physical" else self.special_attack
        other_def = otherPokemon.defense if move_data["Category"] == "Physical" else otherPokemon.special_defense
        STAB = 1.5 if move_data["Type"] == self.type1 or move_data["Type"] == self.type2 else 1
        type_1_bonus = type_modifier[Pokemon.match_type(move_data["Type"])][Pokemon.match_type(otherPokemon.type1)]
        type_2_bonus = type_modifier[Pokemon.match_type(move_data["Type"])][Pokemon.match_type(otherPokemon.type2)]
        random = randint(217, 255) / 255

        damage = ((((22*power*(pokemon_atk/other_def))/50)+2)*STAB*type_1_bonus*type_2_bonus*random ) // 1

        # accuracy = int(move_data["Accuracy"])
        # miss_or_hit = 0 if randint(1, 100) > accuracy else 1
        return damage

    def handle_status_effect(self):
        pass

    def draw_health_bar(self, screen, x, y):
        percent = self.damage_taken/self.hp
        pygame.draw.rect(screen, (0,128,0), (x, y, 250*(1-percent), 10) )
        pygame.draw.rect(screen, (255,0,0), (x + 250*(1-percent), y, 250*percent, 10))


    def attack_t(self, move, otherPokemon): 
        if move["Category"] == "Status":
            return    
        damage = self.compute_atk_damage(move, otherPokemon)
        otherPokemon.damage_taken += damage
        return damage

    def __eq__(self, other):
        return self.name == other.name

class PokemonTrainer():

    def __init__(self, name, team=[]):
        '''
            Arguments
            name: string
            team: list (optional)
        '''
        self.name = name
        self.team = team
    
    def add_pokemon(self, pokemon):
        self.team.append(pokemon)

    def active_pokemon(self):
        return self.team[0]

    def swap_pokemon(self, pokemon):
        self.team[0], self.team[self.team.index(pokemon)] = self.team[self.team.index(pokemon)], self.team[0]

    def choose_attack(self):
        return choice(self.active_pokemon().moves)
    
    def num_pokemon(self):
        return len(self.team)



class Engine():
    pokeball_img = None
    def __init__(self, screen, font, trainer1, trainer2):
        self.screen = screen
        self.font = font
        self.trainer1 = trainer1
        self.trainer2 = trainer2
        self.turn = Turn.main_turn

    def init_render(self):
        self.render_text(f"{self.trainer1.name} versus {self.trainer2.name}", refresh=True)
        self.render_text(f"Click Enter to continue...", y_offset= 20)

        for i in range(len(self.trainer1.team)):
            self.screen.blit(Engine.pokeball_img, (50, 100+i*75))

        for i in range(len(self.trainer2.team)):
            self.screen.blit(Engine.pokeball_img, (1200, 100+i*75))


    def render_movesets(self, pokemon, x):
        for i, move in enumerate(pokemon.moves):
            name = move["Name"]
            txtsurf = self.font.render( f'{name}', True, (0,0,0))
            self.screen.blit(txtsurf, (x, 620 + i*20, 400, 400))
            #190 820


    def render_text(self, text, y_offset = 0, refresh = False):
        #Refresh log box
        if refresh:
            pygame.draw.rect(self.screen, (255, 255, 255), (400, 620, 500, 300))
        txtsurf = self.font.render( text, True, (0,0,0))
        self.screen.blit(txtsurf, (500, 650 + y_offset, 400, 400))

    def run_turn(self):
        '''
            Returns:
                gameWon: boolean - signifies if game has been won on the turn or not
        '''
        pass
