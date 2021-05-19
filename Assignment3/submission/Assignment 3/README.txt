Please refer to the report and comments in the code to get an idea of the internal structure of the code. This README will tell you about running the wrapper program, which is get_plots.py.

For getting plots with no stochasticity and no king moves:

python3 get_plots.py --stochastic 0 --kingmove 0 --episodes 200 --iter 50 --epsilon 0.1 --alpha 0.5

For getting plots with king moves:

python3 get_plots.py --stochastic 0 --kingmove 1 --episodes 200 --iter 50 --epsilon 0.1 --alpha 0.5

For getting plots with stochasticity + king moves:

python3 get_plots.py --stochastic 1 --kingmove 1 --episodes 200 --iter 50 --epsilon 0.1 --alpha 0.5