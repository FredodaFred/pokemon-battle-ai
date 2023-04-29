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
High-Level Logic Diagram: 
<br>
<img src="https://user-images.githubusercontent.com/82429372/235280818-e130f99f-ba87-4541-813a-d1db5315dba0.png" alt="Decision Tree" style="width: 50%; height: auto;">
<br>
<br>
<br>
## Decision Trees
We generated some data by having Pokémon engage in random battles, including information such as their own health points, opponent's health points, opponent's type, and so on. From this data, we selected only the winning instances and examined them for any hidden patterns. We utilized a decision tree to provide us with interpretable decisions. Through repeated validation, we found that 1,000 battles and a decision tree depth of 5 were optimal to avoid overfitting. Below is the automatically generated decision tree, where the "value" represents the occurrence count of a particular situation at each node.
<br>
<img src="https://user-images.githubusercontent.com/82429372/235281119-06115be9-5ae1-4602-951e-c60a92567f5b.png" alt="Decision Tree" style="width: 50%; height: auto;">
<br>
<br>

# How to Use

This section will guide you on how to set up and run the Pokémon battle simulation using different AI strategies. 
<br>
Follow the steps below to get started:
<br>
## Step 1: Create a virtual environment
<br>
Before installing the required packages, it's a good idea to create a virtual environment. This will help isolate the dependencies for this project from other projects you may have on your system. You can create a virtual environment using the following command:
<br>

```
username$ python -m venv pokemon_ai
```
<br>
Activate the virtual environment:
<br>
- For Windows:
<br>

``` 
username$ pokemon_ai\Scripts\activate
``` 
<br>
- For macOS/Linux:

```
username$ source pokemon_ai/bin/activate
```
<br>

## Step 2: Install requirements

<br>
To install the required packages for this project, run the following command:
<br>

``` 
username$ pip install -r requirements.txt
``` 
<br>

## Step 3: Run the main script

<br>
To run the main script, use the following command:

``` 
python main.py
``` 
<br>

### Customizing AI Strategy and Model
<br>
When creating a Pokémon object, you can choose your desired AI strategy from the following options: `random`, `rbes`, `DT` (decision tree), or `RL` (reinforcement learning). If you want to test your own model, you can provide the model's path through the `model_path` parameter when creating the Pokémon object.
<br>
You can also adjust the number of battles by changing the parameters in the for-loop. This will allow you to obtain the potential win rate, which will be printed as the output.
<br>
Example:
<br>

```python 
pokemon = Pokemon(pokemon_id=6, ai_strategy="DT", model_path="path_to_your_model")
``` 
<br>
Adjust the number of battles:
<br>

```python
for i in range(1000):  # Change 1000 to the desired number of battles
    # Run the simulation
```
<br>
## Step 4: Analyze the results

After running the main script, you will see the win rate for the selected AI strategy. Use this information to compare different strategies and models, and to fine-tune your approach.
<br>












