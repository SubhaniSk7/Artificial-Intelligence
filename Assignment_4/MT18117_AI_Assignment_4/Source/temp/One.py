import numpy as np
import sys
import pygame

import math
import random

import gym
import gym_maze
import matplotlib.pyplot as mt

from gym import wrappers


def run():
    gamma = 0.99

    alpha = max(alphaMin, min(0.8, 1.0 - math.log10((0 + 1) / decayRate)))
    decayedEpsilon = min(0.8, 1.0 - math.log10((0 + 1) / decayRate))
    epsilon = max(epsilonMin, decayedEpsilon)

    for i in range(maxEpisodes):
        print('---------------------------------------------------------------------')

        done = False
        finalReward = 0

        currentState = env.reset()
        currentState = (int(currentState[0]), int(currentState[1]))

        for t in range(maxTime):  # restricting the infinite loop
            env.render()
            if random.random() < epsilon:
                action = env.action_space.sample()
            else:  # Select the action with the highest q
                action = int(np.argmax(QTable[currentState]))

            nextState, reward, done, info = env.step(action)

            nextState = (int(nextState[0]), int(nextState[1]))

            finalReward += reward

            bestQValue = np.amax(QTable[nextState])
            QTable[currentState + (action,)] += alpha * (
                    reward + gamma * (bestQValue) - QTable[currentState + (action,)])

            currentState = nextState

            if done:  # if found goal then go start next episode
                print('-->Episode:', i, ' finalReward:', finalReward, ' finished timesteps:', t)
                if (t <= np.prod(MAZE_SIZE, dtype=int)):
                    streaks += 1
                else:
                    streaks = 0
                graph.append(finalReward)
                break

            if t >= maxTime - 1:  # timeout condition--> to restrict infinite loop and not going to goal
                print('-->Episode:', i, ' finalReward:', finalReward, ' timeout timesteps:', t)
                print('-----------timeOut-----------')
                graph.append(finalReward)
                break
        if (streaks > stopStreak):
            print('path continued for ', stopStreak, ' times...stopped')
            break

        alpha = max(alphaMin, min(0.8, 1.0 - math.log10((i + 1) / decayRate)))
        decayedEpsilon = min(0.8, 1.0 - math.log10((i + 1) / decayRate))
        epsilon = max(epsilonMin, decayedEpsilon)


# ------------------------------------------------------------------------------------------------

# env = gym.make('maze-random-5x5-v0')
env = gym.make('maze-sample-5x5-v0')

MAZE_SIZE = tuple((env.observation_space.high + np.ones(env.observation_space.shape)).astype(int))
print('maze size:', MAZE_SIZE)

NUM_BUCKETS = MAZE_SIZE  # one bucket per grid
print('num of buckets:', NUM_BUCKETS)

NUM_ACTIONS = env.action_space.n
print('env.action_space:', env.action_space)  # actions N,S,E,W
print('num of actions:', NUM_ACTIONS)

STATE_BOUNDS = list(zip(env.observation_space.low, env.observation_space.high))
print('observation space:', env.observation_space)
print('state bounds:', STATE_BOUNDS)

epsilonMin = 0.001  # epsilon = for exploration min value
print('min exploration rate:', epsilonMin)

alphaMin = 0.2  # alpha= for learning rate min value
print('min learning rate:', alphaMin)

decayRate = np.prod(MAZE_SIZE, dtype=float) / 10.0  # for exploitation purpose
print('Decay factor:', decayRate)

maxEpisodes = 100000
print('num of episodes:', maxEpisodes)

maxTime = np.prod(MAZE_SIZE, dtype=int) * 100
print('max time:', maxTime)

stopStreak = 100
print('stop for continuous:', stopStreak)

SOLVED_T = np.prod(MAZE_SIZE, dtype=int)
print('solved t:', SOLVED_T)

QTable = np.zeros(NUM_BUCKETS + (NUM_ACTIONS,), dtype=float)  # STATES x ACTIONS matrix
print('q table:', len(QTable))
print(QTable.shape)
# print(QTable)
streaks = 0

graph = []

run()

mt.figure('Gym maze 5x5')
mt.plot(range(len(graph)), graph, 'r', label='5x5')
mt.title('Gym maze 5x5')
mt.ylabel('Reward')
mt.xlabel('Episodes')
mt.legend(loc='upper right')
mt.grid()
mt.show()
