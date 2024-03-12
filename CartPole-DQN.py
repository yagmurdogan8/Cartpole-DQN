import gym
import time
import numpy as np
from Agent import DQNAgent
from ReplayBuffer import ReplayMemory

# PARAMETERS 
num_iterations = 20000 
num_eval_episodes = 10 
eval_interval = 1000  

initial_collect_steps = 100  
collect_steps_per_iteration =   1
replay_buffer_max_length = 10000

batch_size = 64  
log_interval = 200

learning_rate = 1e-3  
gamma = 0.99
epsilon = 0.05
temp = 0.05

# Entities
env = gym.make("CartPole-v1", render_mode="", max_episode_steps=1000)
env_eval = gym.make("CartPole-v1")
# print(env.observation_space.shape[0]) 
# print(env.action_space.n)
dqn_agent_and_model = DQNAgent(n_states=env.observation_space.shape[0], 
                     n_actions=env.action_space.n, 
                     learning_rate=learning_rate, 
                     gamma=gamma,
                     epsilon=epsilon,
                     temp=temp)
replay_buffer = ReplayMemory(replay_buffer_max_length)
observation, info = env.reset(seed=42) 

for iteration in range(num_iterations):
    state, info = env.reset()
    # state = np.reshape(state, [1, dqn_agent_and_model.n_states])
    done = False
    
    while not done:
        # Seleziona l'azione
        action = dqn_agent_and_model.select_action(state,epsilon=epsilon, temp=temp)
        observation, reward, terminated, truncated, info = env.step(action)
        next_state = np.reshape(observation, [1, dqn_agent_and_model.n_states])
        #replay_buffer.push(state, action, next_state, reward, terminated)
        dqn_agent_and_model.remember(state, action, reward, next_state, terminated)

        if len(dqn_agent_and_model.replay_buffer) >= batch_size:
            dqn_agent_and_model.replay(batch_size)
        
        if terminated:
            break
        state = next_state
            

env.close()


