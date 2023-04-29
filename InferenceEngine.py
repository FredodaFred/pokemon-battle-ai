
from data import type_modifier, match_type, stage_modifier, secondary_effect_moves, Status

status_effecting_moves = ['Sleep Powder', 'Sing', 'Hypnosis', 'Spore', 'Poison Powder', 'Toxic', 'Poison Gas', 'Stun Spore', 'Glare', 'Thunder Wave', 'Supersonic', 'Confuse Ray', 'Leech Seed']
class InferenceEngine:
    '''
        Based on other pokemon, make a recomendation on which moves attacking pokemon should make

        ...

        Methods
        -------
        move_recomendation(self, trainer1, trainer2)
    '''
    
    def __init__(self):
        return

    def move_recomendation(self, trainer1, op_pk):
        '''
        
        '''
        atk_pk = trainer1.active_pokemon()

        swap_score = self._evaluate_swap(atk_pk, op_pk)
        if swap_score == 'SWAP':
            return 'SWAP'
            
        move_options = atk_pk.moves
        scores = []
        names = [] #TESTING PURPOSES
        for option in move_options:
            names.append(option['Name'])
            if option['Category'] == 'Status':
                scores.append( self._evaluate_status_move(option, atk_pk, op_pk) ) 
            else:
                scores.append( self._evaluate_attack_move(option,  atk_pk, op_pk) )

        max_score_idx = 0
    
        for i in range(1, len(scores)):
            if scores[i] > scores[max_score_idx]:
                max_score_idx = i
        
        # print(f'Scores: {scores} Moves: {names}')
        return move_options[max_score_idx]

    def _evaluate_swap(self, atk_pk, op_pk):
        '''
        
        '''
        return None
    def _evaluate_status_move(self, move, atk_pk, op_pk):
        '''
        
        '''
        move_name = move['Name']
        #useless moves
        if move_name in ['Splash', 'Teleport']:
            return 0

        #can't effect other pokemon
        type_1_bonus = type_modifier[match_type(move["Type"])][match_type(op_pk.type1)]
        type_2_bonus = type_modifier[match_type(move["Type"])][match_type(op_pk.type2)]
        if type_1_bonus == 0 or type_2_bonus == 0:
            return 0

        #Direct status changers

        if op_pk.status == Status.no_status and move_name in status_effecting_moves:

            if move_name in ['Sleep Powder', 'Sing', 'Hypnosis', 'Spore']:
                return 150
            elif move_name in ['Poison Powder', 'Toxic', 'Poison Gas']:
                return 140
            elif move_name in ['Stun Spore', 'Glare', 'Thunder Wave']:
                return 120
            elif move_name in ['Supersonic', 'Confuse Ray']:
                return 130
            elif move_name == 'Leech Seed':
                return 160
        elif move_name in status_effecting_moves :
            return 0          
                    
        #Self healers
        if move_name in ['Recover', 'Soft Boiled']:
            if atk_pk.hp - atk_pk.damage_taken < atk_pk.hp * 0.25:
                return 170
            elif atk_pk.hp - atk_pk.damage_taken < atk_pk.hp * 0.50:
                return 120
            else: 
                return 80
            
        elif move_name == 'Rest':
            if atk_pk.hp - atk_pk.damage_taken < atk_pk.hp * 0.25:
                return 150
            elif atk_pk.hp - atk_pk.damage_taken < atk_pk.hp * 0.50:
                return 100
            else: 
                return 50

        #attack, def, spatk, spdef, speed
        if move_name in ['Harden', 'Defense Curl', 'Withdraw']:
            return 80
        elif move_name in ['Growl']:  
            return 80
        elif move_name in ['Tail Whip', 'Leer']:
            return 80          
        elif move_name in ['Agility']:        
            return 80
        elif move_name == 'Amnesia':       
            return 80
        elif move_name in ['String Shot']:       
            return 80
        elif move_name in ['Sharpen', 'Meditate']:        
            return 80
        elif move_name == 'Swords Dance':
            return 120
        elif move_name == 'Acid Armor':      
            return 120  
        return 0

    def _evaluate_attack_move(self, move, atk_pk, op_pk):
        '''
            Arguments:
        '''

        #Essentially we are redoing the calculation from compute_atk_damage, except with a few extra steps to make it more generalized 
        move_name = move['Name']
        type_1_bonus = 20*(type_modifier[match_type(move["Type"])][match_type(op_pk.type1)])
        type_2_bonus = 20*(type_modifier[match_type(move["Type"])][match_type(op_pk.type2)])
        if type_1_bonus == 0 or type_2_bonus == 0:
            return 0
        stab =  30 if move["Type"] == atk_pk.type1 or move["Type"] == atk_pk.type2 else 10
        power = move['Power']
        #unique cases...
        if move_name == 'Dragon Rage':
            power = 40
        elif move_name == "Super Fang":
            power = op_pk.hp // 2
        elif move_name in ['Guillotine', 'Horn Drill', 'Fissure']:
            #only hits 35% of time
            # hit = choices([0,1], [70, 30])
            # power = 65535*hit[0]
            power =  70
        elif move_name == "Sonic Boom":
            power = 20
        elif move_name == 'Seismic Toss':
            power = 50
        elif move_name == 'Psywave':
            power = 37.5
        elif move_name == "Night Shade":
            power = 50
        else:
            #default case
            power = int(power)
        
        attack_modifier = 10*(stage_modifier[atk_pk.stat_stages[0]]) if move["Category"] == "Physical" else 10*(stage_modifier[atk_pk.stat_stages[2]])

        #check for secondary effects
        secondary_effect_bonus = 0
        if move_name in secondary_effect_moves:
            if move_name in ['Absorb', 'Mega Drain', 'Leech Life']:
                secondary_effect_bonus = power//2
            elif move_name in ['Double Slap', 'Comet Punch', 'Fury Attack', 'Pin Missile', 'Barrage', 'Double Kick', 'Twineedle']:
                power = atk_pk.apply_secondary_effect(move, op_pk, power)
            elif op_pk.status == Status.no_status:
                if move_name in ['Fire Punch', 'Ember', 'Flamethrower']:
                    secondary_effect_bonus += 10
                elif move_name in ['Ice Punch', 'Ice Beam', 'Blizzard']:
                    secondary_effect_bonus += 20
                elif move_name in ['Psybeam']:
                    secondary_effect_bonus += 13
                elif move_name == 'Thunder Punch':
                    secondary_effect_bonus += 5
                elif move_name == 'Body Slam':
                    if not match_type(op_pk.type1) == 0 and not match_type(op_pk.type1) == 0:
                        secondary_effect_bonus += 7
                elif move_name == 'Poison Sting':
                    secondary_effect_bonus += 15
                elif move_name == "Acid":
                    secondary_effect_bonus += 5
                #recoil moves
                elif move_name in ['Take Down', 'Double Edge', 'Submission']:
                    recoil_damage = ((atk_pk.compute_atk_damage(move, op_pk))*0.25)//1
                    ##Are we on low hp????
                    if recoil_damage + atk_pk.damage_taken >= atk_pk.hp:
                        #Will this kill us????
                        return 0
                    elif atk_pk.hp - atk_pk.damage_taken < atk_pk.hp * 0.25:
                        secondary_effect_bonus -= 50
                    elif atk_pk.hp - atk_pk.damage_taken < atk_pk.hp * 0.55:
                        secondary_effect_bonus -= 30
                    else: 
                        secondary_effect_bonus -= 10
            
        return  stab + type_1_bonus + type_2_bonus + power + attack_modifier