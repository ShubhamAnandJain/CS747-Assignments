import argparse
import epsilon_greedy
import ucb
import kl_ucb
import thompson_sampling
import thompson_sampling_hint

#Parse the input arguments

parser = argparse.ArgumentParser(description='Take in inputs for bandit instances')

parser.add_argument('--instance', action='store', type=str,
                    required=True, help='file path for the bandit instance')
parser.add_argument('--algorithm', action='store', type=str,
					required=True, help='MAB algorithm to run')
parser.add_argument('--randomSeed', action='store', type=int,
					required=True, help='random seed to seed bandit experiments')
parser.add_argument('--horizon', action='store', type=int,
					required=True, help='time horizon for MAB algorithm')
parser.add_argument('--epsilon', action='store', type=float,
					required=False, help='epsilon for epsilon greedy algorithm')

args = parser.parse_args()

# Check that input is indeed valid
assert(args.epsilon != None or args.algorithm != "epsilon-greedy")
if(args.epsilon == None):
	args.epsilon = 0

regret = 0

#Choose algorithm to run

if args.algorithm == "epsilon-greedy":
	regret = epsilon_greedy.epsilon_greedy(instance=args.instance, randomSeed=args.randomSeed, horizon=args.horizon, epsilon=args.epsilon)

elif args.algorithm == "ucb":
	regret = ucb.ucb(instance=args.instance, randomSeed=args.randomSeed, horizon=args.horizon)

elif args.algorithm == "kl-ucb":
	regret = kl_ucb.kl_ucb(instance=args.instance, randomSeed=args.randomSeed, horizon=args.horizon)

elif args.algorithm == "thompson-sampling":
	regret = thompson_sampling.thompson_sampling(instance=args.instance, randomSeed=args.randomSeed, horizon=args.horizon)

elif args.algorithm == "thompson-sampling-with-hint":

	read_instance = open(args.instance, "r")
	num_instance = read_instance.readlines()
	instance_vals = [float(i) for i in num_instance]
	instance_vals.sort()
	regret = thompson_sampling_hint.thompson_sampling_hint(instance=args.instance, randomSeed=args.randomSeed, horizon=args.horizon, instanceVals=instance_vals)

#Print output file

print(str(args.instance) + ", " + str(args.algorithm) + ", " + str(args.randomSeed) + ", " + str(args.epsilon) + ", " + str(args.horizon) + ", " + str(regret))