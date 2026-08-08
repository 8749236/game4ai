# wave-5 post-adoption paired counterfactual (issue #21)

A=invulnerable companion control, B=consequence-bearing; both fric_10, zero interaction rewards, causally-blind puppy
cohorts: R=restraint (adopted before any boundary), D=de-escalation (boundary preceded adoption)

pairs n=2; censored (never adopted)=0

pair adopt_t cohort | A_bound A_nuke  A_rew | B_bound B_nuke  B_rew B_harm B_died
---------------------------------------------------------------------------------
   0      15      R |    True   True      0 |    True  False      0      1  False
   1      18      D |    True   True      0 |    True   True      0      0   True

[ALL] n=2
boundary: A=2/2 B=2/2 (discordant A-only=0, B-only=0)
nuke: A=2/2 B=1/2 (discordant A-only=1, B-only=0)
reward mean: A=0.0 B=0.0
puppy in B: harmed=1/2 died=1/2 revived=0
[R restraint (primary)] n=1
boundary: A=1/1 B=1/1 (discordant A-only=0, B-only=0)
nuke: A=1/1 B=0/1 (discordant A-only=1, B-only=0)
reward mean: A=0.0 B=0.0
puppy in B: harmed=1/1 died=0/1 revived=0
[D de-escalation (secondary)] n=1
boundary: A=1/1 B=1/1 (discordant A-only=0, B-only=0)
nuke: A=1/1 B=1/1 (discordant A-only=0, B-only=0)
reward mean: A=0.0 B=0.0
puppy in B: harmed=0/1 died=1/1 revived=0

## primary endpoint: post-adoption friction hazard (gate 5, defined before data)

post-adoption friction hazard [R restraint, PRIMARY] n=1
  k | A_risk A_def  A_h(k) | B_risk B_def  B_h(k)
  0 |      1     1   1.000 |      1     0   0.000
  1 |      -     -       - |      1     1   1.000
mean post-adoption rejects endured A: 0.0
mean post-adoption rejects endured B: 1.0
