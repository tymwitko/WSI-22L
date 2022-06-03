# Tymon Kobylecki WSI 22L

import gym
import time
import numpy as np
import random
import copy
from cmath import inf

def q_learning(rate, gamma, explor, states_num, actions_num, iters, envi, state):
    q = np.zeros([states_num, actions_num]) #500, 6
    best_seq = []

    for i in range(iters):
        print(" ", str(round(i*100/iters, 2)) + "%", end='\r')
        sequence = []
        reward_sum = 0
        best_reward = -inf
        done = False
        env = copy.deepcopy(envi)
        while not done:
            action = get_action(explor, env, q, state)
            sequence.append(action)

            new_state, rt, done, _ = env.step(action)
            reward_sum += rt
            q[state, action] = q[state, action] + rate * (rt + gamma * np.max(q[new_state]) - q[state, action])
            state = new_state

        if best_reward == -inf or reward_sum > best_reward:
            best_seq = copy.deepcopy(sequence)
            best_reward = reward_sum
    print(" 100%  ")

    return best_seq, best_reward


def get_action(explor, env, q, state):
    if (random.random() > explor):
        return np.argmax(q[state])
    else:
        return env.action_space.sample()


if __name__ == "__main__":
    env = gym.make('Taxi-v3')
    iterations = 25
    cwiczenia = True # czy ma być uruchomiona wizualizacja, czy eksperymenty
    seeds = range(0, 25)
    if cwiczenia:
        for i in range(iterations):
            observation = env.reset(seed=seeds[i])
            print(env.render(mode='ansi'))
            solution, rew = q_learning(0.2, 0.5, 0.2, 500, 6, 500, env, observation)        
            for ind, action in enumerate(solution):
                print("step:", ind+1, "/", len(solution))
                observation, reward, done, info = env.step(action)
                print(env.render(mode='ansi'))
                time.sleep(0.5)
                if done:
                    env.reset()
            print("Total reward:", rew)
    else:
        tested = [0.33, 0.67, 1.0]
        for i in tested: # learning rate
            for j in tested: # gamma
                for k in tested: # explor
                    av_sum = 0
                    for l in range(iterations):
                        observation = env.reset(seed=seeds[l])
                        solution, rew = q_learning(i, j, k, 500, 6, 500, env, observation) 
                        av_sum += rew
                    avg = av_sum/iterations
                    print(i, j, k, "dają", avg)
    env.close()

    # There are 6 discrete deterministic actions:
    # - 0: move south
    # - 1: move north
    # - 2: move east
    # - 3: move west
    # - 4: pickup passenger
    # - 5: drop off passenger

    # https://github.com/openai/gym/blob/master/gym/envs/toy_text/taxi.py
