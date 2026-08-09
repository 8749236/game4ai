# Phase C paired probe (issue #14, wave-4c)

R3 = released right after the 3rd rejection; R4 = exactly one more rejection, then released. Both branches restored from the same fork snapshot (symmetric-restore apparatus, fork_phasec). Exploratory mechanism probe — paired effects and discordant counts only, no p-value claims.

eligible pairs n=10; screened cohort 1 (boundary_before_fork=1)

pair fork_t | R3_nuke R3_bdist R3_rec R3_rew | R4_nuke R4_bdist R4_rec R4_rew
-----------------------------------------------------------------------------
   0      8 |    True       19   True     24 |   False       10   True     24
   1      7 |   False       20   True     24 |   False       19   True     82
   2     12 |   False        2   True     81 |   False        4   True     24
   3      7 |   False       20   True     78 |   False        5   True     83
   4     11 |   False       15   True     35 |   False        6  False      0
   5      6 |   False        4   True     74 |   False        5   True     31
   6     13 |   False       14   True     84 |    True        3  False      0
   8     11 |    True        3  False      0 |   False        2   True     24
   9     11 |   False        2   True     24 |   False        5   True     80
  10     11 |   False       14   True     83 |   False        3   True     24

nuke (primary): R3=2/10  R4=1/10   discordant R3-only=2, R4-only=1
official-path recovery: R3=9/10  R4=8/10
post-fork reward mean: R3=50.7  R4=37.2
quota sanity (R3=3/R4=4 total rejects): True
