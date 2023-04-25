import pygame
from classes import Pokemon, Engine, PokemonTrainer, waitPress
from random import randint
import csv
import os
import numpy as np
import random
from collections import deque
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam


class PokemonMakeDownEnv:
    def __init__(self):
        # pygame setup
        pygame.init()
        self.score = 50
        font = pygame.font.SysFont("Arial", 20)
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        running = True

        Pokemon.sprite_sheet = pygame.image.load("./pokemon.png").convert()
        Pokemon.status_img = pygame.image.load("./status.png").convert()

        self.win_num = 0
        self.total = 0


        self.team1 = [Pokemon(6)]
        self.trainer1 = PokemonTrainer("trainer1", team=self.team1)
        self.team2 = [Pokemon(randint(1, 151))]
        self.trainer2 = PokemonTrainer("trainer2", team=self.team2)

        self.lose_poke = {}
        self.cur_op_id = self.team2[0].id
        if self.team2[0].id not in self.lose_poke:
            self.lose_poke[self.cur_op_id] = 1

        self.engine = Engine(self.screen, font, self.trainer1, self.trainer2)
        Engine.pokeball_img = pygame.transform.scale(pygame.image.load("./pokeball.png").convert(), (50, 50))
        Engine.pokeballfaint_img = pygame.transform.scale(pygame.image.load("./pokeball_faint.png").convert(), (50, 50))

        self.engine.init_render()
        self.init_seq = False

        self.engine.GAME_RECORD["my_type1"] = self.team1[0].type1
        self.engine.GAME_RECORD["my_type2"] = self.team1[0].type2
        self.engine.GAME_RECORD["op_type1"] = self.team2[0].type1
        self.engine.GAME_RECORD["op_type2"] = self.team2[0].type2

        self.op_attack = self.team2[0].attack
        self.op_defense = self.team2[0].defense
        self.op_special_attack = self.team2[0].special_attack
        self.op_special_defense = self.team2[0].special_defense
        self.op_speed = self.team2[0].speed


        self.temp = {"Grass": 0,
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




    def step(self, action):
        pygame.display.flip()
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        move_trans = {0: "Dragon Rage", 1: "Slash", 2: "Leer", 3: "Flamethrower"}
        # print(move_trans[action])
        try:
            done = self.engine.run_turn(strategy="train", action=action)
        except:
            done = True
        self.clock.tick(20)  # limits FPS to 20

        next_state = list()
        for k in ["my_hp", "op_hp", "op_type1", "my_status", "op_status"]:
            if k == "op_type1":
                next_state.append(self.temp[self.engine.GAME_RECORD[k]])
            else:
                # print(self.engine.GAME_RECORD)
                next_state.append(self.engine.GAME_RECORD[k][-1])

        # calculate reward
        if next_state[2] >= 6:
            reward = next_state[0] * 0.3 - next_state[1] * 0.1
        else:
            reward = next_state[0] * 0.3 - next_state[1] * 0.2


        # Check if the game has ended
        if done == True:
            self.total += 1
            win = self.engine.GAME_RECORD["win"]
            if not win:

                self.lose_poke[self.cur_op_id] += 1

                reward = -300  # lost
                # if next_state[2] >= 6:
                #     reward = -50
            elif win:

                cof = self.lose_poke[self.cur_op_id]
                self.lose_poke[self.cur_op_id] == self.lose_poke[self.cur_op_id]//2
                if self.lose_poke[self.cur_op_id] <= 0:
                    self.lose_poke[self.cur_op_id] = 1

                self.win_num += 1

                reward = 200 * cof #  won
                # if next_state[2] >= 6:
                #     reward = 200
            # print(f"{(self.win_num/self.total)*100 : .2f}" + "%")
        self.score += reward
        return next_state, reward, done

    def reset(self):        # pygame setup
        self.score = 0
        pygame.init()
        font = pygame.font.SysFont("Arial", 20)
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        running = True

        Pokemon.sprite_sheet = pygame.image.load("./pokemon.png").convert()
        Pokemon.status_img = pygame.image.load("./status.png").convert()

        win_num = 0
        total = 0

        self.team1 = [Pokemon(6)] 
        self.trainer1 = PokemonTrainer("trainer1", team=self.team1)
        self.team2 = [Pokemon(randint(1, 151))]
        self.trainer2 = PokemonTrainer("trainer2", team=self.team2)

        self.cur_op_id = self.team2[0].id
        if self.team2[0].id not in self.lose_poke:
            self.lose_poke[self.cur_op_id] = 1

        self.op_attack = self.team2[0].attack
        self.op_defense = self.team2[0].defense
        self.op_special_attack = self.team2[0].special_attack
        self.op_special_defense = self.team2[0].special_defense
        self.op_speed = self.team2[0].speed

        self.engine = Engine(self.screen, font, self.trainer1, self.trainer2)
        Engine.pokeball_img = pygame.transform.scale(pygame.image.load("./pokeball.png").convert(), (50, 50))
        Engine.pokeballfaint_img = pygame.transform.scale(pygame.image.load("./pokeball_faint.png").convert(), (50, 50))

        self.engine.init_render()
        self.init_seq = False

        self.engine.GAME_RECORD["my_type1"] = self.team1[0].type1
        self.engine.GAME_RECORD["my_type2"] = self.team1[0].type2
        self.engine.GAME_RECORD["op_type1"] = self.team2[0].type1
        self.engine.GAME_RECORD["op_type2"] = self.team2[0].type2

        self.engine.render_text(f"{self.trainer1.name} sent out {self.trainer1.active_pokemon().name}", refresh=True)
        self.trainer1.active_pokemon().load_sprite(self.screen, 0, 250, flip=True)

        pygame.display.flip()
        self.engine.render_text(f"{self.trainer2.name} sent out {self.trainer2.active_pokemon().name}", refresh=True)
        self.trainer2.active_pokemon().load_sprite(self.screen, 900, 250, flip=False)

        self.init_seq = True


        return [self.team1[0].hp, self.team1[0].hp, self.temp[self.team2[0].type1], 0, 0]




class DQN:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state, verbose=0)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target += self.gamma * np.amax(self.model.predict(next_state, verbose=0)[0])
            target_f = self.model.predict(state, verbose=0)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


state_size = 9
action_size = 4
agent = DQN(state_size, action_size)
env = PokemonMakeDownEnv()
episodes = 1000
batch_size = 32

for e in range(episodes):
    state = [*env.reset(), env.op_attack, env.op_defense, env.op_special_attack, env.op_special_defense]
    state = np.reshape(state, [1, state_size])
    done = False

    while not done:
        action = agent.act(state)
        next_state, reward, done = env.step(action)
        next_state = [*next_state, env.op_attack, env.op_defense, env.op_special_attack, env.op_special_defense]
        next_state = np.reshape(next_state, [1, state_size])
        agent.remember(state, action, reward, next_state, done)

        state = next_state
        if done:
            print(f"Episode: {e}/{episodes}, score: {env.score}")
            break

    if len(agent.memory) > batch_size:
        agent.replay(batch_size)


agent.model.save("./models/RL_model6.h5")