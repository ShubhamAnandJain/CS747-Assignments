import numpy as np

def read_mdp(mdp_location):

	file = open(mdp_location, "r");
	lines = file.readlines();
	n = int(lines[0].split(" ")[1])
	a = int(lines[1].split(" ")[1])
	
	adj = np.zeros((n,a,n))
	reward = np.zeros((n,a,n))

	end = []
	gamma = 0

	for line_iter in lines:
		line_split = line_iter.split(" ")

		if(line_split[0] == "end"):
			for end_iter in line_split:
				if(end_iter == "end"):
					continue
				if(int(end_iter) != -1):
					end.append(int(end_iter))

		if(line_split[0] == "transition"):
			
			s1 = int(line_split[1])
			ac = int(line_split[2])
			s2 = int(line_split[3])
			r = float(line_split[4])
			p = float(line_split[5])

			adj[s1][ac][s2] = p
			reward[s1][ac][s2] = r

		if(line_split[0] == "discount"):
			gamma = float(line_split[2])

	return [n, a, end, adj, reward, gamma]