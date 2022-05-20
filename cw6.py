import gym

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

def q(st, at):
    pass

if __name__ == "__main__":
    env = gym.make('Taxi-v3')
    observation, info = env.reset(seed=42, return_info=True)
    solution = [1, 1, 1, 4, 3, 3, 0, 0, 3, 3, 0, 0, 5, 4, 1, 1, 1, 0, 0, 0, 5, 1, 1, 1]
    for i in solution:
        env.render()
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
