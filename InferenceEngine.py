
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

    def move_recomendation(self, trainer1, trainer2):
        '''
        
        '''
        atk_pk = trainer1.active_pokemon()
        op_pk = trainer2.active_pokemon()
        #swap_score = self._evaluate_swap(atk_pk, op_pk)
        move_options = atk_pk.moves
        score = []
        for option in move_options:
            if option['Category'] == 'Status':
                score.append( self._evaluate_status_move() )
            else:
                score.append( self._evaluate_attack_move() )

    def _evaluate_swap(self, atk_pk, op_pk):
        '''
        
        '''
        pass
    def _evaluate_status_move(self, move, atk_pk, op_pk):
        '''
        
        '''
        move_name = move['Name']
        #useless moves
        if move_name in ['Splash', 'Teleport']:
            return 0
        #Direct status changers

        if op_pk.status == Status.no_status and move_name in status_effecting_moves:

            if move_name in ['Sleep Powder', 'Sing', 'Hypnosis', 'Spore']:
                return 110
            elif move_name in ['Poison Powder', 'Toxic', 'Poison Gas']:
                return 80
            elif move_name in ['Stun Spore', 'Glare', 'Thunder Wave']:
                return 60
            elif move_name in ['Supersonic', 'Confuse Ray']:
                return 70
            elif move_name == 'Leech Seed':
                return 140
        else:
            return 0          
                    
        #Self healers
        if move_name in ['Recover', 'Soft Boiled']:
            if atk_pk.hp - atk_pk.damage_taken < atk_pk.hp * 0.25:
                return 150
            elif atk_pk.hp - atk_pk.damage_taken < atk_pk.hp * 0.55:
                return 70
            else: 
                return 20
            
        elif move_name == 'Rest':
            if atk_pk.hp - atk_pk.damage_taken < atk_pk.hp * 0.25:
                return 140
            elif atk_pk.hp - atk_pk.damage_taken < atk_pk.hp * 0.55:
                return 40
            else: 
                return 10

        #attack, def, spatk, spdef, speed
        if move_name in ['Harden', 'Defense Curl', 'Withdraw']:
            return 30
        elif move_name in ['Growl']:  
            return 30
        elif move_name in ['Tail Whip', 'Leer']:
            return 30          
        elif move_name in ['Agility']:        
            return 30
        elif move_name == 'Amnesia':       
            return 50
        elif move_name in ['String Shot']:       
            return 20
        elif move_name in ['Sharpen', 'Meditate']:        
            return 30
        elif move_name == 'Swords Dance':
            return 50
        elif move_name == 'Acid Armor':      
            return 50  


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
        if power == '-':
            #unique cases...
            if move_name == 'Dragon Rage':
                power = 40
            elif move_name == "Super Fang":
                power = op_pk.hp // 2
            elif move_name in ['Guillotine', 'Horn Drill']:
                #only hits 35% of time
                # hit = choices([0,1], [70, 30])
                # power = 65535*hit[0]
                power =  70
            elif move_name == "Sonic Boom":
                power = 20
            elif move_name == 'Seismic Toss':
                power = 50
            elif move_name == 'Psywave':
                # randint(1, 75), so we return mean
                power = 37.5
            elif move_name == "Night Shade":
                power = 50
        else:
            power = int(power)
        
        pk_atk_pwr = atk_pk.attack*(stage_modifier[atk_pk.stat_stages[0]]) if move["Category"] == "Physical" else atk_pk.special_attack*(stage_modifier[atk_pk.stat_stages[2]])

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
                    secondary_effect_bonus += 5
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
            
            #return total score of this move
            print(f"pk_atk_pwr: {pk_atk_pwr}, stab: {stab} t1b: {type_1_bonus} t2b: {type_2_bonus} power: {power}")
            return pk_atk_pwr + stab + type_1_bonus + type_2_bonus + power
    
'''
 #damage = (((((1/5)*( 2 * level * critical)+2)*attack_power*(pokemon_attack)/(other_pokemon defense))/50 ))*(same_type_attack_bonus)*(attack adv on oppponet type1))*(attack adv on oppponet type2)*(randunif(217, 255)/255  )

"1": {
    "Name": "Pound",
    "Type": "Normal",
    "Category": "Physical",
    "PP": 35,
    "Power": "40",
    "Accuracy": "100"
},
'''