import randomGen
import numpy as np

def thompson_sampling(instance, randomSeed, horizon):

	regret_gen = randomGen.regretGenerator(randomSeed=randomSeed, instance=instance)
	num_instances = len(regret_gen.instance)

	regret = regret_gen.get_optimal_reward(horizon)
	
	np.random.seed(randomSeed)

	beta_samples = [0] * num_instances
	num_success = [0] * num_instances
	num_fail = [0] * num_instances

	for iter in range(horizon):

		for j in range(num_instances):
			beta_samples[j] = np.random.beta(a=num_success[j]+1, b=num_fail[j]+1)

		samp_arm = beta_samples.index(max(beta_samples))

		reward = regret_gen.get_pull_reward(samp_arm)
		regret -= reward

		num_success[samp_arm] += reward
		num_fail[samp_arm] += 1 - reward

	return regret