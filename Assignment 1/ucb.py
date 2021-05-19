import randomGen
import numpy as np

def ucb(instance, randomSeed, horizon):

	regret_gen = randomGen.regretGenerator(randomSeed=randomSeed, instance=instance)
	num_instances = len(regret_gen.instance)

	regret = regret_gen.get_optimal_reward(horizon)
	
	ucb = [1000000] * num_instances
	num_pulls = [0] * num_instances
	num_rewards = [0] * num_instances

	for iter in range(horizon):

		samp_arm = ucb.index(max(ucb))

		reward = regret_gen.get_pull_reward(samp_arm)
		regret -= reward

		num_rewards[samp_arm] += reward
		num_pulls[samp_arm] += 1

		for j in range(num_instances):
			if(num_pulls[j] == 0):
				continue

			ucb[j] = (num_rewards[j] * 1.0) / num_pulls[j] + np.sqrt(2.0*np.log(iter+1)/num_pulls[j])

	return regret