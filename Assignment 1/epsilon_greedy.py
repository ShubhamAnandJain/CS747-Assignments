import randomGen
import numpy as np

def epsilon_greedy(instance, randomSeed, horizon, epsilon):

	regret_gen = randomGen.regretGenerator(randomSeed=randomSeed, instance=instance)
	num_instances = len(regret_gen.instance)
	np.random.seed(randomSeed)

	regret = regret_gen.get_optimal_reward(horizon)

	emp_mean = [1] * num_instances
	num_pulls = [0] * num_instances
	num_rewards = [0] * num_instances

	for iter in range(horizon):

		should_sample = np.random.binomial(n=1, p=epsilon)
		samp_arm = 0

		if(should_sample):

			samp_arm = np.random.randint(0, num_instances)

		else:

			samp_arm = emp_mean.index(max(emp_mean))

		reward = regret_gen.get_pull_reward(samp_arm)
		regret -= reward

		num_rewards[samp_arm] += reward
		num_pulls[samp_arm] += 1
		emp_mean[samp_arm] = (num_rewards[samp_arm] * 1.0) / num_pulls[samp_arm]

	return regret