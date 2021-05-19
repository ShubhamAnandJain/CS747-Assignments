import numpy as np
import matplotlib.pyplot as plt
import argparse
import sys,os,math
import copy
parser = argparse.ArgumentParser()
parser.add_argument("--instance", help="'instance' is a path to the instance file.",type=str)
parser.add_argument("--algorithm", help="al is one of epsilon-greedy, ucb, kl-ucb, thompson-sampling, and thompson-sampling-with-hint.",type=str)
parser.add_argument("--randomSeed", help="rs is a non-negative integer.",type=int)
parser.add_argument("--epsilon", help="ep is a number in [0, 1].",type=float)
parser.add_argument("--horizon", help="hz is a non-negative integer.",type=int)
args = parser.parse_args()

FILEPATH = sys.path[0] + "{0}".format(args.instance[2:])

Bandit_Instance = []
np.random.seed(args.randomSeed)
with open(FILEPATH,'r') as f:
	lines = f.readlines()
	for line in lines:
		Bandit_Instance.append(float(line.rstrip()))


class Epsilon:
	def __init__(self,Bandit_Instance,horizon,epsilon):
		self.no_of_arms = len(Bandit_Instance)
		self.curr_means = np.zeros(self.no_of_arms,dtype=float)
		self.curr_pulls = np.zeros(self.no_of_arms,dtype=int)
		self.curr_rewards = np.zeros(self.no_of_arms,dtype=float)
		self.Budget = horizon
		self.Epsilon = epsilon
		self.Total_Pulls = 0


	def pull(self):
		p = np.random.random()

		if(p<self.Epsilon):
			index =np.random.randint(0,self.no_of_arms)
		else:
			index = np.argmax(self.curr_means)

		self.Total_Pulls += 1
		self.curr_pulls[index] += 1
		Pull_reward = np.random.binomial(1,Bandit_Instance[index])
		self.curr_rewards[index] += Pull_reward
		self.curr_means[index] = self.curr_rewards[index]/self.curr_pulls[index]

	def start(self):
		for i in range(0,self.no_of_arms):
			self.Total_Pulls += 1
			self.curr_pulls[i] = 1
			self.curr_means[i] = np.random.binomial(1,Bandit_Instance[i]) # Binomial with n = 1 => Bernouli

	def Run_Epsilon(self):
		if(self.Budget<self.no_of_arms):
			for i in range(0,self.Budget): # DOUBT 
				self.Total_Pulls += 1
				self.curr_pulls[i] = 1
				self.curr_means[i] = np.random.binomial(1,Bandit_Instance[i]) # Binomial with n = 1 => Bernouli
		else:
			# self.start()
			for i in range(self.Total_Pulls,self.Budget):
				self.pull()

	def result(self):
		Cumulative_reward_REW = sum(self.curr_rewards)
		regret = max(Bandit_Instance)*self.Budget - Cumulative_reward_REW
		print("{0}, {1}, {2}, {3}, {4}, {5}\n".format(args.instance,args.algorithm, args.randomSeed, args.epsilon, args.horizon, regret))

class UCB:
	def __init__(self,Bandit_Instance,horizon):
		self.no_of_arms = len(Bandit_Instance)
		self.curr_means = np.zeros(self.no_of_arms,dtype=float)
		self.curr_pulls = np.zeros(self.no_of_arms,dtype=int)
		self.curr_rewards = np.zeros(self.no_of_arms,dtype=float)
		self.Budget = horizon
		self.Total_Pulls = 0

	def pull(self):
		ucb_max_index = np.argmax(self.curr_means + np.sqrt((2*np.log(self.Total_Pulls)) / self.curr_pulls))
		self.Total_Pulls += 1
		self.curr_pulls[ucb_max_index] += 1
		Pull_reward = np.random.binomial(1,Bandit_Instance[ucb_max_index])
		self.curr_rewards[ucb_max_index] += Pull_reward
		self.curr_means[ucb_max_index] = self.curr_rewards[ucb_max_index]/self.curr_pulls[ucb_max_index]


	def start(self):
		for i in range(0,self.no_of_arms):
			self.Total_Pulls += 1
			self.curr_pulls[i] = 1
			self.curr_means[i] = np.random.binomial(1,Bandit_Instance[i]) # Binomial with n = 1 => Bernouli

	def Run_UCB(self):
		if(self.Budget<self.no_of_arms):
			for i in range(0,self.Budget):
				self.Total_Pulls += 1
				self.curr_pulls[i] = 1
				self.curr_means[i] = np.random.binomial(1,Bandit_Instance[i]) # Binomial with n = 1 => Bernouli
		else:
			self.start()
			for i in range(self.Total_Pulls,self.Budget):
				self.pull()

	def result(self):
		Cumulative_reward_REW = sum(self.curr_rewards)
		print(self.curr_rewards)
		print(self.curr_means)
		print(self.curr_pulls)
		regret = max(Bandit_Instance)*self.Budget - Cumulative_reward_REW
		print("{0}, {1}, {2}, {3}, {4}, {5}\n".format(args.instance,args.algorithm, args.randomSeed, args.epsilon, args.horizon, regret))

class KL_UCB:
	def __init__(self,Bandit_Instance,horizon):
		self.no_of_arms = len(Bandit_Instance)
		self.curr_means = np.zeros(self.no_of_arms,dtype=float)
		self.curr_pulls = np.zeros(self.no_of_arms,dtype=int)
		self.curr_rewards = np.zeros(self.no_of_arms,dtype=float)
		self.Budget = horizon
		self.Total_Pulls = 0


	def KL_divergence(self,p, q):
		if(math.isclose(p,q,abs_tol = 1e-5)):
			return 0
		if(math.isclose(p,0,abs_tol = 1e-5)):
			return (1-p)*np.log((1-p)/(1-q))
		elif(math.isclose(q,1,abs_tol = 1e-5)):
			return p*np.log(p/q)
		else:
			return p*np.log(p/q) + (1-p)*np.log((1-p)/(1-q))

	def binarysearch(self,Lim,p_hat):
		left = p_hat
		right = 1.0
		while (abs(left-right)>1e-4):
			mid = (left+right)/2.0
			if(self.KL_divergence(p_hat,mid)<Lim):
				left = mid
			else:
				right = mid

		return right

	def compute_q(self,i,RHS):
		if(self.curr_means[i] == 1):
			return 1
		Lim = (RHS*1.0)/self.curr_pulls[i]
		return self.binarysearch(Lim,self.curr_means[i])

	def kl_ucb_max_index_generator(self):
		ucb_kl_t_a = []
		RHS = np.log(self.Total_Pulls) + 3*np.log(np.log(self.Total_Pulls))
		for i in range(0,self.no_of_arms):
			ucb_kl_t_a.append(self.compute_q(i,RHS))
		return np.argmax(ucb_kl_t_a)

	def pull(self):
		kl_ucb_max_index = self.kl_ucb_max_index_generator()
		self.Total_Pulls += 1
		self.curr_pulls[kl_ucb_max_index] += 1
		Pull_reward = np.random.binomial(1,Bandit_Instance[kl_ucb_max_index])
		self.curr_rewards[kl_ucb_max_index] += Pull_reward
		self.curr_means[kl_ucb_max_index] = self.curr_rewards[kl_ucb_max_index]/self.curr_pulls[kl_ucb_max_index]


	def start(self):
		for i in range(0,self.no_of_arms):
			self.Total_Pulls += 1
			self.curr_pulls[i] = 1
			self.curr_means[i] = np.random.binomial(1,Bandit_Instance[i]) # Binomial with n = 1 => Bernouli

	def Run_UCB(self):
		self.start()
		self.start()##ROUND ROBIN DONE TWICE
		for i in range(self.Total_Pulls,self.Budget):
			self.pull()

	def result(self):
		Cumulative_reward_REW = sum(self.curr_rewards)
		regret = max(Bandit_Instance)*self.Budget - Cumulative_reward_REW
		print("{0}, {1}, {2}, {3}, {4}, {5}\n".format(args.instance,args.algorithm, args.randomSeed, args.epsilon, args.horizon, regret))

class Thompson_Sampling:
	def __init__(self,Bandit_Instance,horizon):
		self.no_of_arms = len(Bandit_Instance)
		self.curr_means = np.zeros(self.no_of_arms,dtype=float)
		self.curr_pulls = np.zeros(self.no_of_arms,dtype=int)
		self.curr_rewards = np.zeros(self.no_of_arms,dtype=float)
		self.Budget = horizon
		self.Total_Pulls = 0

	def beta_dist(self):
		Betas = []
		for i in range(0,self.no_of_arms):
			S = self.curr_rewards[i]
			F = self.curr_pulls[i] - self.curr_rewards[i]
			Betas.append(np.random.beta(S+1,F+1))
		return np.argmax(Betas)

	def pull(self):
		beta_arm = self.beta_dist()
		self.Total_Pulls += 1
		self.curr_pulls[beta_arm] += 1
		Pull_reward = np.random.binomial(1,Bandit_Instance[beta_arm])
		self.curr_rewards[beta_arm] += Pull_reward
		self.curr_means[beta_arm] = self.curr_rewards[beta_arm]/self.curr_pulls[beta_arm]


	def start(self):
		for i in range(0,self.no_of_arms):
			self.Total_Pulls += 1
			self.curr_pulls[i] = 1
			self.curr_rewards[i] = np.random.binomial(1,Bandit_Instance[i]) # Binomial with n = 1 => Bernouli
			self.curr_means[i] = self.curr_rewards[i]
	def Run_Thompson_Sampling(self):
		if(self.Budget<self.no_of_arms):
			for i in range(0,self.Budget):
				self.Total_Pulls += 1
				self.curr_pulls[i] = 1
				self.curr_rewards[i] = np.random.binomial(1,Bandit_Instance[i]) # Binomial with n = 1 => Bernouli
				self.curr_means[i] = self.curr_rewards[i]
		else:
			# self.start() START NOT NEEDED HERE IN THIS CASE
			for i in range(self.Total_Pulls,self.Budget):
				self.pull()

	def result(self):
		Cumulative_reward_REW = sum(self.curr_rewards)
		regret = max(Bandit_Instance)*self.Budget - Cumulative_reward_REW
		print("{0}, {1}, {2}, {3}, {4}, {5}\n".format(args.instance,args.algorithm, args.randomSeed, args.epsilon, args.horizon, regret))

class Thompson_Sampling_with_hint:
	def __init__(self,Bandit_Instance,horizon):
		self.no_of_arms = len(Bandit_Instance)
		self.curr_means = np.zeros(self.no_of_arms,dtype=float)
		self.curr_pulls = np.zeros(self.no_of_arms,dtype=int)
		self.curr_rewards = np.zeros(self.no_of_arms,dtype=float)
		self.Budget = horizon
		self.Total_Pulls = 0
		self.Bandit_Instance = Bandit_Instance
		self.Sorted_True_Arms = np.sort(Bandit_Instance)
		self.Discrete_Prior_Belief = [[]*self.no_of_arms]*self.no_of_arms
		self.Last_rewards = np.zeros(self.no_of_arms,dtype=float)

	def Initialize_Belief(self):
		AA = []
		for l in range(0,self.no_of_arms):
			V = []
			Success = self.curr_rewards[l]
			Failures = self.curr_pulls[l] - Success
			for i in self.Sorted_True_Arms:
				V.append((i**Success)*((1-i)**Failures))

			V = V/sum(V)
			AA.append(V)

		for l in range(0,self.no_of_arms):
			Apple = []
			HH = AA[l]
			HH = HH.tolist()
			for k in range(0,self.no_of_arms):
				Apple.append([self.Sorted_True_Arms[k],HH[k]])
			self.Discrete_Prior_Belief[l] = copy.deepcopy((Apple))


	def Update_Priors(self,ARM):
		Arm_Belief = copy.deepcopy(self.Discrete_Prior_Belief[ARM])
		Last_reward = self.Last_rewards[ARM]
		E = []
		P = []
		D = 0

		if(Last_reward):
			for i in range(0,len(Arm_Belief)):
				D += (Arm_Belief[i][0])*Arm_Belief[i][1]

			for i in range(0,len(Arm_Belief)):
				Arm_Belief[i][1] = Arm_Belief[i][0]*Arm_Belief[i][1]/D
				E.append(Arm_Belief[i][0])
				P.append(Arm_Belief[i][1])
		else:
			for i in range(0,len(Arm_Belief)):
				D += (1-Arm_Belief[i][0])*Arm_Belief[i][1]

			for i in range(0,len(Arm_Belief)):
				Arm_Belief[i][1] = (1-Arm_Belief[i][0])*Arm_Belief[i][1]/D
				E.append(Arm_Belief[i][0])
				P.append(Arm_Belief[i][1])			 
		self.Discrete_Prior_Belief[ARM] = copy.deepcopy(Arm_Belief)

		return np.random.choice(a = E,size = 1,p = P)[0] ####WORKS

	def Descrete_Prior_Distribution(self):
		Dist = []
		for i in range(0,self.no_of_arms):
			Dist.append(self.Update_Priors(i))

		Dist = np.array(Dist)
		L = np.argmax(Dist)
		AA = 0
		for i in range(0,len(Dist)):
			if(Dist[L] == Dist[i]):
				if(AA <= self.curr_pulls[i]):
					AA = self.curr_pulls[i]

		return ((self.curr_pulls).tolist()).index(AA)
		# return np.random.choice(AA)

	def pull(self):
		beta_arm = self.Descrete_Prior_Distribution()
		self.Total_Pulls += 1
		self.curr_pulls[beta_arm] += 1
		Pull_reward = np.random.binomial(1,Bandit_Instance[beta_arm])
		self.curr_rewards[beta_arm] += Pull_reward
		self.Last_rewards[beta_arm] = Pull_reward
		self.curr_means[beta_arm] = self.curr_rewards[beta_arm]/self.curr_pulls[beta_arm]

	def beta_dist(self):
		Betas = []
		for i in range(0,self.no_of_arms):
			S = self.curr_rewards[i]
			F = self.curr_pulls[i] - self.curr_rewards[i]
			Betas.append(np.random.beta(S+1,F+1))
		return np.argmax(Betas)

	def pull_beta_Start(self):
		beta_arm = self.beta_dist()
		self.Total_Pulls += 1
		self.curr_pulls[beta_arm] += 1
		Pull_reward = np.random.binomial(1,Bandit_Instance[beta_arm])
		self.curr_rewards[beta_arm] += Pull_reward
		self.Last_rewards[beta_arm] = Pull_reward
		self.curr_means[beta_arm] = self.curr_rewards[beta_arm]/self.curr_pulls[beta_arm]


	def start(self):
		for i in range(0,self.no_of_arms):
			self.Total_Pulls += 1
			self.curr_pulls[i] += 1
			Reward = np.random.binomial(1,Bandit_Instance[i]) # Binomial with n = 1 => Bernouli
			self.curr_rewards[i] += Reward
			self.curr_means[i] = self.curr_rewards[i]/self.curr_pulls[i]
			self.Last_rewards[i] = Reward

	def Run_Thompson_Sampling(self):
		if(self.Budget<self.no_of_arms):
			for i in range(0,self.Budget):
				self.Total_Pulls += 1
				self.curr_pulls[i] += 1
				Reward = np.random.binomial(1,Bandit_Instance[i]) # Binomial with n = 1 => Bernouli
				self.curr_rewards[i] += Reward
				self.curr_means[i] = self.curr_rewards[i]/self.curr_pulls[i]
				self.Last_rewards[i] = Reward
		elif(self.Budget<20*self.no_of_arms):
			for i in range(0,self.Budget):
				self.pull_beta_Start()
		elif(self.Budget>=20*self.no_of_arms and self.no_of_arms<20):
			for i in range(0,20*self.no_of_arms):
				self.start() #!!!!!!!!!!!!!!START NEEDED HERE IN THIS CASE
			self.Initialize_Belief()
			for i in range(self.Total_Pulls,self.Budget):
				self.pull()
		else:
			# for i in range(0,20):
			# 	self.start() #!!!!!!!!!!!!!!START NEEDED HERE IN THIS CASE
			for i in range(0,500):
				self.pull_beta_Start()
			self.Initialize_Belief()
			for i in range(self.Total_Pulls,self.Budget):
				self.pull()		

	def result(self):
		Cumulative_reward_REW = sum(self.curr_rewards)
		regret = max(Bandit_Instance)*self.Budget - Cumulative_reward_REW
		print("{0}, {1}, {2}, {3}, {4}, {5}".format(args.instance,args.algorithm, args.randomSeed, args.epsilon, args.horizon, regret))



if(args.algorithm == "thompson-sampling"):
	Thompson_Sampling_run = Thompson_Sampling(Bandit_Instance,args.horizon)
	Thompson_Sampling_run.Run_Thompson_Sampling()
	Thompson_Sampling_run.result()
elif(args.algorithm == "thompson-sampling-with-hint"):
	Thompson_Sampling_run_hint = Thompson_Sampling_with_hint(Bandit_Instance,args.horizon)
	Thompson_Sampling_run_hint.Run_Thompson_Sampling()
	Thompson_Sampling_run_hint.result()
elif(args.algorithm == "kl-ucb"):
	KL_UCB_run = KL_UCB(Bandit_Instance,args.horizon)
	KL_UCB_run.Run_UCB()
	KL_UCB_run.result()
elif(args.algorithm == "epsilon-greedy"):
	Epsilon_run = Epsilon(Bandit_Instance,args.horizon,args.epsilon)
	Epsilon_run.Run_Epsilon()
	Epsilon_run.result()
elif(args.algorithm == "ucb"):
	UCB_run = UCB(Bandit_Instance,args.horizon)
	UCB_run.Run_UCB()
	UCB_run.result()