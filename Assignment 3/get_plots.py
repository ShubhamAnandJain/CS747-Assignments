import argparse
import os
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Take in Windy Gridworld Inputs to plot')
parser.add_argument('--stochastic', action='store', type=lambda x: bool(int(x)),
					required=True, help='is wind stochastic')
parser.add_argument('--kingmove', action='store', type=lambda x: bool(int(x)),
					required=True, help='should kingmove be considered')
parser.add_argument('--episodes', action='store', type=int,
					required=True, help='number of episodes to run for')
parser.add_argument('--iter', action='store', type=int,
					required=True, help='number of iters to average over')
parser.add_argument('--epsilon', action='store', type=float,
					required=True, help='epsilon value for epsilon-greedy')
parser.add_argument('--alpha', action='store', type=float,
					required=True, help='alpha value for bootstrap updates')

args = parser.parse_args()

algorithms = ['sarsa0', 'q_learning', 'expected_sarsa']

run_cmd = "python3 windy_gridworld.py"

for alg in algorithms:

	file_name = "output_data_" + alg + ".txt"

	if(os.path.exists(file_name)):
		os.remove(file_name)

	run_cmd1 = run_cmd
	run_cmd1 = run_cmd1 + " --algorithm " + alg + " --stochastic " + str(int(args.stochastic))
	run_cmd1 = run_cmd1 + " --kingmove " + str(int(args.kingmove)) + " --episodes " + str(args.episodes)
	run_cmd1 = run_cmd1 + " --epsilon " + str(args.epsilon) + " --alpha " + str(args.alpha)
	for i in range(args.iter):
		run_cmd2 = run_cmd1 + " --randomSeed " + str(i)
		run_cmd2 = run_cmd2 + " >> " + file_name
		os.system(run_cmd2)


ans_dict = {}

for alg in algorithms:
	file_name = "output_data_" + alg + ".txt"
	read_data = open(file_name, "r")
	num_data = read_data.readlines()

	for line in num_data:
		single_line_data = line.split(' ')
		hashed_str = alg + single_line_data[1][:-1]

		if ans_dict.get(hashed_str) is None:
			ans_dict[hashed_str] = 0

		ans_dict[hashed_str] += float(single_line_data[0]) / args.iter

# print(ans_dict)

for alg in algorithms:
	x = []
	y = []
	x.append(0)
	y.append(0)
	for i in range(args.episodes):
		hashed_str = alg + str(i+1)
		x.append(ans_dict[hashed_str])
		y.append(i+1)
	plt.plot(x, y)

plt_name = "Performance of agents with "
if((args.stochastic == 0) and (args.kingmove == 0)):
	plt_name += "no stochasticity or king moves"
elif((args.stochastic == 1) and (args.kingmove == 1)):
	plt_name += "both stochasticity and king moves"
elif((args.stochastic == 1) or (args.kingmove == 1)):
	if(args.stochastic == 1):
		plt_name += "stochasticity"
	else:
		plt_name += "king moves"

plt.title(plt_name)
plt.xlabel('Timesteps')
plt.ylabel('Number of episodes')
plt.legend(algorithms, loc="upper left")
file_name = "stoc"+str(args.stochastic)+"kingmove"+str(args.kingmove)+".png"
plt.savefig(file_name)
# plt.show()