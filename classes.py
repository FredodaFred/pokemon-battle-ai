import pygame
from random import randint, choice, choices
from data import pokemon_dict, moves, type_modifier, move_sets, stage_modifier, Turn, Status
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
    status_img = None
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
        #keep track of used moves
        self.used_moves = []
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
        
    def render_status_symbol(self, screen, x_loc, y_loc):
        status = self.status
        if status == Status.no_status:
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
    
    def apply_status_damage(self, otherPokemon):
        if self.status == Status.burn:
            self.damage_taken += self.hp//16
        elif self.status == Status.poison:
            self.damage_taken += self.hp//16
        elif self.status == Status.leech_seed:
            self.damage_taken += self.hp//16
            otherPokemon.damage_taken -= self.hp//16
        elif self.status == Status.sleep or self.status == Status.confused:
            self.status_counter -= 1
            if self.status_counter == 0:
                self.status = Status.no_status
        elif self.status == Status.frozen:
            self.status = choices([Status.frozen, Status.no_status], [90, 10])
    
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
            if otherPokemon.status == Status.no_status and not Pokemon.match_type(otherPokemon.type1) == 0 and not Pokemon.match_type(otherPokemon.type1) == 0:
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
        elif move['Name'] in ['Guillotine', 'Horn Drill']:
            #only hits 35% of time
            hit = choices([0,1], [70, 30])
            return 65535*hit[0]
        elif move['Name'] == "Sonic Boom":
            return 20
        elif move['Name'] == 'Seismic Toss':
            return 50
        elif move['Name'] == 'Psywave':
            return randint(1, 75)
        
        
        move_data = move
        power = int(move_data["Power"]) 
        #attack, def, spatk, spdef, speed
        pokemon_atk = self.attack*(stage_modifier[self.stat_stages[0]]) if move_data["Category"] == "Physical" else self.special_attack*(stage_modifier[self.stat_stages[2]])
        other_def = otherPokemon.defense*(stage_modifier[otherPokemon.stat_stages[1]]) if move_data["Category"] == "Physical" else otherPokemon.special_defense*(stage_modifier[otherPokemon.stat_stages[3]])
        STAB = 1.5 if move_data["Type"] == self.type1 or move_data["Type"] == self.type2 else 1
        type_1_bonus = type_modifier[Pokemon.match_type(move_data["Type"])][Pokemon.match_type(otherPokemon.type1)]
        type_2_bonus = type_modifier[Pokemon.match_type(move_data["Type"])][Pokemon.match_type(otherPokemon.type2)]
        random = randint(217, 255) / 255

        damage = ((((22*power*(pokemon_atk/other_def))/50)+2)*STAB*type_1_bonus*type_2_bonus*random ) // 1

        #Moves with secondary effects
        damage = self.apply_secondary_effect(move, otherPokemon, damage)
        # accuracy = int(move_data["Accuracy"])
        # miss_or_hit = 0 if randint(1, 100) > accuracy else 1
        return damage

    def draw_health_bar(self, screen, x, y):
        percent = self.damage_taken/self.hp
        pygame.draw.rect(screen, (0,0,0), (x, y, 250, 10) )
        pygame.draw.rect(screen, (0,128,0), (x, y, 250*(1-percent), 10) )
        # pygame.draw.rect(screen, (255,0,0), (x + 250*(1-percent) if percent <= 250 else 250, y, 250*percent, 10))
        pygame.draw.rect(screen, (255,0,0), (x + 250*(1-percent), y, 250*percent, 10))

    def status_attack(self, move, otherPokemon):
        #Direct status changers
        if otherPokemon.status == Status.no_status:
            if move['Name'] in ['Sleep Powder', 'Sing', 'Hypnosis', 'Spore']:
                otherPokemon.status = Status.sleep
                return
            elif move['Name'] in ['Poison Powder', 'Toxic', 'Poison Gas']:
                otherPokemon.status = Status.poison
                return
            elif move['Name'] in ['Stun Spore', 'Glare', 'Thunder Wave']:
                otherPokemon.status = Status.paralyzed
                return
            elif move['Name'] in ['Supersonic', 'Confuse Ray']:
                otherPokemon.status = Status.confused
                return
            
        #Self healers
        if move['Name'] in ['Recover', 'Soft Boiled']:
            self.damage_taken -= (self.hp // 2) if self.damage_taken -(self.hp // 2) >= 0 else 0
            return

        if move['Name'] == 'Rest':
            self.damage_taken = 0
            self.status = Status.sleep
            self.status_counter = 2

        #attack, def, spatk, spdef, speed
        if move['Name'] in ['Harden', 'Defense Curl', 'Withdraw']:
            self.stat_stages[1] =  self.stat_stages[1] + 1 if self.stat_stages[1] < 6 else 6
        if move['Name'] in ['Growl']:
            otherPokemon.stat_stages[0] = self.stat_stages[0] - 1 if self.stat_stages[0] > -6 else -6
        if move['Name'] in ['Agility']:
            self.stat_stages[4] =  self.stat_stages[4] + 1 if self.stat_stages[4] < 6 else 6
        if move['Name'] == 'Amnesia':
            self.stat_stages[3] = self.stat_stages[3] + 2 if self.stat_stages[3] < 5 else 6
        if move['Name'] in ['String Shot']:
            otherPokemon.stat_stages[4] =  otherPokemon.stat_stages[4] - 1 if otherPokemon.stat_stages[4] > -6 else -6
        if move['Name'] == 'Sharpen':
            self.stat_stages[0] = self.stat_stages[0] + 1 if self.stat_stages[0] < 6 else 6
        if move['Name'] == 'Swords Dance':
            self.stat_stages[0] = self.stat_stages[0] + 2 if self.stat_stages[0] < 5 else 6
        if move['Name'] == 'Acid Armor':
            self.stat_stages[1] = self.stat_stages[1] + 2 if self.stat_stages[1] < 5 else 6       

    def attack_t(self, move, otherPokemon):
        #Check the moves stack here 
        if move["Category"] == "Status":
            self.status_attack(move, otherPokemon) 
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
        self.fainted = [] #stores fainted pokemon
        
    
    def add_pokemon(self, pokemon):
        self.team.append(pokemon)

    def active_pokemon(self):
        return self.team[0]

    def swap_pokemon(self, pokemon):
        self.team[0], self.team[self.team.index(pokemon)] = self.team[self.team.index(pokemon)], self.team[0]

    def choose_attack(self):
        '''
        WHERE THE AI CODE SHOULD GO...
        '''
        return choice(self.active_pokemon().moves)
    
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
        self.turn = Turn.main_turn

    def init_render(self):
        self.render_text(f"{self.trainer1.name} versus {self.trainer2.name}", refresh=True)
        self.render_text(f"Click Enter to continue...", y_offset= 20)

        for i in range(len(self.trainer1.team)):
            self.screen.blit(Engine.pokeball_img, (50, 50+i*75))

        for i in range(len(self.trainer2.team)):
            self.screen.blit(Engine.pokeball_img, (1200, 50+i*75))


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
            pygame.draw.rect(self.screen, (0, 0, 0), (50, 250, 80*5, 80*5))
            pygame.display.flip()
            self.trainer1.active_pokemon().load_sprite(self.screen, 50, 250, flip = True)
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

    def run_turn(self):
        '''
            Returns:
                gameWon: boolean - signifies if game has been won on the turn or not
        '''

        if self.trainer1.num_pokemon() == 0:
            self.render_text('Trainer 2 has won', refresh=True)
            return
        elif self.trainer2.num_pokemon() == 0:
            self.render_text('Trainer 1 has won', refresh=True)
            return

        t1_pokemon = self.trainer1.active_pokemon()
        t2_pokemon = self.trainer2.active_pokemon()
        pygame.draw.rect(self.screen, (0,0,0), (0, 600, 1240, 20))
        t1_pokemon.draw_health_bar(self.screen, 100, 600)
        t2_pokemon.draw_health_bar(self.screen, 1000, 600)
        t1_pokemon.render_status_symbol(self.screen, 100, 620)
        t2_pokemon.render_status_symbol(self.screen, 1000, 620)
        pygame.display.flip()

        at1 = self.trainer1.choose_attack()
        at2 = self.trainer2.choose_attack()


        #Move priority?

        #determine turn sequence based on speed
        
        
        waitPress()
        if t1_pokemon.speed*(stage_modifier[t1_pokemon.stat_stages[4]]) > t2_pokemon.speed*(stage_modifier[t2_pokemon.stat_stages[4]]):

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
                    t1_pokemon.attack_t(at1, t2_pokemon)
                    self.render_text(f"{t1_pokemon.name} used { at1['Name'] } ", refresh=True)
                    t2_pokemon.draw_health_bar(self.screen, 1000, 600)
                    pygame.display.flip()
                    waitPress()

                    ##Check for faint
                    if check_faint(t2_pokemon):
                        self.handle_faint('2')
                        pygame.display.flip()
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
                    t1_pokemon.attack_t(at1, t2_pokemon)
                    self.render_text(f"{t1_pokemon.name} used { at1['Name'] } ", refresh=True)
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
                t1_pokemon.attack_t(at1, t2_pokemon)
                self.render_text(f"{t1_pokemon.name} used { at1['Name'] } ", refresh=True)
                t2_pokemon.draw_health_bar(self.screen, 1000, 600)
                pygame.display.flip()
                waitPress()

                ##Check for faint
                if check_faint(t2_pokemon):
                    self.handle_faint('2')
                    pygame.display.flip()
                    return


            ####################################
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
                    t2_pokemon.attack_t(at2, t1_pokemon)
                    self.render_text(f"{t2_pokemon.name} used { at2['Name'] } ", refresh=True)
                    t1_pokemon.draw_health_bar(self.screen, 1000, 600)
                    pygame.display.flip()
                    waitPress()

                    ##Check for faint
                    if check_faint(t1_pokemon):
                        self.handle_faint('1')
                        pygame.display.flip()
                        return
                else:
                    confuse_attack = {"Name": "Pound", "Type": "Normal", "Category": "Physical","PP": 35, "Power": "40","Accuracy": "100"}
                    t2_pokemon.damage_taken += t2_pokemon.compute_atk_damage(confuse_attack, t2_pokemon)
                    t2_pokemon.draw_health_bar(self.screen, 100, 600)
                    self.render_text(f"{t2_pokemon.name} hurt itself in confusion", refresh=True)
                    pygame.display.flip()
                    waitPress()

                    ##Check for faint
                    if check_faint(t1_pokemon):
                        self.handle_faint('2')
                        pygame.display.flip()
                        return        
            elif t2_pokemon.status == Status.paralyzed:
                chance = randint(0,100)
                if chance > 30:
                     ##Use chosen move
                    t2_pokemon.attack_t(at2, t1_pokemon)
                    self.render_text(f"{t2_pokemon.name} used { at2['Name'] } ", refresh=True)
                    t2_pokemon.draw_health_bar(self.screen, 1000, 600)
                    pygame.display.flip()
                    waitPress()

                    ##Check for faint
                    if check_faint(t2_pokemon):
                        self.handle_faint('2')
                        pygame.display.flip()
                        return
                else:
                    self.render_text(f"{t2_pokemon.name} is paralyzed", refresh=True)
                    pygame.display.flip()
                    waitPress()
            else:
                #default sequence
                t2_pokemon.attack_t(at2, t1_pokemon)
                self.render_text(f"{t2_pokemon.name} used { at2['Name'] } ", refresh=True)
                t1_pokemon.draw_health_bar(self.screen, 100, 600)
                pygame.display.flip()
                waitPress()


            if check_faint(t1_pokemon):
                self.handle_faint('1')
                pygame.display.flip()
                return 
            

            ## Apply Status Effects ##
            t1_pokemon.apply_status_damage(t2_pokemon)
            t2_pokemon.apply_status_damage(t1_pokemon)

            ##Check for another faint due to status
            if check_faint(t2_pokemon):
                self.handle_faint('2')
                pygame.display.flip()
                return
            if check_faint(t1_pokemon):
                self.handle_faint('1')
                pygame.display.flip()
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
                    t2_pokemon.attack_t(at2, t1_pokemon)
                    self.render_text(f"{t2_pokemon.name} used { at2['Name'] } ", refresh=True)
                    t1_pokemon.draw_health_bar(self.screen, 1000, 600)
                    pygame.display.flip()
                    waitPress()

                    ##Check for faint
                    if check_faint(t1_pokemon):
                        self.handle_faint('1')
                        pygame.display.flip()
                        return
                else:
                    confuse_attack = {"Name": "Pound", "Type": "Normal", "Category": "Physical","PP": 35, "Power": "40","Accuracy": "100"}
                    t2_pokemon.damage_taken += t2_pokemon.compute_atk_damage(confuse_attack, t2_pokemon)
                    t2_pokemon.draw_health_bar(self.screen, 100, 600)
                    self.render_text(f"{t2_pokemon.name} hurt itself in confusion", refresh=True)
                    pygame.display.flip()
                    waitPress()

                    ##Check for faint
                    if check_faint(t1_pokemon):
                        self.handle_faint('2')
                        pygame.display.flip()
                        return        
            elif t2_pokemon.status == Status.paralyzed:
                chance = randint(0,100)
                if chance > 30:
                     ##Use chosen move
                    t2_pokemon.attack_t(at2, t1_pokemon)
                    self.render_text(f"{t2_pokemon.name} used { at2['Name'] } ", refresh=True)
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
                t2_pokemon.attack_t(at2, t1_pokemon)
                self.render_text(f"{t2_pokemon.name} used { at2['Name'] } ", refresh=True)
                t1_pokemon.draw_health_bar(self.screen, 100, 600)
                pygame.display.flip()
                waitPress()


            if check_faint(t1_pokemon):
                self.handle_faint('1')
                pygame.display.flip()
                return 

            ###########

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
                    t1_pokemon.attack_t(at1, t2_pokemon)
                    self.render_text(f"{t1_pokemon.name} used { at1['Name'] } ", refresh=True)
                    t2_pokemon.draw_health_bar(self.screen, 1000, 600)
                    pygame.display.flip()
                    waitPress()

                    ##Check for faint
                    if check_faint(t2_pokemon):
                        self.handle_faint('2')
                        pygame.display.flip()
                        return
                else:
                    confuse_attack = {"Name": "Pound", "Type": "Normal", "Category": "Physical","PP": 35, "Power": "40","Accuracy": "100"}
                    t1_pokemon.damage_taken += t1_pokemon.compute_atk_damage(confuse_attack, t1_pokemon)
                    t1_pokemon.draw_health_bar(self.screen, 100, 600)
                    self.render_text(f"{t1_pokemon.name} hurt itself in confusion", refresh=True)
                    pygame.display.flip()
                    waitPress()

                    ##Check for faint
                    if check_faint(t1_pokemon):
                        self.handle_faint('1')
                        pygame.display.flip()
                        return

            elif t1_pokemon.status == Status.paralyzed:
                chance = randint(0,100)
                if chance > 30:
                     ##Use chosen move
                    t1_pokemon.attack_t(at1, t2_pokemon)
                    self.render_text(f"{t1_pokemon.name} used { at1['Name'] } ", refresh=True)
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
                t1_pokemon.attack_t(at1, t2_pokemon)
                self.render_text(f"{t1_pokemon.name} used { at1['Name'] } ", refresh=True)
                t2_pokemon.draw_health_bar(self.screen, 1000, 600)
                pygame.display.flip()
                waitPress()

                ##Check for faint
                if check_faint(t2_pokemon):
                    self.handle_faint('2')
                    pygame.display.flip()
                    return

        ## Apply Status Effects ##
        t1_pokemon.apply_status_damage(t2_pokemon)
        t2_pokemon.apply_status_damage(t1_pokemon)

        ##Check for another faint due to status
        if check_faint(t2_pokemon):
            self.handle_faint('2')
            pygame.display.flip()
            return
        if check_faint(t1_pokemon):
            self.handle_faint('1')
            pygame.display.flip()
            return

        t1_pokemon.draw_health_bar(self.screen, 100, 600)
        t2_pokemon.draw_health_bar(self.screen, 1000, 600)
        
        pygame.display.flip()