import randomGen
import numpy as np
import math

def thompson_sampling_hint(instance, randomSeed, horizon, instanceVals):

	regret_gen = randomGen.regretGenerator(randomSeed=randomSeed, instance=instance)
	num_instances = len(regret_gen.instance)

	regret = regret_gen.get_optimal_reward(horizon)
	
	np.random.seed(randomSeed)

	beta_samples = [0] * num_instances
	num_success = [0] * num_instances
	num_fail = [0] * num_instances

	weight_arr = [[1.0/num_instances for i in range(num_instances)] for j in range(num_instances)]	

	for iter in range(horizon):

		max_val = -1
		samp_arm = -1

		arm_choices = []

		for arm in range(num_instances):
			
			a = num_success[arm] + 1
			b = num_fail[arm] + 1

			total = 0
			prob_vals = []
			arm_choices.append(weight_arr[arm][num_instances-1])
		
		samp_arm = arm_choices.index(max(arm_choices))

		reward = regret_gen.get_pull_reward(samp_arm)
		regret -= reward

		num_success[samp_arm] += reward
		num_fail[samp_arm] += 1 - reward
		tot_wt = 0.0

		for inst in range(num_instances):
			if(reward == 1):
				weight_arr[samp_arm][inst] *= instanceVals[inst]
			else:
				weight_arr[samp_arm][inst] *= (1.0-instanceVals[inst])

			tot_wt += weight_arr[samp_arm][inst]

		for inst in range(num_instances):
			weight_arr[samp_arm][inst] /= tot_wt

	return regret