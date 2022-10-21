import random

def random_seed():
    return run_seed.pop(random.randrange(0,len(run_seed)))

def random_in_tier(seed,tier):
    return eval(f'{seed}_tier_{tier}.pop(random.randrange(0,len({seed}_tier_{tier})))')

run_seed=['scareboss']

#tier 1 level indexes

scareboss_tier_1=[1]

#tier 2 level indexes

scareboss_tier_2=[3]

#tier 3 level indexes

scareboss_tier_3=[4]

#tier 4 level indexes

scareboss_tier_4=[1]