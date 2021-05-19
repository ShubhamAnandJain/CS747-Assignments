import numpy as np
import random

#This file generates the regret for one armpull
#This is used across all instances
#It is assumed that the arm pulls are sampled from bernoulli distributions

class regretGenerator:

	def __init__(self, randomSeed, instance):
		np.random.seed(randomSeed)
		
		read_instance = open(instance, "r")
		num_instance = read_instance.readlines()

		self.instance = [float(i) for i in num_instance]
		self.optimal = max(self.instance)
		
		return 

	def get_pull_reward(self, armPulled):
		reward = np.random.binomial(n=1, p=self.instance[armPulled])
		return reward

	def get_optimal_reward(self, horizon):
		return self.optimal * horizon