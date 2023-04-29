# Pokemon Trainer AI

### Goal: Create an AI that can replicate the decisions of a Pokemon Trainer

# Methods

## RBES (Rules Based Expert System)

### Our Inference Engine:
We used a series of production rules based on knowledge of the game of Pokemon to make an inference engine
<br>
Uses its knowledge of a pokemon’s moves and current status effects to model the decision making of a Pokemon Trainer
<br>
Scores each of its current Pokemon’s move options
<br>
For Status moves, Pokémon current HP, existing buff/debuff, and effectiveness are considered in scoring
<br>
For Damage Moves, move power, type effectiveness, same type bonus, secondary effect application, and self-harming application are considered in scoring.
<br>
Chooses the highest scoring move option to use to against opponent
<br>
Recommends the highest scoring move to the Pokemon Trainer each turn in battle
<br>
High-Level Logic Diagram: https://app.diagrams.net/#G1qa-3euYMihw4ZtDVu00VMMIEIYdfPlNI
<br>
Or check out the RBES.png in main directory
<br>
Data Used: Pokemon Database, Pokemon Moves Database, Pokemon Battle Damage Calculation Formulas
<br>
### Data Sources
<br>
Damage Calculations: https://bulbapedia.bulbagarden.net/wiki/Damage
<br>
Pokemon Stat Calculations: https://pokemon.fandom.com/wiki/Statistics
<br>
Pokedex Data: https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_numbe
<br>
Type Bonuses: https://www.ign.com/wikis/pokemon-red-blue-yellow-version/Pokemon_Types

## Reinforcement Q-Learning
We used a state based Q-learning to find the best move to choose based on rewards.
<br>
In each state, the type of Pokémon is checked. After that, both Pokémons will use moves (Action) to deduct each other's HP
<br>
One of the two state-reward formulas is chosen based on the type counter relationship between both Pokémons and their HP difference.
<br>
The Pokémon is rewarded more if it survives hard combat (got type-countered) and less if it survies easy combat (type-countered opponent)
<br>
Until the game ends (either Pokémon reaches zero HP), the state-reward is calculated and aggregated. 
<br>
After the game ends (Final State), a score bonus or penality is added to sum of state-rewards if the Pokémon won or lose respectively.
<br>
The lose_counter increment by 1 each time the Pokémon loses and Pokémon is awarded with large reward if it lost multiple rounds before making a come-back to win
<br>
The reward changes is recorded and fed to the Q-Learning Module to decide the policy: which action (Pokémon's move) is optimal during each state.
<br>
Data Used: Pokemon Database, Pokemon Moves Database, Pokemon Battle Damage Calculation Formulas, Charizard combat data: train_data_output.csv in folder train_data
<br>
High-Level Logic Diagram: RL.png in our main folder
<br>
<br>
<br>
<br>
## Decision Trees
