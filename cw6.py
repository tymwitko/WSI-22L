import gym
import time
import numpy as np
import itertools
from collections import defaultdict
import Plotting

def policy(observation): # 0 - south, 1 - north, 2 - east, 3 - west, 4 - pickup, 5 - dropoff
    '''
    :param observation
    returns:
    0 - south
    1 - north
    2 - east
    3 - west
    4 - pickup
    5 - dropoff
    '''
    return 0

def q(xt, ut):
    pass

def createEpsilonGreedyPolicy(Q, epsilon, num_actions):
    """
    https://www.geeksforgeeks.org/q-learning-in-python/
    Creates an epsilon-greedy policy based
    on a given Q-function and epsilon.
    
    Returns a function that takes the state
    as an input and returns the probabilities
    for each action in the form of a numpy array
    of length of the action space(set of possible actions).
    """
    def policyFunction(state):

        Action_probabilities = np.ones(num_actions,
                dtype = float) * epsilon / num_actions
                
        best_action = np.argmax(Q[state])
        Action_probabilities[best_action] += (1.0 - epsilon)
        return Action_probabilities

    return policyFunction

def qLearning(env, num_episodes, discount_factor = 1.0,
                            alpha = 0.6, epsilon = 0.1):
    """
    https://www.geeksforgeeks.org/q-learning-in-python/
    Q-Learning algorithm: Off-policy TD control.
    Finds the optimal greedy policy while improving
    following an epsilon-greedy policy"""
    
    # Action value function
    # A nested dictionary that maps
    # state -> (action -> action-value).
    Q = defaultdict(lambda: np.zeros(env.action_space.n))

    # Keeps track of useful statistics
    stats = Plotting.EpisodeStats(
        episode_lengths = np.zeros(num_episodes),
        episode_rewards = np.zeros(num_episodes))
    # stats_episode_rewards = np.zeros(num_episodes)
    # stats_episode_lengths = np.zeros(num_episodes)
    actions = []

    
    # Create an epsilon greedy policy function
    # appropriately for environment action space
    policy = createEpsilonGreedyPolicy(Q, epsilon, env.action_space.n)
    
    # For every episode
    for ith_episode in range(num_episodes):
        
        # Reset the environment and pick the first action
        state = env.reset()
        
        for t in itertools.count():
            
            # get probabilities of all actions from current state
            action_probabilities = policy(state)

            # choose action according to
            # the probability distribution
            action = np.random.choice(np.arange(
                    len(action_probabilities)),
                    p = action_probabilities)

            # take action and get reward, transit to next state
            next_state, reward, done, _ = env.step(action)

            # Update statistics
            stats.episode_rewards[ith_episode] += reward
            stats.episode_lengths[ith_episode] = t
            
            # TD Update
            best_next_action = np.argmax(Q[next_state])
            actions.append(best_next_action)
            td_target = reward + discount_factor * Q[next_state][best_next_action]
            td_delta = td_target - Q[state][action]
            Q[state][action] += alpha * td_delta

            # done is True if episode terminated
            if done:
                break
                
            state = next_state
    
    return Q, stats, actions



if __name__ == "__main__":
    env = gym.make('Taxi-v3')
    observation, info = env.reset(seed=42, return_info=True)
    # solution = [1, 1, 1, 4, 3, 3, 0, 0, 3, 3, 0, 0, 5, 4, 1, 1, 1, 0, 0, 0, 5, 1, 1, 1]
    Q, stats, solution = qLearning(env, 1000)
    Plotting.plot_episode_stats(stats)
    for i in solution:
        env.render()
        time.sleep(0.3)
        action = i  # hardcoding rozwiazania dla tasku 42
        observation, reward, done, info = env.step(action)
        print(list(env.decode(observation)), reward, done, info) # decoded observation - (taxi_row, taxi_col, passenger_location (RGYB, taxi), destination (RGYB))
        if done:
            env.reset()
    # for _ in range(10):
    #     env.render()
    #     action = policy(observation)  # User-defined policy function
    #     observation, reward, done, info = env.step(action)
    #     print(observation, reward, done, info)

    if done:
        observation, info = env.reset(return_info=True)
    env.close()

    # https://github.com/openai/gym/blob/master/gym/envs/toy_text/taxi.py
