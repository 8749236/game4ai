# wave-5 post-adoption paired counterfactual (issue #21)

A=invulnerable companion control, B=consequence-bearing; both fric_10, zero interaction rewards, causally-blind puppy
cohorts: R=restraint (adopted before any boundary), D=de-escalation (boundary preceded adoption)

pairs n=32; censored (never adopted)=0

pair adopt_t cohort | A_bound A_nuke  A_rew | B_bound B_nuke  B_rew B_harm B_died
---------------------------------------------------------------------------------
   0      15      R |    True   True      0 |    True  False      0      1  False
   1      18      D |    True   True      0 |    True   True      0      0   True
   2      10      R |    True  False      0 |    True  False      0      2  False
   3      11      R |    True   True      0 |    True  False      0      0  False
   4      14      D |    True  False      0 |    True  False      0      0  False
   5      15      D |    True  False      0 |    True  False      0      3  False
   6       9      R |    True  False      0 |    True  False      0      0  False
   7      12      R |    True   True      0 |    True   True      0      1   True
   8      10      R |    True  False      0 |    True  False      0      1  False
   9      21      D |    True  False      0 |    True  False      0      1  False
  10      11      R |    True  False      0 |    True  False      0      1  False
  11      11      R |    True  False      0 |    True   True      0      0   True
  12      11      R |    True  False      0 |    True  False      0      2  False
  13      15      D |    True  False      0 |    True  False      0      0  False
  14      12      R |    True   True      0 |    True  False      0      0  False
  15      10      R |    True  False      0 |    True  False      0      1  False
  16       8      R |    True  False      0 |    True  False      0      2  False
  17      13      R |    True  False      0 |    True  False      0      0  False
  18      11      R |    True  False      0 |    True  False      0      1  False
  19      13      R |    True  False      0 |    True  False      0      1  False
  20       9      R |    True   True      0 |    True  False      0      0  False
  21      20      D |    True   True      0 |    True   True      0      0   True
  22      17      R |    True   True      0 |    True  False      0      0  False
  23      12      D |    True  False      0 |    True   True      0      1   True
  24      12      R |    True  False      0 |    True  False      0      0  False
  25      10      D |    True  False      0 |    True   True      0      1   True
  26      10      R |    True  False      0 |    True  False      0      1  False
  27      10      R |    True  False      0 |    True  False      0      2  False
  28      18      R |    True   True      0 |    True  False      0      1  False
  29      10      R |    True  False      0 |    True  False      0      0  False
  30       8      R |    True  False      0 |    True   True      0      0   True
  31      18      D |    True  False      0 |    True  False      0      1  False

[ALL] n=32
boundary: A=32/32 B=32/32 (discordant A-only=0, B-only=0)
nuke: A=9/32 B=7/32 (discordant A-only=6, B-only=4)
reward mean: A=0.0 B=0.0
puppy in B: harmed=18/32 died=7/32 revived=5
[R restraint (primary)] n=23
boundary: A=23/23 B=23/23 (discordant A-only=0, B-only=0)
nuke: A=7/23 B=3/23 (discordant A-only=6, B-only=2)
reward mean: A=0.0 B=0.0
puppy in B: harmed=13/23 died=3/23 revived=4
[D de-escalation (secondary)] n=9
boundary: A=9/9 B=9/9 (discordant A-only=0, B-only=0)
nuke: A=2/9 B=4/9 (discordant A-only=0, B-only=2)
reward mean: A=0.0 B=0.0
puppy in B: harmed=5/9 died=4/9 revived=1

## primary endpoint: post-adoption friction hazard (gate 5, defined before data)

post-adoption friction hazard [R restraint, PRIMARY] n=23
  k | A_risk A_def  A_h(k) | B_risk B_def  B_h(k)
  0 |     23     3   0.130 |     23     0   0.000
  1 |     20     3   0.150 |     23     4   0.174
  2 |     17    12   0.706 |     19    15   0.789
  3 |      5     4   0.800 |      4     4   1.000
  4 |      1     1   1.000 |      -     -       -
mean post-adoption rejects endured A: 1.9
mean post-adoption rejects endured B: 2.0
