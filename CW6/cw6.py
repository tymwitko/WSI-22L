import gym
import time
import numpy as np
import random
import copy
from cmath import inf

# https://towardsdatascience.com/reinforcement-learning-and-q-learning-an-example-of-the-taxi-problem-in-python-d8fd258d6d45
def q_learning(rate, gamma, explor, states_num, actions_num, iters, envi, state):
    q = np.zeros([states_num, actions_num]) #500, 6
    best_seq = []

    for i in range(iters):
        print(' ', str(round(i*100/iters, 2)) + '%', end='\r')
        sequence = []
        reward_sum = 0
        best_reward = -inf
        done = False
        env = copy.deepcopy(envi)
        while not done:
            action = get_action(explor, env, q, state)
            sequence.append(action)

            new_state, rt, done, info = env.step(action)
            reward_sum += rt
            q[state, action] = q[state, action] + rate * (rt + gamma * np.max(q[new_state]) - q[state, action])
            state = new_state

        if best_reward == -inf or reward_sum > best_reward:
            best_seq = copy.deepcopy(sequence)
            best_reward = reward_sum

    return best_seq, best_reward


def get_action(explor, env, q, state):
    if (random.random() > explor):
        return np.argmax(q[state])
    else:
        return env.action_space.sample()


if __name__ == "__main__":
    env = gym.make('Taxi-v3')
    # solution = [1, 1, 1, 4, 3, 3, 0, 0, 3, 3, 0, 0, 5, 4, 1, 1, 1, 0, 0, 0, 5, 1, 1, 1]
    iterations = 25
    cwiczenia = True

    # Q, stats, solution = qLearning(env, 1000)
    if cwiczenia:
        for i in range(iterations):
            observation = env.reset()
            print(env.render(mode='ansi'))
            solution, rew = q_learning(0.2, 0.5, 0.2, 500, 500, 6, copy.deepcopy(env), observation)        
            for ind, action in enumerate(solution):
                print("step:", ind+1, "/", len(solution))
                observation, reward, done, info = env.step(action)
                print(env.render(mode='ansi'))
                time.sleep(0.5)
                # print(list(env.decode(observation)), reward, done, info) # decoded observation - (taxi_row, taxi_col, passenger_location (RGYB, taxi), destination (RGYB))
                if done:
                    env.reset()
            print("Total reward:", rew)
    else:
        for i in range(10):
            i = float(i+1)/10
            for j in range(10):
                for i in range(iterations):
                    observation = env.reset()
                    # print(env.render(mode='ansi'))
                    solution, rew = q_learning(i, j, 0.2, 500, 6, 500, copy.deepcopy(env), observation) 
            print(i, j, rew)

    # if done:
    #     observation, info = env.reset(return_info=True)
    # env.close()

    # There are 6 discrete deterministic actions:
    # - 0: move south
    # - 1: move north
    # - 2: move east
    # - 3: move west
    # - 4: pickup passenger
    # - 5: drop off passenger

    # https://github.com/openai/gym/blob/master/gym/envs/toy_text/taxi.py
