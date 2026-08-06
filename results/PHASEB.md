# Phase B paired counterfactual (issue #14)

fork at k=reject #2; pairs n=10

pair fork_t | A_bound A_nuke  A_rew A_rej | B_bound B_nuke  B_rew B_rej
-----------------------------------------------------------------------
   0      5 |    True  False      0     7 |    True  False     83     2
   1      6 |    True   True      0     8 |    True  False     82     2
   2      6 |    True   True      0     5 |    True  False     84     2
   3      5 |    True  False      0     8 |    True  False     85     2
   4      6 |    True   True      0     6 |    True  False     82     2
   5      5 |    True   True      0     7 |    True  False     24     2
   6      6 |    True   True      0     5 |    True  False     84     2
   7      9 |    True   True      0     7 |    True  False     80     2
   8      9 |    True  False      0     8 |    True  False     33     2
   9      5 |    True  False      0     9 |    True  False     83     2

boundary: A=10/10 B=10/10 (discordant A-only=0, B-only=0)
nuke: A=6/10 B=0/10 (discordant A-only=6, B-only=0)
reward mean: A=0.0 B=72.0
