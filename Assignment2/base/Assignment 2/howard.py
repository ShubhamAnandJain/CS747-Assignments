import read_mdp
import numpy as np

def howard_iteration(mdp_location):

	[n, a, end, adj, reward, gamma] = read_mdp.read_mdp(mdp_location)
	
	v = np.zeros(n)
	pi = np.zeros(n)
	zero_vals = len(end)
	marked_zero = np.zeros(n)

	for i in range(n):
		marked_zero[i] = int(0)
	
	for zero_pos in end:
		marked_zero[zero_pos] = 1

	map_to = np.zeros(n)
	state_no = 0

	for i in range(n):
		if(marked_zero[i] == 1):
			map_to[i] = -1
			continue
		map_to[i] = state_no
		state_no += 1

	while(True):
		changed = 0

		A = np.zeros((n-zero_vals, n-zero_vals))
		B = np.zeros(n-zero_vals)

		for i in range(n):
			ni = int(map_to[i])
			if(marked_zero[i] == 1):
				continue
			ac = int(pi[i])
			for j in range(n):
				nj = int(map_to[j])
				if(marked_zero[j] == 1):
					continue
				A[ni][nj] = - gamma * adj[i][ac][j]
			A[ni][ni] += 1.0

		for i in range(n):
			ac = int(pi[i])
			ni = int(map_to[i])
			if(marked_zero[i] == 1):
				continue
			val = np.sum(adj[i][ac] * reward[i][ac])
			B[ni] = val

		C = np.linalg.solve(A, B)

		for i in range(n):
			if(marked_zero[i] == 1):
				v[i] = 0
				continue
			ni = int(map_to[i])
			v[i] = C[ni]

		for i in range(n):
			if(marked_zero[i] == 1):
				continue
			for ac in range(a):
				val = np.sum(adj[i][ac] * (reward[i][ac] + gamma * v))
				if val > v[i]+1e-8:
					pi[i] = ac
					changed += 1

		if(changed == 0):
			break

	return [v, pi]