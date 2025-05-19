# Building Agents with Reinforcement Learning

## Introduction

In artificial intelligence, an agent is an entity that perceives its environment through sensors and acts upon it to achieve specific goals. Reinforcement Learning (RL) is a subfield of machine learning where an agent learns to make decisions by interacting with an environment, receiving feedback in the form of rewards or penalties. The agent’s objective is to maximize the cumulative reward over time, learning optimal behaviors through trial and error.

RL has transformative applications, including:

- **Game Playing**: Systems like AlphaGo, which defeated world champions in Go.
- **Robotics**: Robots learning to navigate or manipulate objects.
- **Autonomous Vehicles**: Cars optimizing driving strategies.
- **Recommendation Systems**: Personalizing content delivery.

This tutorial provides a step-by-step guide to understanding RL and building agents, suitable for beginners with basic machine learning knowledge.

## Key Concepts in Reinforcement Learning

RL is built on several foundational concepts that define how agents learn:

- **States (S)**: Representations of the environment’s current situation. For example, in a game, the state might be the positions of all pieces on a board.
- **Actions (A)**: The set of possible moves or decisions the agent can make, such as moving left or right in a game.
- **Rewards (R)**: Numerical feedback from the environment, indicating the success of an action (e.g., `+1` for a good move, `-1` for a mistake).
- **Markov Decision Processes (MDPs)**: A mathematical framework where the next state and reward depend only on the current state and action, formalized as a tuple `(S, A, P, R, γ)`, where `P` is the transition probability and `γ` is the discount factor.
- **Policies (π)**: Strategies that map states to actions, either deterministic (choosing one action) or stochastic (assigning probabilities to actions).
- **Value Functions**: Estimates of expected future rewards:
  - **State-Value Function (V(s))**: Expected reward starting from state `s`, following policy `π`.
  - **Action-Value Function (Q(s,a))**: Expected reward starting from state `s`, taking action `a`, then following `π`.
- **Exploration vs. Exploitation**: The agent must balance trying new actions (exploration) to discover their effects and choosing known rewarding actions (exploitation). Techniques like epsilon-greedy (choosing random actions with probability `ε`) address this tradeoff.
- **Bellman Equations**: Recursive equations that express value functions in terms of immediate rewards and future values, forming the basis for many RL algorithms.

These concepts are critical for understanding how RL agents learn optimal behaviors.

## Value-Based Methods

Value-based methods estimate the value of states or state-action pairs to derive an optimal policy.

### Q-Learning

Q-Learning is a model-free, off-policy RL algorithm that learns the optimal action-value function `Q(s,a)` by updating a Q-table based on observed rewards and future estimates. The update rule is derived from the Bellman equation:

```
Q(s,a) <- Q(s,a) + α ( r + γ max_{a'} Q(s',a') - Q(s,a) )
```

Where:

- `α` is the learning rate.
- `γ` is the discount factor.
- `r` is the reward.
- `s’` is the next state.

Here’s a Python implementation of Q-Learning for the CartPole environment:

```python
import gym
import numpy as np

env = gym.make('CartPole-v1')
state_space = 100  # Discretized state space
action_space = env.action_space.n
Q = np.zeros((state_space, action_space))
alpha, gamma, epsilon = 0.1, 0.99, 0.1
num_episodes = 1000

def discretize_state(state):
    return min(int(state[2] * 10), state_space - 1)  # Simplified discretization

def choose_action(state, Q, epsilon):
    if np.random.random() < epsilon:
        return env.action_space.sample()
    return np.argmax(Q[state])

for episode in range(num_episodes):
    state = env.reset()
    state = discretize_state(state)
    done = False
    while not done:
        action = choose_action(state, Q, epsilon)
        next_state, reward, done, _ = env.step(action)
        next_state = discretize_state(next_state)
        Q[state, action] += alpha * (reward + gamma * np.max(Q[next_state]) - Q[state, action])
        state = next_state
env.close()
```

This code trains an agent to balance a pole by discretizing the state space and updating the Q-table.

### Deep Q-Networks (DQN)

For environments with large or continuous state spaces, Deep Q-Networks (DQN) use neural networks to approximate the Q-function. DQNs incorporate techniques like experience replay and target networks to stabilize learning. They’re effective in complex tasks like playing Atari games.

Using Stable Baselines3, you can implement a DQN easily:

```python
from stable_baselines3 import DQN

model = DQN('MlpPolicy', 'CartPole-v1', verbose=1)
model.learn(total_timesteps=10000)
```

This trains a DQN agent to balance the CartPole, leveraging a multi-layer perceptron policy.

## Policy-Based Methods

Policy-based methods directly optimize the policy `π(a|s)` without estimating value functions.

### Policy Gradient

Policy Gradient methods adjust the policy parameters (e.g., neural network weights) in the direction that increases expected rewards. The gradient of the expected reward is computed to update the policy.

### REINFORCE Algorithm

The REINFORCE algorithm is a simple policy gradient method that updates the policy based on the total reward of an episode. It uses the following update rule:

```
∇θ J(θ) = E [ Σ_t ∇θ log πθ(a_t|s_t) G_t ]
```

Where `G_t` is the discounted return from time `t`.

Here’s an implementation using PyTorch:

```python
import gym
import torch
import torch.nn as nn
import numpy as np

class PolicyNetwork(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(PolicyNetwork, self).__init__()
        self.fc = nn.Linear(state_dim, 128)
        self.action_head = nn.Linear(128, action_dim)

    def forward(self, x):
        x = torch.relu(self.fc(x))
        action_probs = torch.softmax(self.action_head(x), dim=-1)
        return action_probs

env = gym.make('CartPole-v1')
state_dim = env.observation_space.shape[0]
action_dim = env.action_space.n
policy = PolicyNetwork(state_dim, action_dim)
optimizer = torch.optim.Adam(policy.parameters(), lr=0.01)
gamma = 0.99
num_episodes = 1000

for episode in range(num_episodes):
    state = env.reset()
    log_probs = []
    rewards = []
    done = False
    while not done:
        state_tensor = torch.from_numpy(state).float()
        action_probs = policy(state_tensor)
        action = np.random.choice(action_dim, p=action_probs.detach().numpy())
        log_prob = torch.log(action_probs[action])
        next_state, reward, done, _ = env.step(action)
        log_probs.append(log_prob)
        rewards.append(reward)
        state = next_state

    returns = []
    R = 0
    for r in rewards[::-1]:
        R = r + gamma * R
        returns.insert(0, R)

    loss = 0
    for log_prob, R in zip(log_probs, returns):
        loss -= log_prob * R
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
env.close()
```

This code trains a policy network to maximize rewards in CartPole.

## Practical Implementation

### Setting Up the Environment

**OpenAI Gym** provides standardized environments for RL research. Install it with:

```bash
pip install gym
```

Create an environment:

```python
import gym
env = gym.make('CartPole-v1')
state = env.reset()
```

### Using RL Libraries

For complex tasks, Stable Baselines3 offers robust implementations of RL algorithms. Install it with:

```bash
pip install stable-baselines3
```

The DQN example above demonstrates its ease of use.

### Example: Q-Learning on Cat-Mouse-Cheese

Inspired by a tutorial on GitHub, consider a 2D grid where a mouse navigates to cheese while avoiding a cat. Rewards are:

- **-100**: Cat eats mouse.
- **+50**: Mouse eats cheese.
- **-1**: Default step.

Parameters:

- **Alpha**: 0.1
- **Gamma**: 0.9
- **Epsilon**: 0.1

The mouse learns to navigate efficiently after thousands of episodes, demonstrating Q-Learning’s effectiveness.

## Advanced Topics

### Multi-Agent RL

In multi-agent RL, multiple agents interact in the same environment, either cooperating (e.g., team games) or competing (e.g., chess). This introduces complexity, as each agent’s actions affect others. The Hugging Face course covers this in Unit 7, exploring soccer-playing agents.

### Deep RL in Complex Environments

Deep RL combines RL with deep learning to handle high-dimensional inputs, like images from video games. DQNs and policy gradient methods are often used in environments like Atari or Doom, as seen in the Hugging Face course’s VizDoom tasks.

## Resources for Further Learning

To deepen your RL knowledge, explore these resources:

### Online Courses and Tutorials

| Course/Tutorial | Provider | Description | URL |
| --- | --- | --- | --- |
| **Deep RL Course** | Hugging Face | Free, open-source, hands-on with environments like Lunar Lander and Doom. | [Hugging Face](https://huggingface.co/learn/deep-rl-course) |
| **Reinforcement Learning Specialization** | Coursera/University of Alberta | Comprehensive, covering MDPs, Q-Learning, and real-world applications. | [Coursera](https://www.coursera.org/specializations/reinforcement-learning) |
| **RL Lecture Series** | DeepMind x UCL | Free YouTube series on RL theory, from dynamic programming to deep RL. | [YouTube](https://www.youtube.com/playlist?list=PLqYmG7hTraZBiG_XpjnPrSNw-1XQaM_gB) |
| **RL Course** | FreeCodeCamp | Practical tutorial with Q-Learning, DQN, and policy gradients using PyTorch. | [YouTube](https://www.youtube.com/watch?v=2Hvj64QYQJQ) |
| **Intro to Game AI and RL** | Kaggle | Focuses on game AI, including minimax and RL techniques. | [Kaggle](https://www.kaggle.com/learn/intro-to-game-ai-and-reinforcement-learning) |

### GitHub Repositories

| Repository | Description | URL |
| --- | --- | --- |
| **dennybritz/reinforcement-learning** | Implementations of RL algorithms with exercises from Sutton’s book. | [GitHub](https://github.com/dennybritz/reinforcement-learning) |
| **tsmatz/reinforcement-learning-tutorials** | Theoretical explanations and Python code for model-free RL algorithms. | [GitHub](https://github.com/tsmatz/reinforcement-learning-tutorials) |
| **vmayoral/basic_reinforcement_learning** | Step-by-step RL tutorials, including Q-Learning examples. | [GitHub](https://github.com/vmayoral/basic_reinforcement_learning) |
| **omerbsezer/Reinforcement_learning_tutorial_with_demo** | Demos for dynamic programming, Monte Carlo, and Q-Learning. | [GitHub](https://github.com/omerbsezer/Reinforcement_learning_tutorial_with_demo) |

### Books

- *Reinforcement Learning: An Introduction* by Richard S. Sutton and Andrew G. Barto: The definitive RL textbook, covering theory and algorithms.
- *Deep Reinforcement Learning Hands-On* by Maxim Lapan: Practical guide with code examples for deep RL.

## Conclusion

Building agents with reinforcement learning involves understanding core concepts like states, actions, and rewards, and applying algorithms like Q-Learning and policy gradients. By leveraging tools like OpenAI Gym and Stable Baselines3, you can create agents for diverse applications, from games to robotics. The resources listed provide a robust foundation for both beginners and advanced learners, enabling you to explore RL’s potential further.

