import os

run_cmd = "python bandit.py "
instances = ["../instances/i-1.txt", "../instances/i-2.txt", "../instances/i-3.txt"]
epsilon = [0.02]
algorithm = ["epsilon-greedy", "ucb", "kl-ucb", "thompson-sampling", "thompson-sampling-with-hint"]
horizon = [100, 400, 1600, 6400, 25600, 102400]
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
					run_cmd5 = run_cmd5 + ">> outputDataT1.txt"
					os.system(run_cmd5)

run_cmd = "python bandit.py "
instances = ["../instances/i-1.txt", "../instances/i-2.txt", "../instances/i-3.txt"]
epsilon = [0.02]
algorithm = ["thompson-sampling", "thompson-sampling-with-hint"]
horizon = [100, 400, 1600, 6400, 25600, 102400]
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
					run_cmd5 = run_cmd5 + ">> outputDataT2.txt"
					os.system(run_cmd5)