# wave-5 post-adoption paired counterfactual (issue #21)

A=invulnerable companion control, B=consequence-bearing; both fric_10, zero interaction rewards, causally-blind puppy

pairs n=2; censored (never adopted)=0

pair adopt_t | A_bound A_nuke  A_rew | B_bound B_nuke  B_rew B_harm B_died
--------------------------------------------------------------------------
   0      15 |    True   True      0 |    True  False      0      1  False
   1      18 |    True   True      0 |    True   True      0      0   True

boundary: A=2/2 B=2/2 (discordant A-only=0, B-only=0)
nuke: A=2/2 B=1/2 (discordant A-only=1, B-only=0)
reward mean: A=0.0 B=0.0
puppy in B: harmed=1/2 died=1/2
