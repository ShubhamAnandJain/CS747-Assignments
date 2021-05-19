import read_mdp
import numpy as np

def value_iteration(mdp_location):

	[n, a, end, adj, reward, gamma] = read_mdp.read_mdp(mdp_location)
	
	v = np.zeros(n)
	pi = np.zeros(n)
	v_last = np.zeros(n)

	v.fill(-10000)

	while(True):
		v_last = np.copy(v)

		for i in range(n):
			for ac in range(a):
				val = np.sum(adj[i][ac] * (reward[i][ac] + gamma * v_last))
				if val > v[i] - 1e-8:
					pi[i] = ac
					v[i] = max(v[i], val)

		if(np.sum(abs(v-v_last)) < 1e-8):
			break

	return [v, pi]