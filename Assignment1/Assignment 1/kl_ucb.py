import randomGen
import numpy as np

def kl_div(p, q):

	if(abs(p-q)<1e-9):
		return 0
	if(abs(1-q)<1e-9):
		return 1000000
	if(abs(p)<1e-9):
		return np.log(1/(1-q))

	return p * np.log(p / q) + (1 - p) * np.log ((1 - p) / (1 - q))

def bsearch(l, r, p, u, val):
	if(r-l < 2e-4):
		return r
	
	mid = (l*1.0 + r) / 2
	
	if(u * kl_div(p, mid) > val): 
		r = mid
	else:
		l = mid

	return bsearch(l, r, p, u, val)

def kl_ucb(instance, randomSeed, horizon):

	regret_gen = randomGen.regretGenerator(randomSeed=randomSeed, instance=instance)
	num_instances = len(regret_gen.instance)

	regret = regret_gen.get_optimal_reward(horizon)
	
	kl_ucb = [1000000] * num_instances
	num_pulls = [0] * num_instances
	num_rewards = [0] * num_instances

	for iter in range(horizon):

		samp_arm = kl_ucb.index(max(kl_ucb))

		reward = regret_gen.get_pull_reward(samp_arm)
		regret -= reward

		num_rewards[samp_arm] += reward
		num_pulls[samp_arm] += 1

		if iter < num_instances:
			kl_ucb[samp_arm] = 0
			continue

		for j in range(num_instances):
			if(num_pulls[j] == 0):
				continue

			bounding_val = np.log(iter+1) + 3 * np.log(np.log(iter+1))
			emp_mean = (num_rewards[j]*1.0)/num_pulls[j]
			
			kl_ucb[j] = bsearch(l=emp_mean, r=1, p=emp_mean, u=num_pulls[j], val=bounding_val)

	return regret