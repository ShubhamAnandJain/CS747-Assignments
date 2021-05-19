import argparse
import numpy as np

parser = argparse.ArgumentParser(description='Take in MDP Input')

parser.add_argument('--grid', action='store', type=str,
                    required=True, help='file path for the mdp')
parser.add_argument('--value_policy', action='store', type=str,
					required=True, help='output file of the grid')
args = parser.parse_args()

file = open(args.grid, "r")
lines = file.readlines()

num_rows = 0
num_cols = 0
n = 0

for iter_lines in lines:
	num_rows += 1
	line_split = iter_lines.split(" ")
	for val in line_split:
		num_cols += 1
		if(int(val)!=1):
			n += 1
num_cols /= num_rows
num_cols = int(num_cols)

pos_to_state = np.zeros((num_rows,num_cols))
state_to_pos = np.zeros((n))
start_pos = 0
end_pos = 0

count = 0
row = 0

for iter_lines in lines:
	line_split = iter_lines.split(" ")
	col = 0
	for val in line_split:
		if(int(val)!=1):
			pos_to_state[row][col] = count
			state_to_pos[count] = row * num_cols + col
			count += 1
			if(int(val) == 2):
				start_pos = count-1
			if(int(val) == 3):
				end_pos = count-1
		col += 1
	row += 1

file = open(args.value_policy, "r")
lines = file.readlines()

v = np.zeros(n)
pi = np.zeros(n)
cnt = 0

for iter_lines in lines:
	line_split = iter_lines.split(" ")
	v[cnt] = float(line_split[0])
	pi[cnt] = int(line_split[1])
	cnt += 1

path = ""
output = ["N ", "W ", "S ", "E "]
add_x = [-1, 0, 1, 0]
add_y = [0, -1, 0, 1]

start_pos = int(start_pos)

while(start_pos != end_pos):
	
	choose = int(pi[start_pos])
	path += output[choose]
	curr_x = int(state_to_pos[start_pos] / num_cols)
	curr_y = int(state_to_pos[start_pos]) % num_cols
	curr_x += add_x[choose]
	curr_y += add_y[choose]
	curr_x = int(curr_x)
	curr_y = int(curr_y)
	start_pos = int(pos_to_state[curr_x][curr_y])

print(path[:-1])