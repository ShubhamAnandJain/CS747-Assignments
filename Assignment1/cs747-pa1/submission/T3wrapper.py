import os
import numpy as np

run_cmd = "python bandit.py "
instances = ["../instances/i-1.txt", "../instances/i-2.txt", "../instances/i-3.txt"]
epsilon = np.linspace(0.001,0.009,9).tolist()
algorithm = ["epsilon-greedy"]
horizon = [102400]
randomSeed = list(range(50))

for instance in instances:
	run_cmd1 = run_cmd + "--instance "+instance+" "
	for eps in epsilon:
		run_cmd2 = run_cmd1 + "--epsilon "+str(eps)+" "
		for alg in algorithm:
			run_cmd3 = run_cmd2 + "--algorithm "+alg+" "
			for hor in horizon:
				run_cmd4 = run_cmd3 + "--horizon "+str(hor)+" "
				for r in randomSeed:
					run_cmd5 = run_cmd4 + "--randomSeed "+str(r)+" "
					run_cmd5 = run_cmd5 + ">> outputDataT3.txt"
					os.system(run_cmd5)