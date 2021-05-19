import matplotlib.pyplot as plt
import numpy as np

fileToPlot = "outputDataT3.txt"
instanceToPlot = ["../instances/i-1.txt", "../instances/i-2.txt", "../instances/i-3.txt"]
algorithms = ["epsilon-greedy"]
horizons = [102400]

epsilon = np.linspace(0.001,0.009,9).tolist()
epsilon2 = np.linspace(0.01,0.10,10).tolist()
for eps in epsilon2:
	if(eps < 0.04): epsilon.append(eps)

read_data = open(fileToPlot, "r")
num_data = read_data.readlines()

sampdict = {}

for line in num_data:

	single_line_data = line.split(',')
	hashed_str = single_line_data[0] + single_line_data[1] + str(single_line_data[-3])

	if sampdict.get(hashed_str) is None:
		sampdict[hashed_str] = 0

	sampdict[hashed_str] += float(single_line_data[-1])/50.0

for inst in instanceToPlot:
	for alg in algorithms:

		x = []
		y = []

		for eps in epsilon:
			curr_hash = inst+" "+alg+" "+str(eps)
			x.append(eps)
			y.append(sampdict[curr_hash])

		plt.plot(x, y)

	plt.title('Output for instance '+inst[-7:-4])
	plt.xlabel('Epsilon')
	plt.ylabel('Regret')
	plt.legend(algorithms, loc="upper left")
	file_name = fileToPlot[-6:-4]+inst[-7:-4]+"PlotData.png"
	print(file_name)
	plt.savefig(file_name)
	plt.show()
	