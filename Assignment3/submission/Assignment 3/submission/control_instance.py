import numpy as np

start = [0, 3]
end = [7, 3]
wind = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]
size = [9, 6] 
stoc_add = [-1, 0, 1]

# board is 7 x 10 in size
# Thus, x is from 0...9 and y is from 0...6
# wind values are given wrt x
# random values will be chosen from stoc_add; i.e, stochasticity introduced

def compute_state(posx, posy):
	return posx * (size[1] + 1) + posy

class instance:

	# we maintain the following:
	# posx, posy maintain our current position
	# stochastic tells us if our instance is stochastic or not

	def __init__(self, randomSeed, stochastic):
		np.random.seed(randomSeed)
		self.stochastic = stochastic
		self.posx = start[0]
		self.posy = start[1]
		return

	def reset_instance(self):
		self.posx = start[0]
		self.posy = start[1]
		return compute_state(self.posx, self.posy)

	def make_move(self, movex, movey):

		finx = self.posx + movex
		finy = self.posy + wind[self.posx] + movey
		if(self.stochastic == 1):
			finy += np.random.choice(stoc_add, 1)[0]
		finx = min(finx, size[0])
		finx = max(finx, 0)
		finy = min(finy, size[1])
		finy = max(finy, 0)
		curr_state = compute_state(finx, finy)
		self.posx = finx
		self.posy = finy
		rew = -1
		if(finx == end[0] and finy == end[1]):
			rew = 1

		return [rew, curr_state]


mx = [-1, 0, 1, 0]
my = [0, -1, 0, 1]

mx_stoc = [-1, 1, 0]
my_stoc = [-1, 1, 0]

def decode(action, kingmove):

	# if kingmove = 0, action = 0, 1, 2, 3 correspond to L, D, R, U
	# else, action = 0-7 corresponding to [-1,1,0] * [-1,1,0]

	movex = 0
	movey = 0

	if(kingmove == 0):
		movex = mx[action]
		movey = my[action]

	else:
		movex = mx_stoc [action % 3]
		movey = my_stoc [int(action / 3)]

	return [movex, movey]
