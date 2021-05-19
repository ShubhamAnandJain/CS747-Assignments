import control_instance
import numpy as np

def sarsa0(stochastic, kingmove, num_episodes, seed, epsilon, alpha):

	control_inst = control_instance.instance(randomSeed=seed, stochastic=stochastic)
	np.random.seed(seed)
	episodes = []
	timesteps = []
	curr_ep = 1
	curr_ti = 0
	num_actions = 4
	if(kingmove):
		num_actions = 8

	q_table = np.zeros(((control_instance.size[0] + 1) * (control_instance.size[1] + 1), 8))

	for iter in range(num_episodes):

		curr_state = control_inst.reset_instance()

		while(True):
			
			curr_ti += 1
			opt_ans = -1e10
			arm = -1
			
			for i in range(num_actions):
				if(q_table[curr_state][i] > opt_ans):
					opt_ans = q_table[curr_state][i]
					arm = i

			# We calculated the optimal action to take
			# Now we need to follow epsilon greedy policy
			# random_sample is 1 with epsilon probability

			random_sample = np.random.binomial(n=1, p=epsilon)

			if(random_sample):
				arm = np.random.choice(num_actions, 1)[0]

			[movex, movey] = control_instance.decode(action=arm, kingmove=kingmove)
			[rew, nxt_state] = control_inst.make_move(movex, movey)

			opt_ans = -1e10
			nxt_arm = -1

			if(rew > 0):
				#indicates we reached the end state
				#just update and break
				q_table[curr_state][arm] += alpha * (- rew - q_table[curr_state][arm])
				break

			for i in range(num_actions):
				if(q_table[nxt_state][i] > opt_ans):
					opt_ans = q_table[nxt_state][i]
					nxt_arm = i

			random_sample = np.random.binomial(n=1, p=epsilon)

			if(random_sample):
				nxt_arm = np.random.choice(num_actions, 1)[0]

			#this should be changed for policies
			q_table[curr_state][arm] += alpha * (rew + q_table[nxt_state][nxt_arm] - q_table[curr_state][arm])
			curr_state = nxt_state

		timesteps.append(curr_ti)
		episodes.append(curr_ep)
		curr_ep += 1

	return [timesteps, episodes]