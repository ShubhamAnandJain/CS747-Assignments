import argparse
import numpy as np


def print_transition(s1, ac, s2, r, p, end_val):

	if(s2 == end_val):
		print("transition "+str(int(s1))+" "+str(int(ac))+" "+str(int(s2))+" "+str(100000)+" "+str(p))
	else:
		print("transition "+str(int(s1))+" "+str(int(ac))+" "+str(int(s2))+" "+str(r)+" "+str(p))
	

parser = argparse.ArgumentParser(description='Take in MDP Input')

parser.add_argument('--grid', action='store', type=str,
                    required=True, help='file path for the mdp')
args = parser.parse_args()

file = open(args.grid, "r")
lines = file.readlines()

n = 0
a = 4
gamma = 1
num_rows = 0
num_cols = 0

for iter_lines in lines:
	num_rows += 1
	line_split = iter_lines.split(" ")
	for val in line_split:
		num_cols += 1
		if(int(val)!=1):
			n += 1

num_cols /= num_rows
num_cols = int(num_cols)

print("numStates "+str(n))
print("numActions "+str(a))
print("start -1")

pos_to_state = np.zeros((num_rows,num_cols))

count = 0
row = 0
val_mat = np.zeros((num_rows,num_cols))
end_val = 0

for iter_lines in lines:
	line_split = iter_lines.split(" ")
	col = 0
	for val in line_split:
		val_mat[row][col] = int(val)
		if(int(val)!=1):
			pos_to_state[row][col] = count
			count += 1
		if(int(val)==3):
			end_val = pos_to_state[row][col]
		col += 1
	row += 1

print("end "+str(int(end_val)))

for i in range(num_rows):
	for j in range(num_cols):

		if(val_mat[i][j] == 1):
			continue

		s1 = pos_to_state[i][j]
		s2 = 0
		r = -1
		p = 1.0

		if(val_mat[i][j] == 3):
			for action in range(4):
				print_transition(s1, 0, s1, 0, 1, -10)
			continue

		number_adj = 0
		adj_state = []

		if(i>0 and val_mat[i-1][j] != 1):
			s2 = pos_to_state[i-1][j]
			adj_state.append(s2)
			number_adj += 1
		else:
			adj_state.append(s1)

		if(j>0 and val_mat[i][j-1] != 1):
			s2 = pos_to_state[i][j-1]
			adj_state.append(s2)
			number_adj += 1
		else:
			adj_state.append(s1)

		if(i+1<num_rows and val_mat[i+1][j] != 1):
			s2 = pos_to_state[i+1][j]
			adj_state.append(s2)
			number_adj += 1
		else:
			adj_state.append(s1)

		if(j+1<num_cols and val_mat[i][j+1] != 1):
			s2 = pos_to_state[i][j+1]
			adj_state.append(s2)
			number_adj += 1
		else:
			adj_state.append(s1)

		ac = 0

		for end_state in adj_state:

			curr_set = {s1}
			for oth_state in adj_state:
				if(oth_state == end_state):
					continue
				curr_set.add(oth_state)
			sz_set = len(curr_set)
			trans_prob = 0.4 / sz_set;
			print_transition(s1, ac, end_state, -1.0, 0.6, end_val)
			for oth_state in curr_set:
				print_transition(s1, ac, oth_state, -1.0, trans_prob, end_val)

			ac += 1





# for i in range(num_rows):
# 	for j in range(num_cols):
# 		if(val_mat[i][j] != 1):
# 			print(i,j)
# 			print(pos_to_state[i][j])

print("mdptype continuing")
print("discount  1")