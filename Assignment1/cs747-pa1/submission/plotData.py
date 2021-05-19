import matplotlib.pyplot as plt
import numpy as np

fileToPlot = "outputDataT1.txt"
instanceToPlot = ["../instances/i-1.txt", "../instances/i-2.txt", "../instances/i-3.txt"]
algorithms = ["epsilon-greedy", "ucb", "kl-ucb", "thompson-sampling"]
horizons = [100, 400, 1600, 6400, 25600, 102400]

read_data = open(fileToPlot, "r")
num_data = read_data.readlines()

sampdict = {}

for line in num_data:

	single_line_data = line.split(',')
	hashed_str = single_line_data[0] + single_line_data[1] + str(single_line_data[-2])

	if sampdict.get(hashed_str) is None:
		sampdict[hashed_str] = 0

	sampdict[hashed_str] += float(single_line_data[-1])/50.0

for inst in instanceToPlot:
	for alg in algorithms:

		x = []
		y = []

		for hor in horizons:
			curr_hash = inst+" "+alg+" "+str(hor)
			x.append(hor)
			y.append(sampdict[curr_hash])

		plt.plot(x, y)

	plt.title('Output for instance '+inst[-7:-4])
	plt.xlabel('Horizon (log scale)')
	plt.ylabel('Regret')
	plt.xscale('log')
	plt.legend(algorithms, loc="upper left")
	file_name = fileToPlot[-6:-4]+inst[-7:-4]+"PlotData.png"
	print(file_name)
	plt.savefig(file_name)
	plt.show()
	# plt.close()
	