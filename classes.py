import pygame
from random import randint, choice, choices
from data import pokemon_dict, moves, type_modifier, move_sets, stage_modifier, Status, match_type
from pygame.locals import *
from InferenceEngine import InferenceEngine
from time import sleep
import csv
import numpy as np

pygame.init()

SPRITE_ROWS = 28
SPRIT_COLS = 6
SPRITE_WIDTH = SPRITE_HEIGHT = 80

inference_engine = InferenceEngine()

def waitPress():
    '''
        Waits for user to hit enter to continue with game
        Returns - if key is pressed or not
    '''
    pressed = True
    while not pressed:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            pressed=  True
        elif event.type == pygame.QUIT:
            exit(0)
    
class Pokemon:
    sprite_sheet = None
    status_img = None

    def __init__(self, pokemon_id):
        assert pokemon_id <= 151, "Invalid Pokemon ID"
        self.id = pokemon_id
        self.name  = pokemon_dict[f'{pokemon_id}']["Name"]
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
        self.status_counter = 0
        
        # attack, def, spatk, spdef, speed
        # https://www.dragonflycave.com/mechanics/stat-stages#:~:text=In%20particular%2C%20whenever%20you%20use,for%20each%20of%20its%20stats.
        self.stat_stages = [0,0,0,0,0]

        
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

    def draw_health_bar(self, screen, x, y):
        percent = self.damage_taken/self.hp
        if percent > 1:
            percent = 1
        #green part
        pygame.draw.rect(screen, (0,128,0), (x, y, 250*(1-percent), 10) )
        #damage part
        pygame.draw.rect(screen, (255,0,0), (x + 250*(1-percent), y, 250*percent, 10))   

    def render_status_symbol(self, screen, x_loc, y_loc):
        status = self.status
        if status == Status.no_status:
            pygame.draw.rect(screen, (0,0,0), (x_loc, y_loc, 65, 45))
            return 

        y_offset = 0
        if status == Status.burn:
            y_offset = 0
        elif status == Status.frozen:
            y_offset = 55
        elif status == Status.sleep:
            y_offset = 105
        elif status == Status.confused:
            y_offset = 160
        elif status == Status.paralyzed:
            y_offset = 210
        elif status == Status.poison:
            y_offset = 265

        sprite_rect = pygame.Rect(0, y_offset, 65, 45)
        symbol_img = Pokemon.status_img.subsurface(sprite_rect)
        symbol_img = pygame.transform.scale(symbol_img, (50, 30))
        screen.blit(symbol_img, (x_loc, y_loc))


    
    def apply_status_damage(self, otherPokemon, render_text):
        if self.status == Status.burn:
            self.damage_taken += self.hp//16
            render_text(f"{self.name} is hurt by burn",refresh=True)
            waitPress()
        elif self.status == Status.poison:
            self.damage_taken += self.hp//16
            render_text(f"{self.name} is hurt by poison",refresh=True)
            waitPress()
        elif self.status == Status.leech_seed:
            self.damage_taken -= self.hp//16
            otherPokemon.damage_taken += self.hp//16
            render_text(f"{otherPokemon.name} is being drained with leech seed",refresh=True)
            waitPress()
        elif self.status == Status.sleep or self.status == Status.confused:
            self.status_counter -= 1
            if self.status_counter == 0:
                self.status = Status.no_status
                render_text(f"{self.name} woke up",refresh=True)
                waitPress()
        elif self.status == Status.frozen:
            self.status = choices([Status.frozen, Status.no_status], [90, 10])[0]
            if self.status == Status.no_status:
                render_text(f"{self.name} thawed out",refresh=True)
                waitPress()             
        
    
    def apply_secondary_effect(self, move, otherPokemon, damage):
        #absorbing moves
        if move['Name'] in ['Absorb', 'Mega Drain', 'Leech Life']:
            #Case for going over maximum HP.
            if self.damage_taken - damage // 2 < 0:
                self.damage_taken = 0
            else:
                self.damage_taken -= damage // 2
        #moves hitting multiple times
        elif move['Name'] == 'Double Slap':
            strikes = choices([2,3,4,5], weights=[35,35, 15,15])
            damage *= strikes[0]
        elif move['Name'] in ['Comet Punch', 'Fury Attack', 'Pin Missile', 'Barrage']:
            strikes = choices([2,3,4,5], weights=[37.5, 37.5, 12.5, 12.5]) 
            damage *= strikes[0]
        elif move['Name'] == 'Double Kick':
             damage *= 2
        elif move['Name'] == 'Twineedle':
            damage *= 2
            if otherPokemon.status == Status.no_status:
                status = choices([Status.poison, Status.no_status], [20, 80])
                otherPokemon.status = status[0]
        #Moves with status effects
        elif move['Name'] in ['Fire Punch', 'Ember', 'Flamethrower']:
            '''10% chance to burn'''
            if otherPokemon.status == Status.no_status:
                status = choices([Status.burn, Status.no_status], [10, 90])
                otherPokemon.status = status[0]
        elif move['Name'] in ['Ice Punch', 'Ice Beam', 'Blizzard']:
             if otherPokemon.status == Status.no_status:
                status = choices([Status.frozen, Status.no_status], [10, 90]) 
                otherPokemon.status = status[0]
        elif move['Name'] in ['Psybeam']:
            if otherPokemon.status == Status.no_status:
                status = choices([Status.confused, Status.no_status], [10, 90])
                otherPokemon.status = status[0]
        elif move['Name'] == 'Thunder Punch':
            if otherPokemon.status == Status.no_status:
                status = choices([Status.paralyzed, Status.no_status], [10, 90])  
                otherPokemon.status = status[0]
        elif move['Name'] == 'Body Slam':
            if otherPokemon.status == Status.no_status and not match_type(otherPokemon.type1) == 0 and not match_type(otherPokemon.type1) == 0:
                 status = choices([Status.paralyzed, Status.no_status], [30, 70]) 
                 otherPokemon.status = status[0]
        elif move['Name'] == 'Poison Sting':
            if otherPokemon.status == Status.no_status:
                status = choices([Status.poison, Status.no_status], [20, 80])
                otherPokemon.status = status[0]
        elif move['Name'] == "Acid":
            hit = choices([0,1], [66.8, 33.2])
            otherPokemon.defense -= 5*hit[0]
        #recoil moves
        elif move['Name'] in ['Take Down', 'Double Edge', 'Submission']:
            self.damage_taken += (damage*0.25)//1

        return damage

    def compute_atk_damage(self, move, otherPokemon):
        
        ''' 
            move: dict() - Example: {'Name': 'Slash', 'Type': 'Normal', 'Category': 'Physical', 'PP': 20, 'Power': '70', 'Accuracy': '100'}
        DAMAGE FORMULA FROM GENERATION 1
        https://bulbapedia.bulbagarden.net/wiki/Damage

         damage = (((((1/5)*( 2 * level * critical)+2)*attack_power*(pokemon_attack)/(other_pokemon defense))/50 ))*(same_type_attack_bonus)*(attack adv on oppponet type1))*(attack adv on oppponet type2)*(randunif(217, 255)/255  )
         We will simplify this with no crits (critical == 1)

        '''
        assert type(otherPokemon) == Pokemon, "otherPokemon incorrect type"

        #unique cases...
        if move['Name'] == 'Dragon Rage':
            return 40
        elif move['Name'] == "Super Fang":
            return otherPokemon.hp // 2
        elif move['Name'] in ['Guillotine', 'Horn Drill', 'Fissure']:
            #only hits 35% of time
            hit = choices([0,1], [70, 30])
            return 65535*hit[0]
        elif move['Name'] == "Sonic Boom":
            return 20
        elif move['Name'] == 'Seismic Toss':
            return 50
        elif move['Name'] == 'Psywave':
            return randint(1, 75)
        elif move['Name'] == "Night Shade":
            return 50
        
        
        move_data = move
        power = int(move_data["Power"]) 
        #attack, def, spatk, spdef, speed
        pokemon_atk = self.attack*(stage_modifier[self.stat_stages[0]]) if move_data["Category"] == "Physical" else self.special_attack*(stage_modifier[self.stat_stages[2]])
        other_def = otherPokemon.defense*(stage_modifier[otherPokemon.stat_stages[1]]) if move_data["Category"] == "Physical" else otherPokemon.special_defense*(stage_modifier[otherPokemon.stat_stages[3]])
        STAB = 1.5 if move_data["Type"] == self.type1 or move_data["Type"] == self.type2 else 1
        type_1_bonus = type_modifier[match_type(move_data["Type"])][match_type(otherPokemon.type1)]
        type_2_bonus = type_modifier[match_type(move_data["Type"])][match_type(otherPokemon.type2)]
        random = randint(217, 255) / 255

        damage = ((((22*power*(pokemon_atk/other_def))/50)+2)*STAB*type_1_bonus*type_2_bonus*random ) // 1

        #Moves with secondary effects
        damage = self.apply_secondary_effect(move, otherPokemon, damage)
        # accuracy = int(move_data["Accuracy"])
        # miss_or_hit = 0 if randint(1, 100) > accuracy else 1
        return damage

    def status_attack(self, move, otherPokemon):
        #useless moves
        if move['Name'] in ['Splash', 'Teleport']:
            self.render_text(f'{self.name} did nothing', refresh=True)
            pygame.display.flip()
            waitPress()
            return    
        
        #can't effect other pokemon
        type_1_bonus = type_modifier[match_type(move["Type"])][match_type(otherPokemon.type1)]
        type_2_bonus = type_modifier[match_type(move["Type"])][match_type(otherPokemon.type2)]
        if type_1_bonus == 0 or type_2_bonus == 0:
            return
            
        #Direct status changers

        if otherPokemon.status == Status.no_status:
            status_changed_flag = False
            if move['Name'] in ['Sleep Powder', 'Sing', 'Hypnosis', 'Spore']:
                status_changed_flag = True
                otherPokemon.status = Status.sleep
                otherPokemon.status_counter = randint(2,6)
                self.render_text(f'{otherPokemon.name} was put to sleep', refresh=True)
            elif move['Name'] in ['Poison Powder', 'Toxic', 'Poison Gas']:
                status_changed_flag = True
                otherPokemon.status = Status.poison
                self.render_text(f'{otherPokemon.name} was poisoned', refresh=True)
            elif move['Name'] in ['Stun Spore', 'Glare', 'Thunder Wave']:
                status_changed_flag = True
                self.render_text(f'{otherPokemon.name} became paralyzed', refresh=True)         
                otherPokemon.status = Status.paralyzed          
            elif move['Name'] in ['Supersonic', 'Confuse Ray']:
                status_changed_flag = True
                self.render_text(f'{otherPokemon.name} became confused', refresh=True)           
                otherPokemon.status = Status.confused
            elif move['Name'] == 'Leech Seed':
                 status_changed_flag = True
                 self.render_text(f'{otherPokemon.name} was seeded', refresh=True)           
                 otherPokemon.status = Status.leech_seed               

            if status_changed_flag:
                pygame.display.flip()
                waitPress()
                return        
            
            
        #Self healers
        if move['Name'] in ['Recover', 'Soft Boiled']:
            self.damage_taken -= (self.hp // 2) if self.damage_taken -(self.hp // 2) >= 0 else 0
            return
        elif move['Name'] == 'Rest':
            self.damage_taken = 0
            self.status = Status.sleep
            self.status_counter = 2
            return

        #attack, def, spatk, spdef, speed
        if move['Name'] in ['Harden', 'Defense Curl', 'Withdraw']:
            self.render_text(f'{self.name} raised its defense', refresh=True)
            pygame.display.flip()
            waitPress()
            self.stat_stages[1] =  self.stat_stages[1] + 1 if self.stat_stages[1] < 6 else 6
        elif move['Name'] in ['Growl']:
            self.render_text(f'{otherPokemon.name} lost attack power', refresh=True)
            pygame.display.flip()
            waitPress()            
            otherPokemon.stat_stages[0] = self.stat_stages[0] - 1 if self.stat_stages[0] > -6 else -6
        elif move['Name'] in ['Tail Whip', 'Leer']:
            self.render_text(f'{otherPokemon.name} lost defense', refresh=True)
            pygame.display.flip()
            waitPress()            
            otherPokemon.stat_stages[1] = self.stat_stages[1] - 1 if self.stat_stages[1] > -6 else -6            
        elif move['Name'] in ['Agility']:
            self.render_text(f'{self.name} raised its speed', refresh=True)
            pygame.display.flip()
            waitPress()               
            self.stat_stages[4] =  self.stat_stages[4] + 1 if self.stat_stages[4] < 6 else 6
        elif move['Name'] == 'Amnesia':
            self.render_text(f'{self.name} raised its spdef', refresh=True)
            pygame.display.flip()
            waitPress()               
            self.stat_stages[3] = self.stat_stages[3] + 2 if self.stat_stages[3] < 5 else 6
        elif move['Name'] in ['String Shot']:
            self.render_text(f'{otherPokemon.name} lost speed', refresh=True)
            pygame.display.flip()
            waitPress()              
            otherPokemon.stat_stages[4] =  otherPokemon.stat_stages[4] - 1 if otherPokemon.stat_stages[4] > -6 else -6
        elif move['Name'] in ['Sharpen', 'Meditate']:
            self.render_text(f'{self.name} raised its attack', refresh=True)
            pygame.display.flip()
            waitPress()              
            self.stat_stages[0] = self.stat_stages[0] + 1 if self.stat_stages[0] < 6 else 6
        elif move['Name'] in ['Growth']:
            self.render_text(f'{self.name} raised its special attack', refresh=True)
            pygame.display.flip()
            waitPress()              
            self.stat_stages[2] = self.stat_stages[2] + 1 if self.stat_stages[2] < 6 else 6
        elif move['Name'] == 'Swords Dance':
            self.render_text(f'{self.name} raised its attack', refresh=True)
            pygame.display.flip()
            waitPress()             
            self.stat_stages[0] = self.stat_stages[0] + 2 if self.stat_stages[0] < 5 else 6
        elif move['Name'] == 'Acid Armor':
            self.render_text(f'{self.name} raised its defense', refresh=True)
            pygame.display.flip()
            waitPress()             
            self.stat_stages[1] = self.stat_stages[1] + 2 if self.stat_stages[1] < 5 else 6       

    def attack_t(self, move, otherPokemon):
        #Check the moves stack here 
        if move["Category"] == "Status":
            self.status_attack(move, otherPokemon) 
            return
        damage = self.compute_atk_damage(move, otherPokemon)
        otherPokemon.damage_taken += damage
        return damage

    def give_render_text(self, render_text_func):
        self.render_text = render_text_func

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
        self.fainted = [] #stores fainted pokemon
        
    
    def add_pokemon(self, pokemon):
        self.team.append(pokemon)

    def active_pokemon(self):
        return self.team[0]

    def swap_pokemon(self, pokemon):
        self.team[0], self.team[self.team.index(pokemon)] = self.team[self.team.index(pokemon)], self.team[0]

    def choose_attack(self):
        move = choice(self.active_pokemon().moves)
        return move
    
    def num_pokemon(self):
        return len(self.team)

    def num_fainted(self):
        return len(self.fainted)


check_faint = lambda pokemon : True if pokemon.damage_taken >= pokemon.hp else False
class Engine():
    pokeball_img = None
    pokeballfaint_img = None

    def __init__(self, screen, font, trainer1, trainer2):
        self.screen = screen
        self.font = font
        self.trainer1 = trainer1
        self.trainer2 = trainer2
        self.turn_num = 0

        atk_pk = self.trainer1.active_pokemon()
        op_pk = self.trainer2.active_pokemon()

        self.GAME_RECORD = { "move_name" : [],
                                "op_name" : op_pk.name,
                                "my_hp" : [],
                                "op_hp" : [],
                                "my_type1" : atk_pk.type1,
                                "my_type2":  atk_pk.type2,
                                "op_type1" : op_pk.type1,
                                "op_type2":  op_pk.type2,
                                "my_status" : [],
                                "op_status" : [],
                                "my_speed" : [],
                                "op_speed" : [],
                                "win" : False } # train1 wins?
        
        self.type_to_index =  {"Grass": 0,
                                'Bug': 1,
                                'Ground': 2,
                                'Poison': 3,
                                'Dragon': 4,
                                'Normal': 5,
                                'Fire': 6,
                                'Rock': 7,
                                'Ice': 8,
                                'Fighting': 9,
                                'Water': 10,
                                'Ghost': 11,
                                'Electric': 12,
                                'Psychic': 13}
        
        self.index_to_move =  {"charizard" : {0: "Dragon Rage", 1: "Slash", 2: "Leer", 3: "Flamethrower"}}

    def init_render(self):
        self.render_text(f"{self.trainer1.name} versus {self.trainer2.name}", refresh=True)
        self.render_text(f"Click Enter to continue...", y_offset= 20)

        for i in range(len(self.trainer1.team)):
            self.screen.blit(Engine.pokeball_img, (50, 50+i*75))

        for i in range(len(self.trainer2.team)):
            self.screen.blit(Engine.pokeball_img, (1200, 50+i*75))


    # def render_movesets(self, pokemon, x):
    #     for i, move in enumerate(pokemon.moves):
    #         name = move["Name"]
    #         txtsurf = self.font.render( f'{name}', True, (0,0,0))
    #         self.screen.blit(txtsurf, (x, 620 + i*20, 400, 400))
    #         #190 820


    def render_text(self, text, y_offset = 0, refresh = False):
        #Refresh log box
        if refresh:
            pygame.draw.rect(self.screen, (255, 255, 255), (400, 620, 500, 300))
        txtsurf = self.font.render( text, True, (0,0,0))
        self.screen.blit(txtsurf, (500, 650 + y_offset, 400, 400))

    def handle_faint(self, side):
        '''
            Arguments
            trainer - pokemon trainer whos pokemon has fainted, can be trainer 1 or 2 ['1', '2']
        '''
        if side == '1':
            if self.trainer1.num_pokemon() == 1:
                self.trainer1.team.pop(0)
                return
            fainted_pokemon = self.trainer1.active_pokemon()
            #pop the first pokemon and add it to the list of fainted pokemon
            self.trainer1.fainted.append(self.trainer1.team.pop(0))
            self.render_text(f"{fainted_pokemon.name} fainted!", refresh=True)

            for i in range(len(self.trainer1.fainted)):
                self.screen.blit(Engine.pokeballfaint_img, (50, 50+i*75))
            pygame.display.flip()
            waitPress()

            #release new pokemon to screen

            self.render_text(f"{self.trainer1.name} sent out {self.trainer1.active_pokemon().name}", refresh=True)

            #refresh the spot where it fainted
            pygame.draw.rect(self.screen, (0, 0, 0), (0, 250, 80*5, 80*5))
            pygame.display.flip()
            self.trainer1.active_pokemon().load_sprite(self.screen, 0, 250, flip = True)
        else:
            if self.trainer2.num_pokemon() == 1:
                self.trainer2.team.pop(0)
                return
            fainted_pokemon = self.trainer2.active_pokemon()
            #pop the first pokemon and add it to the list of fainted pokemon
            self.trainer2.fainted.append(self.trainer2.team.pop(0))
            self.render_text(f"{fainted_pokemon.name} fainted!", refresh=True)

            for i in range(len(self.trainer2.fainted)):
                self.screen.blit(Engine.pokeballfaint_img, (1200, 50+i*75))

            pygame.display.flip()
            waitPress()

            self.render_text(f"{self.trainer2.name} sent out {self.trainer2.active_pokemon().name}", refresh=True)

            pygame.draw.rect(self.screen, (0, 0, 0), (900, 250, 80*5, 80*5))
            pygame.display.flip()
            self.trainer2.active_pokemon().load_sprite(self.screen, 900, 250, flip = False)

    
    def run_turn(self, strategy="random", model=None):
        '''
            Returns:
                gameWon: boolean - signifies if game has been won on the turn or not
        '''

        if self.trainer1.num_pokemon() == 0:
            self.render_text('Trainer 2 has won', refresh=True)
            return True
        elif self.trainer2.num_pokemon() == 0:
            self.render_text('Trainer 1 has won', refresh=True)
            self.GAME_RECORD['win'] = True
            return True

        t1_pokemon = self.trainer1.active_pokemon()
        t2_pokemon = self.trainer2.active_pokemon()
        
        #give access to text rendering
        t1_pokemon.give_render_text(self.render_text)
        t2_pokemon.give_render_text(self.render_text)

        pygame.draw.rect(self.screen, (0,0,0), (0, 600, 1240, 20))
        t1_pokemon.draw_health_bar(self.screen, 100, 600)
        t2_pokemon.draw_health_bar(self.screen, 1000, 600)
        t1_pokemon.render_status_symbol(self.screen, 100, 620)
        t2_pokemon.render_status_symbol(self.screen, 1000, 620)
        pygame.display.flip()

        at1 = self.trainer1.choose_attack()
        at2 = self.trainer2.choose_attack()

        #Check for quick attack, this always moves first
        priority1 = at1['Name'] == 'Quick Attack'
        priority2 = at2['Name'] == 'Quick Attack'

        self.GAME_RECORD['move_name'] = at1['Name']
        my_status = int(t1_pokemon.status)
        op_status = int(t2_pokemon.status)

        self.GAME_RECORD["my_speed"].append(t1_pokemon.speed)
        self.GAME_RECORD["op_speed"].append(t2_pokemon.speed)   


        if strategy.lower() == "rbes":
            at1 = inference_engine.move_recomendation(self.trainer1, t2_pokemon)
            if at1 == 'SWAP':
                self.trainer1.swap_pokemon()

        elif strategy.lower() != "random":

            my_hp = t1_pokemon.hp - t1_pokemon.damage_taken
            op_hp = t2_pokemon.hp - t2_pokemon.damage_taken
            input_data = [my_hp, op_hp, self.type_to_index[self.GAME_RECORD["op_type1"]], \
                    my_status, op_status, t2_pokemon.speed]

            if strategy.lower() == "dt":
                input_num = model.n_features_
                move_num = model.predict([input_data[:input_num]])[0]

            elif strategy.lower() == "rl":
                input_data = [*input_data[:5], t2_pokemon.attack, t2_pokemon.defense, t2_pokemon.special_attack, t2_pokemon.special_defense, t2_pokemon.speed]
                input_num = model.input_shape[1]
                state = np.reshape(input_data[:input_num], [1, input_num])
                q_values = model.predict(state, verbose=0)
                move_num = np.argmax(q_values[0])

            for move in t1_pokemon.moves:
                if move["Name"] == self.index_to_move[t1_pokemon.name.lower()][move_num]:
                    at1 = move
                    break

        waitPress()
        if not priority2 and (t1_pokemon.speed*(stage_modifier[t1_pokemon.stat_stages[4]]) > t2_pokemon.speed*(stage_modifier[t2_pokemon.stat_stages[4]])) or priority1 :

            if t1_pokemon.status == Status.sleep:
                self.render_text(f"{t1_pokemon.name} is asleep", refresh=True)
                pygame.display.flip()
                waitPress()
            elif t1_pokemon.status == Status.frozen:
                self.render_text(f"{t1_pokemon.name} is frozen", refresh=True)
                pygame.display.flip()
                waitPress()
            elif t1_pokemon.status == Status.confused:
                chance = randint(0,100)
                if chance > 50:
                     ##Use chosen move

                    self.render_text(f"{t1_pokemon.name} used { at1['Name'] } ", refresh=True)
                    pygame.display.flip()
                    waitPress()
                    t1_pokemon.attack_t(at1, t2_pokemon)
                    t2_pokemon.draw_health_bar(self.screen, 1000, 600)
                    pygame.display.flip()
                    waitPress()

                    ##Check for faint
                    if check_faint(t2_pokemon):
                        self.handle_faint('2')
                        pygame.display.flip()
                        self.GAME_RECORD["my_status"].append(my_status)
                        self.GAME_RECORD["op_status"].append(op_status)
                        my_hp = t1_pokemon.hp - t1_pokemon.damage_taken
                        op_hp = t2_pokemon.hp - t2_pokemon.damage_taken
                        self.GAME_RECORD["my_hp"].append(my_hp)
                        self.GAME_RECORD["op_hp"].append(op_hp)                        
                        return
                else:
                    confuse_attack = {"Name": "Pound", "Type": "Normal", "Category": "Physical","PP": 35, "Power": "40","Accuracy": "100"}
                    t1_pokemon.damage_taken += t1_pokemon.compute_atk_damage(confuse_attack, t1_pokemon)
                    t1_pokemon.draw_health_bar(self.screen, 100, 600)
                    self.render_text(f"{t1_pokemon.name} hurt itself in confusion", refresh=True)
                    pygame.display.flip()
                    waitPress()

            elif t1_pokemon.status == Status.paralyzed:
                chance = randint(0,100)
                if chance > 30:
                     ##Use chosen move
                    self.render_text(f"{t1_pokemon.name} used { at1['Name'] } ", refresh=True)
                    pygame.display.flip()
                    waitPress()
                    t1_pokemon.attack_t(at1, t2_pokemon)

                    t2_pokemon.draw_health_bar(self.screen, 1000, 600)
                    pygame.display.flip()
                    waitPress()

                    ##Check for faint
                    if check_faint(t2_pokemon):
                        self.handle_faint('2')
                        pygame.display.flip()
                        self.GAME_RECORD["my_status"].append(my_status)
                        self.GAME_RECORD["op_status"].append(op_status)
                        my_hp = t1_pokemon.hp - t1_pokemon.damage_taken
                        op_hp = t2_pokemon.hp - t2_pokemon.damage_taken
                        self.GAME_RECORD["my_hp"].append(my_hp)
                        self.GAME_RECORD["op_hp"].append(op_hp)                       
                        return
                else:
                    self.render_text(f"{t1_pokemon.name} is paralyzed", refresh=True)
                    pygame.display.flip()
                    waitPress()
            else:
                #Default sequence

                ##Use chosen move
                self.render_text(f"{t1_pokemon.name} used { at1['Name'] } ", refresh=True)
                pygame.display.flip()
                waitPress()
                t1_pokemon.attack_t(at1, t2_pokemon)
   
                t2_pokemon.draw_health_bar(self.screen, 1000, 600)
                t1_pokemon.render_status_symbol(self.screen, 100, 620)
                t2_pokemon.render_status_symbol(self.screen, 1000, 620)
                pygame.display.flip()
                waitPress()

                ##Check for faint
                if check_faint(t2_pokemon):
                    self.handle_faint('2')
                    pygame.display.flip()
                    self.GAME_RECORD["my_status"].append(my_status)
                    self.GAME_RECORD["op_status"].append(op_status)
                    my_hp = t1_pokemon.hp - t1_pokemon.damage_taken
                    op_hp = t2_pokemon.hp - t2_pokemon.damage_taken
                    self.GAME_RECORD["my_hp"].append(my_hp)
                    self.GAME_RECORD["op_hp"].append(op_hp)                    
                    return


            ##################NEXT TURN t1 -> t2##################
            if t2_pokemon.status == Status.sleep:
                self.render_text(f"{t2_pokemon.name} is asleep", refresh=True)
                pygame.display.flip()
                waitPress()
            elif t2_pokemon.status == Status.frozen:
                self.render_text(f"{t2_pokemon.name} is frozen", refresh=True)
                pygame.display.flip()
                waitPress()
            elif t2_pokemon.status == Status.confused:
                chance = randint(0,100)
                if chance > 50:
                     ##Use chosen move
                    self.render_text(f"{t2_pokemon.name} used { at2['Name'] } ", refresh=True)
                    pygame.display.flip()
                    waitPress()
                    t2_pokemon.attack_t(at2, t1_pokemon)

                    t1_pokemon.draw_health_bar(self.screen, 1000, 600)
                    pygame.display.flip()
                    waitPress()

                    ##Check for faint
                    if check_faint(t1_pokemon):
                        self.handle_faint('1')
                        pygame.display.flip()
                        self.GAME_RECORD["my_status"].append(my_status)
                        self.GAME_RECORD["op_status"].append(op_status)
                        my_hp = t1_pokemon.hp - t1_pokemon.damage_taken
                        op_hp = t2_pokemon.hp - t2_pokemon.damage_taken
                        self.GAME_RECORD["my_hp"].append(my_hp)
                        self.GAME_RECORD["op_hp"].append(op_hp)                        
                        return
                else:
                    confuse_attack = {"Name": "Pound", "Type": "Normal", "Category": "Physical","PP": 35, "Power": "40","Accuracy": "100"}
                    t2_pokemon.damage_taken += t2_pokemon.compute_atk_damage(confuse_attack, t2_pokemon)
                    t2_pokemon.draw_health_bar(self.screen, 1000, 600)
                    self.render_text(f"{t2_pokemon.name} hurt itself in confusion", refresh=True)
                    pygame.display.flip()
                    waitPress()

                    ##Check for faint
                    if check_faint(t1_pokemon):
                        self.handle_faint('2')
                        pygame.display.flip()
                        self.GAME_RECORD["my_status"].append(my_status)
                        self.GAME_RECORD["op_status"].append(op_status)
                        my_hp = t1_pokemon.hp - t1_pokemon.damage_taken
                        op_hp = t2_pokemon.hp - t2_pokemon.damage_taken
                        self.GAME_RECORD["my_hp"].append(my_hp)
                        self.GAME_RECORD["op_hp"].append(op_hp)                       
                        return        
            elif t2_pokemon.status == Status.paralyzed:
                chance = randint(0,100)
                if chance > 30:
                     ##Use chosen move
                    self.render_text(f"{t2_pokemon.name} used { at2['Name'] } ", refresh=True)
                    pygame.display.flip()
                    waitPress()
                    t2_pokemon.attack_t(at2, t1_pokemon)
                    t2_pokemon.draw_health_bar(self.screen, 1000, 600)
                    pygame.display.flip()
                    waitPress()

                    ##Check for faint
                    if check_faint(t2_pokemon):
                        self.handle_faint('2')
                        pygame.display.flip()
                        self.GAME_RECORD["my_status"].append(my_status)
                        self.GAME_RECORD["op_status"].append(op_status)
                        my_hp = t1_pokemon.hp - t1_pokemon.damage_taken
                        op_hp = t2_pokemon.hp - t2_pokemon.damage_taken
                        self.GAME_RECORD["my_hp"].append(my_hp)
                        self.GAME_RECORD["op_hp"].append(op_hp)                        
                        return
                else:
                    self.render_text(f"{t2_pokemon.name} is paralyzed", refresh=True)
                    pygame.display.flip()
                    waitPress()
            else:
                #default sequence
                self.render_text(f"{t2_pokemon.name} used { at2['Name'] } ", refresh=True)               
                pygame.display.flip()
                waitPress()                
                t2_pokemon.attack_t(at2, t1_pokemon)

                t1_pokemon.draw_health_bar(self.screen, 100, 600)
                pygame.display.flip()
                waitPress()
            t1_pokemon.render_status_symbol(self.screen, 100, 620)
            t2_pokemon.render_status_symbol(self.screen, 1000, 620)

            if check_faint(t1_pokemon):
                self.handle_faint('1')
                pygame.display.flip()
                self.GAME_RECORD["my_status"].append(my_status)
                self.GAME_RECORD["op_status"].append(op_status)
                my_hp = t1_pokemon.hp - t1_pokemon.damage_taken
                op_hp = t2_pokemon.hp - t2_pokemon.damage_taken
                self.GAME_RECORD["my_hp"].append(my_hp)
                self.GAME_RECORD["op_hp"].append(op_hp)                
                return 
            

            ## Apply Status Effects ##
            t1_pokemon.apply_status_damage(t2_pokemon, self.render_text)
            t2_pokemon.apply_status_damage(t1_pokemon, self.render_text)

            ##Check for another faint due to status
            if check_faint(t2_pokemon):
                self.handle_faint('2')
                pygame.display.flip()
                self.GAME_RECORD["my_status"].append(my_status)
                self.GAME_RECORD["op_status"].append(op_status)
                my_hp = t1_pokemon.hp - t1_pokemon.damage_taken
                op_hp = t2_pokemon.hp - t2_pokemon.damage_taken
                self.GAME_RECORD["my_hp"].append(my_hp)
                self.GAME_RECORD["op_hp"].append(op_hp)                
                return
            if check_faint(t1_pokemon):
                self.handle_faint('1')
                pygame.display.flip()
                self.GAME_RECORD["my_status"].append(my_status)
                self.GAME_RECORD["op_status"].append(op_status)
                my_hp = t1_pokemon.hp - t1_pokemon.damage_taken
                op_hp = t2_pokemon.hp - t2_pokemon.damage_taken
                self.GAME_RECORD["my_hp"].append(my_hp)
                self.GAME_RECORD["op_hp"].append(op_hp)
                return
        else:

            if t2_pokemon.status == Status.sleep:
                self.render_text(f"{t2_pokemon.name} is asleep", refresh=True)
                pygame.display.flip()
                waitPress()
            elif t2_pokemon.status == Status.frozen:
                self.render_text(f"{t2_pokemon.name} is frozen", refresh=True)
                pygame.display.flip()
                waitPress()
            elif t2_pokemon.status == Status.confused:
                chance = randint(0,100)
                if chance > 50:
                     ##Use chosen move
                    self.render_text(f"{t2_pokemon.name} used { at2['Name'] } ", refresh=True)
                    pygame.display.flip()
                    waitPress()
                    
                    t2_pokemon.attack_t(at2, t1_pokemon)
                    t1_pokemon.draw_health_bar(self.screen, 100, 600)
                    pygame.display.flip()
                    waitPress()

                    ##Check for faint
                    if check_faint(t1_pokemon):
                        self.handle_faint('1')
                        pygame.display.flip()
                        self.GAME_RECORD["my_status"].append(my_status)
                        self.GAME_RECORD["op_status"].append(op_status)
                        my_hp = t1_pokemon.hp - t1_pokemon.damage_taken
                        op_hp = t2_pokemon.hp - t2_pokemon.damage_taken
                        self.GAME_RECORD["my_hp"].append(my_hp)
                        self.GAME_RECORD["op_hp"].append(op_hp)                       
                        return
                else:
                    confuse_attack = {"Name": "Pound", "Type": "Normal", "Category": "Physical","PP": 35, "Power": "40","Accuracy": "100"}
                    t2_pokemon.damage_taken += t2_pokemon.compute_atk_damage(confuse_attack, t2_pokemon)
                    t2_pokemon.draw_health_bar(self.screen, 1000, 600)
                    self.render_text(f"{t2_pokemon.name} hurt itself in confusion", refresh=True)
                    pygame.display.flip()
                    waitPress()

                    ##Check for faint
                    if check_faint(t1_pokemon):
                        self.handle_faint('2')
                        pygame.display.flip()
                        self.GAME_RECORD["my_status"].append(my_status)
                        self.GAME_RECORD["op_status"].append(op_status)
                        my_hp = t1_pokemon.hp - t1_pokemon.damage_taken
                        op_hp = t2_pokemon.hp - t2_pokemon.damage_taken
                        self.GAME_RECORD["my_hp"].append(my_hp)
                        self.GAME_RECORD["op_hp"].append(op_hp)                      
                        return        
            elif t2_pokemon.status == Status.paralyzed:
                chance = randint(0,100)
                if chance > 30:
                     ##Use chosen move
                    self.render_text(f"{t2_pokemon.name} used { at2['Name'] } ", refresh=True)                     
                    pygame.display.flip()
                    waitPress()                     
                    t2_pokemon.attack_t(at2, t1_pokemon)

                    t2_pokemon.draw_health_bar(self.screen, 1000, 600)
                    pygame.display.flip()
                    waitPress()

                    ##Check for faint
                    if check_faint(t2_pokemon):
                        self.handle_faint('2')
                        pygame.display.flip()
                        return
                else:
                    print('here')
                    self.render_text(f"{t2_pokemon.name} is paralyzed", refresh=True)
                    pygame.display.flip()
                    waitPress()
            else:
                #default sequence
                self.render_text(f"{t2_pokemon.name} used { at2['Name'] } ", refresh=True)                
                pygame.display.flip()
                waitPress()               
                t2_pokemon.attack_t(at2, t1_pokemon)

                t1_pokemon.draw_health_bar(self.screen, 100, 600)
                pygame.display.flip()
                waitPress()

            t1_pokemon.render_status_symbol(self.screen, 100, 620)
            t2_pokemon.render_status_symbol(self.screen, 1000, 620)
            if check_faint(t1_pokemon):
                self.handle_faint('1')
                pygame.display.flip()

                self.GAME_RECORD["my_status"].append(my_status)
                self.GAME_RECORD["op_status"].append(op_status)
                my_hp = t1_pokemon.hp - t1_pokemon.damage_taken
                op_hp = t2_pokemon.hp - t2_pokemon.damage_taken
                self.GAME_RECORD["my_hp"].append(my_hp)
                self.GAME_RECORD["op_hp"].append(op_hp)
                return 

            ##########################NEXT TURN t2-> t1#######################################################

            if t1_pokemon.status == Status.sleep:
                self.render_text(f"{t1_pokemon.name} is asleep", refresh=True)
                pygame.display.flip()
                waitPress()
            elif t1_pokemon.status == Status.frozen:
                self.render_text(f"{t1_pokemon.name} is frozen", refresh=True)
                pygame.display.flip()
                waitPress()
            elif t1_pokemon.status == Status.confused:
                chance = randint(0,100)
                if chance > 50:
                     ##Use chosen move
                    self.render_text(f"{t1_pokemon.name} used { at1['Name'] } ", refresh=True)                     
                    pygame.display.flip()
                    waitPress()                     
                    t1_pokemon.attack_t(at1, t2_pokemon)
                    t2_pokemon.draw_health_bar(self.screen, 1000, 600)
                    pygame.display.flip()
                    waitPress()

                    ##Check for faint
                    if check_faint(t2_pokemon):
                        self.handle_faint('2')
                        pygame.display.flip()

                        self.GAME_RECORD["my_status"].append(my_status)
                        self.GAME_RECORD["op_status"].append(op_status)
                        my_hp = t1_pokemon.hp - t1_pokemon.damage_taken
                        op_hp = t2_pokemon.hp - t2_pokemon.damage_taken
                        self.GAME_RECORD["my_hp"].append(my_hp)
                        self.GAME_RECORD["op_hp"].append(op_hp)
                        return
                else:
                    confuse_attack = {"Name": "Pound", "Type": "Normal", "Category": "Physical","PP": 35, "Power": "40","Accuracy": "100"}
                    t1_pokemon.damage_taken += t1_pokemon.compute_atk_damage(confuse_attack, t1_pokemon)
                    t1_pokemon.draw_health_bar(self.screen, 100, 600)
                    self.render_text(f"{t1_pokemon.name} hurt itself in confusion", refresh=True)
                    pygame.display.flip()
                    waitPress()

                    t1_pokemon.render_status_symbol(self.screen, 100, 620)
                    t2_pokemon.render_status_symbol(self.screen, 1000, 620)
                    ##Check for faint
                    if check_faint(t1_pokemon):
                        self.handle_faint('1')
                        pygame.display.flip()

                        self.GAME_RECORD["my_status"].append(my_status)
                        self.GAME_RECORD["op_status"].append(op_status)
                        my_hp = t1_pokemon.hp - t1_pokemon.damage_taken
                        op_hp = t2_pokemon.hp - t2_pokemon.damage_taken
                        self.GAME_RECORD["my_hp"].append(my_hp)
                        self.GAME_RECORD["op_hp"].append(op_hp)
                        return

            elif t1_pokemon.status == Status.paralyzed:
                chance = randint(0,100)
                if chance > 30:
                     ##Use chosen move

                    self.render_text(f"{t1_pokemon.name} used { at1['Name'] } ", refresh=True)
                    pygame.display.flip()
                    waitPress()
                    t1_pokemon.attack_t(at1, t2_pokemon)

                    t2_pokemon.draw_health_bar(self.screen, 1000, 600)
                    pygame.display.flip()
                    waitPress()

                    ##Check for faint
                    if check_faint(t2_pokemon):
                        self.handle_faint('2')
                        pygame.display.flip()
                        return
                else:
                    self.render_text(f"{t1_pokemon.name} is paralyzed", refresh=True)
                    pygame.display.flip()
                    waitPress()
            else:
                #Default sequence
                
                ##Use chosen move

                self.render_text(f"{t1_pokemon.name} used { at1['Name'] } ", refresh=True)
                pygame.display.flip()
                waitPress()
                t1_pokemon.attack_t(at1, t2_pokemon)
                t2_pokemon.draw_health_bar(self.screen, 1000, 600)
                pygame.display.flip()
                waitPress()
                t1_pokemon.render_status_symbol(self.screen, 100, 620)
                t2_pokemon.render_status_symbol(self.screen, 1000, 620)
                ##Check for faint
                if check_faint(t2_pokemon):
                    self.handle_faint('2')
                    pygame.display.flip()

                    self.GAME_RECORD["my_status"].append(my_status)
                    self.GAME_RECORD["op_status"].append(op_status)
                    my_hp = t1_pokemon.hp - t1_pokemon.damage_taken
                    op_hp = t2_pokemon.hp - t2_pokemon.damage_taken
                    self.GAME_RECORD["my_hp"].append(my_hp)
                    self.GAME_RECORD["op_hp"].append(op_hp)
                    return

        ## Apply Status Effects ##
        t1_pokemon.apply_status_damage(t2_pokemon, self.render_text)
        t2_pokemon.apply_status_damage(t1_pokemon, self.render_text)

        ##Check for another faint due to status
        if check_faint(t2_pokemon):
            self.handle_faint('2')
            pygame.display.flip()
            self.GAME_RECORD["my_status"].append(my_status)
            self.GAME_RECORD["op_status"].append(op_status)
            my_hp = t1_pokemon.hp - t1_pokemon.damage_taken
            op_hp = t2_pokemon.hp - t2_pokemon.damage_taken
            self.GAME_RECORD["my_hp"].append(my_hp)
            self.GAME_RECORD["op_hp"].append(op_hp)
            return
        if check_faint(t1_pokemon):
            self.handle_faint('1')
            pygame.display.flip()
            self.GAME_RECORD["my_status"].append(my_status)
            self.GAME_RECORD["op_status"].append(op_status)
            my_hp = t1_pokemon.hp - t1_pokemon.damage_taken
            op_hp = t2_pokemon.hp - t2_pokemon.damage_taken
            self.GAME_RECORD["my_hp"].append(my_hp)
            self.GAME_RECORD["op_hp"].append(op_hp)
            return

        t1_pokemon.draw_health_bar(self.screen, 100, 600)
        t2_pokemon.draw_health_bar(self.screen, 1000, 600)


        self.GAME_RECORD["my_status"].append(my_status)
        self.GAME_RECORD["op_status"].append(op_status)
        my_hp = t1_pokemon.hp - t1_pokemon.damage_taken
        op_hp = t2_pokemon.hp - t2_pokemon.damage_taken
        self.GAME_RECORD["my_hp"].append(my_hp)
        self.GAME_RECORD["op_hp"].append(op_hp)


        pygame.display.flip()
        return False