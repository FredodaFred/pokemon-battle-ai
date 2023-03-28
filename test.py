from data import pokemon_dict, move_sets, moves

class Pokemon:
    def __init__(self, pokemon_id):
        assert pokemon_id <= 151, "Invalid Pokemon ID"
        self.id = pokemon_id
        self.image = None
        self.hp = pokemon_dict[f'{pokemon_id}']["HP"]
        self.type1 = pokemon_dict[f'{pokemon_id}']["Type 1"]
        self.type2 = pokemon_dict[f'{pokemon_id}']["Type 2"]
        self.attack = pokemon_dict[f'{pokemon_id}']["Attack"]
        self.defense = pokemon_dict[f'{pokemon_id}']["Defense"]
        self.special_attack = pokemon_dict[f'{pokemon_id}']["Sp. Atk"]
        self.special_defense = pokemon_dict[f'{pokemon_id}']["Sp. Def"]
        self.speed = pokemon_dict[f'{pokemon_id}']["Speed"]

        self.moves = []
        for move in move_sets[pokemon_id]:
            self.moves.append(moves[f'{move}'])



bulbasaur = Pokemon(1)
print(bulbasaur.speed)

