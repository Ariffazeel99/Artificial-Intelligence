import gym
import numpy as np

# Create the environment
env = gym.make('CartPole-v1')

# Hyperparameters
learning_rate = 0.1
discount_factor = 0.95
epsilon = 1.0
epsilon_decay = 0.995
min_epsilon = 0.01
episodes = 1000

# Initialize the Q-table
state_space = env.observation_space.shape[0]
action_space = env.action_space.n
q_table = np.zeros((state_space, action_space))

# Define a function to choose an action using epsilon-greedy policy
def choose_action(state, q_table, epsilon):
    if np.random.uniform(0, 1) < epsilon:
        return np.random.choice(action_space)  # Explore
    else:
        return np.argmax(q_table[state, :])  # Exploit

# Update Q-values using the Q-learning formula
def update_q_table(q_table, state, action, reward, next_state, done, learning_rate, discount_factor):
    q_predict = q_table[state, action]
    if done:
        q_target = reward
    else:
        q_target = reward + discount_factor * np.max(q_table[next_state, :])
    q_table[state, action] = q_predict + learning_rate * (q_target - q_predict)

# Train the agent over episodes
for episode in range(episodes):
    state = env.reset()
    done = False
    total_reward = 0

    while not done:
        action = choose_action(state, q_table, epsilon)
        next_state, reward, done, info = env.step(action)
        
        update_q_table(q_table, state, action, reward, next_state, done, learning_rate, discount_factor)
        
        state = next_state
        total_reward += reward
    
    # Decay epsilon
    epsilon = max(min_epsilon, epsilon * epsilon_decay)
    
    if episode % 100 == 0:
        print(f'Episode {episode} - Total Reward: {total_reward}')

# Test the agent after training
state = env.reset()
done = False
while not done:
    env.render()
    action = np.argmax(q_table[state, :])
    state, reward, done, info = env.step(action)

env.close()
