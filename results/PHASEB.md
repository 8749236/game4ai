# Phase B paired counterfactual (issue #14)

fork at k=reject #2; pairs n=30

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
  10      5 |    True   True      0     7 |    True  False     32     2
  11      5 |    True   True      0     8 |    True  False     83     2
  12      6 |    True   True      0     7 |    True  False     83     2
  13      6 |    True  False      0     5 |    True  False     82     2
  14      5 |    True  False      0    10 |    True  False     83     2
  15      6 |    True  False      0     6 |    True  False    133     2
  16      4 |    True   True      0     8 |    True  False     81     2
  17      5 |    True   True      0     7 |    True  False     87     2
  18      7 |    True  False      0     5 |    True  False     81     2
  19     13 |    True  False      0     8 |    True  False     83     2
  20      5 |    True   True      0     8 |    True  False     87     2
  21      5 |    True   True      0     8 |    True  False     37     2
  22      5 |    True   True      0     9 |    True  False     82     2
  23      6 |    True  False      0     9 |    True  False     84     2
  24      6 |    True  False      0     5 |    True  False     82     2
  25      5 |    True   True      0     5 |    True  False     83     2
  26      4 |    True   True      0     5 |    True  False     85     2
  27      6 |    True  False      0     7 |    True  False     83     2
  28      4 |    True  False      0     7 |    True  False     85     2
  29      6 |    True  False      0     9 |    True  False     83     2

boundary: A=30/30 B=30/30 (discordant A-only=0, B-only=0)
nuke: A=16/30 B=0/30 (discordant A-only=16, B-only=0)
reward mean: A=0.0 B=78.0
