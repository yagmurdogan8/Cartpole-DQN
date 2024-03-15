#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Practical for course 'Reinforcement Learning',
Leiden University, The Netherlands
By Thomas Moerland
"""

import numpy as np
import time

from CartPoleDQN import dqn
from Helper import LearningCurvePlot, smooth

def average_over_repetitions(n_repetitions, n_timesteps, max_episode_length, learning_rate, gamma, policy='egreedy', 
                    epsilon=None, temp=None, smoothing_window=None, eval_interval=500):

    returns_over_repetitions = []
    now = time.time()
    
    for rep in range(n_repetitions): # Loop over repetitions
        
        returns, timesteps = dqn(n_timesteps, learning_rate, gamma, policy, epsilon, temp, eval_interval)
        returns_over_repetitions.append(returns)
        print("I have returned: ", returns)
        
    print('Running one setting takes {} minutes'.format((time.time()-now)/60))
    print("I have this returnsssss: ",returns_over_repetitions)
    learning_curve = np.mean(np.array(returns_over_repetitions),axis=0) # average over repetitions  
    if smoothing_window is not None: 
        learning_curve = smooth(learning_curve,smoothing_window) # additional smoothing
    return learning_curve, timesteps  

def experiment():
    ####### Settings
    # Experiment      
    n_repetitions = 2
    smoothing_window = 9 # Must be an odd number. Use 'None' to switch smoothing off!
        
    # MDP    
    n_timesteps = 1001 # Set one extra timestep to ensure evaluation at start and end
    eval_interval = 500
    max_episode_length = 100
    gamma = 0.95
    
    # Parameters we will vary in the experiments, set them to some initial values: 
    # Exploration
    policy = 'egreedy' # 'egreedy' or 'softmax' 
    epsilon = 0.05
    temp = 0.99
    # Back-up & update
    learning_rate = 0.1
    
    Plot = LearningCurvePlot(title = r'Annealing: $\epsilon$-greedy and softmax with decaying parameters')    
    Plot.set_ylim(-100, 100) 
    learning_curve, timesteps = average_over_repetitions(n_repetitions, n_timesteps, max_episode_length, learning_rate, 
                                          gamma, policy, epsilon, temp, smoothing_window, eval_interval)
    
    Plot.add_curve(timesteps,learning_curve,label=r'$\epsilon$-greedy, $\epsilon $ = {}'.format(epsilon))
    
    Plot.save('dqn.png')
    
    
    # for epsilon in epsilons:        
    #     learning_curve, timesteps = average_over_repetitions(backup, n_repetitions, n_timesteps, max_episode_length, learning_rate, 
    #                                           gamma, policy, epsilon, temp, smoothing_window, eval_interval)
    #     Plot.add_curve(timesteps,learning_curve,label=r'$\epsilon$-greedy, $\epsilon $ = {}'.format(epsilon))    
    # policy = 'softmax'
    # # temps = [0.01,0.1,1.0]
    # temps = [0.9]
    # for temp in temps:
    #     learning_curve, timesteps = average_over_repetitions(backup, n_repetitions, n_timesteps, max_episode_length, learning_rate, 
    #                                           gamma, policy, epsilon, temp, smoothing_window, eval_interval)
    #     Plot.add_curve(timesteps,learning_curve,label=r'softmax, $ \tau $ = {}'.format(temp))
    # Plot.add_hline(optimal_episode_return, label="DP optimum")
    # Plot.save('qlearning_lr_09.png')

    ###### Assignment 3: Q-learning versus SARSA
    policy = 'softmax'
    # temp = 0.8
    # epsilon = 0.1 # set epsilon back to original value 
    # learning_rates = [0.03,0.1,0.3]
    # backups = ['q','sarsa']
    # Plot = LearningCurvePlot(title = 'Back-up: on-policy versus off-policy')    
    # Plot.set_ylim(-100, 100) 
    # for backup in backups:
    #     for learning_rate in learning_rates:
    #         learning_curve, timesteps = average_over_repetitions(backup, n_repetitions, n_timesteps, max_episode_length, learning_rate, 
    #                                           gamma, policy, epsilon, temp, smoothing_window, plot, n, eval_interval)
    #         Plot.add_curve(timesteps,learning_curve,label=r'{}, $\alpha$ = {} '.format(backup_labels[backup],learning_rate))
    # Plot.add_hline(optimal_episode_return, label="DP optimum")
    # Plot.save('sarsa_qlearning_softmax_temp_08.png') 
    
    # ##### Assignment 4: Back-up depth
    # policy = 'egreedy'
    # policy = 'softmax'
    # temp = 0.1
    # gamma = 0.90
    # epsilon = 0.05 # set epsilon back to original value
    # learning_rate = 0.1
    # backup = 'nstep'
    # ns = [1,3,10]
    # Plot = LearningCurvePlot(title = 'Back-up: depth')   
    # Plot.set_ylim(-100, 100) 
    # for n in ns:
    #     learning_curve, timesteps = average_over_repetitions(backup, n_repetitions, n_timesteps, max_episode_length, learning_rate, 
    #                                         gamma, policy, epsilon, temp, smoothing_window, plot, n, eval_interval)
    #     Plot.add_curve(timesteps,learning_curve,label=r'{}-step Q-learning'.format(n))
    # backup = 'mc'
    # learning_curve, timesteps = average_over_repetitions(backup, n_repetitions, n_timesteps, max_episode_length, learning_rate, 
    #                                     gamma, policy, epsilon, temp, smoothing_window, plot, n, eval_interval)
    # Plot.add_curve(timesteps,learning_curve,label='Monte Carlo')        
    # Plot.add_hline(optimal_episode_return, label="DP optimum")
    # Plot.save('softmax_temp_01_lr_01.png')

if __name__ == '__main__':
    experiment()
