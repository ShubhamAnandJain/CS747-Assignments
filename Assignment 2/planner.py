import argparse
import value_iteration
import howard
import lp
import numpy as np

#Parse the input arguments

parser = argparse.ArgumentParser(description='Take in MDP Input')

parser.add_argument('--mdp', action='store', type=str,
                    required=True, help='file path for the mdp')
parser.add_argument('--algorithm', action='store', type=str,
					required=True, help='MDP algorithm to run')
args = parser.parse_args()

#Choose algorithm to run

if args.algorithm == "vi":
	[v, pi] = value_iteration.value_iteration(args.mdp)

elif args.algorithm == "hpi":
	[v, pi] = howard.howard_iteration(args.mdp)
	
elif args.algorithm == "lp":
	[v, pi] = lp.linear_program(args.mdp)

#Print output file

for i in range(np.size(v)):
	print(str(format(v[i], '.6f')) + " " + str(int(pi[i])))