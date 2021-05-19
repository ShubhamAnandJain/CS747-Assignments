import argparse
import sarsa0
import expected_sarsa
import q_learning


parser = argparse.ArgumentParser(description='Take in Windy Gridworld Inputs')
parser.add_argument('--algorithm', action='store', type=str,
					required=True, help='algorithm for bootstrapping')
parser.add_argument('--stochastic', action='store', type=lambda x: bool(int(x)),
					required=True, help='is wind stochastic')
parser.add_argument('--kingmove', action='store', type=lambda x: bool(int(x)),
					required=True, help='should kingmove be considered')
parser.add_argument('--episodes', action='store', type=int,
					required=True, help='number of episodes to run for')
parser.add_argument('--randomSeed', action='store', type=int,
					required=True, help='random seed for rngs')
parser.add_argument('--epsilon', action='store', type=float,
					required=True, help='epsilon value for epsilon-greedy')
parser.add_argument('--alpha', action='store', type=float,
					required=True, help='alpha value for bootstrap updates')

args = parser.parse_args()

# algorithm is one of sarsa0, expected_sarsa, q_learning
# if stochastic is 1, wind is stochastic
# if kingmove is 1, moves will be in 8 directions instead of 4
# episodes tells us the number of episodes

if(args.algorithm == 'sarsa0'):
	[timesteps, episodes] = sarsa0.sarsa0(stochastic=args.stochastic, kingmove=args.kingmove,
										  num_episodes=args.episodes, seed=args.randomSeed,
										  epsilon=args.epsilon, alpha=args.alpha)

if(args.algorithm == 'q_learning'):
	[timesteps, episodes] = q_learning.q_learning(stochastic=args.stochastic, kingmove=args.kingmove,
										  num_episodes=args.episodes, seed=args.randomSeed,
										  epsilon=args.epsilon, alpha=args.alpha)

if(args.algorithm == 'expected_sarsa'):
	[timesteps, episodes] = expected_sarsa.expected_sarsa(stochastic=args.stochastic, kingmove=args.kingmove,
										  num_episodes=args.episodes, seed=args.randomSeed,
										  epsilon=args.epsilon, alpha=args.alpha)

for i in range(len(timesteps)):
	print(str(timesteps[i]) + " " + str(episodes[i]))