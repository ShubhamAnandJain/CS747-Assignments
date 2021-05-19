import read_mdp
import numpy as np
import pulp as pl

def linear_program(mdp_location):

	[n, a, end, adj, reward, gamma] = read_mdp.read_mdp(mdp_location)
	
	v = np.zeros(n)
	pi = np.zeros(n)
	v_last = np.zeros(n)
	const_constraint = {}
	mul_constraint = {}
	lp_names = {}

	prob = pl.LpProblem('SolveMDP', pl.LpMaximize)

	for state in range(n):
		lp_names[state] = 0.0

	lp_vars = pl.LpVariable.dicts("V", lp_names, cat="Continuous")

	prob += pl.lpSum(-lp_vars[i] for i in range(n))

	for state in range(n):
		for actions in range(a):
			prob += lp_vars[state] >= np.sum(adj[state][actions]*reward[state][actions]) + pl.lpSum(gamma * adj[state][actions][state2] * lp_vars[state2] for state2 in range(n))
	
	prob.solve(pl.PULP_CBC_CMD(msg=0))	

	for state in range(n):
		v[state] = pl.value(lp_vars[state])

	for state in range(n):
		closest_val = -1e9
		for action in range(a):
			val = np.sum(adj[state][action] * (reward[state][action] + gamma * v))
			if(abs(val-v[state])<abs(closest_val-v[state])):
				pi[state] = action
				closest_val = val

	return [v, pi]