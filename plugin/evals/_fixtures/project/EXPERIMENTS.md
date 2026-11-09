# Experiment log (internal, not for the paper)

## Stage A - baselines
- run_A1: 6-layer transformer, no scratchpad. Train on 1-8 digit sums, test on 9-16 digits.
  in-distribution (ID) 99.2, out-of-distribution (OOD) 11.4
- run_A2: same + scratchpad. ID 99.6, OOD 38.0
  !! this is the number in drafts/results_v1.tex. Tokenizer bug: numbers > 9 were split
  into two tokens in the scratchpad (cfg_v1). See Stage B.

## Stage B - after tokenizer fix (cfg_v2)
- run_B2: rerun of run_A2 with cfg_v2. ID 99.7, OOD 63.1 (was 38.0 in draft v1!)
- run_B3: scratchpad + index hints. ID 99.8, OOD 81.7
- run_B4: run_B3 + length curriculum. OOD 80.9 -> no gain, drop it (maybe appendix?)

## Carry-chain breakdown (OOD test set)
| chain length | run_B2 | run_B3 |
|---|---|---|
| 0-2 | 88.4 | 94.0 |
| 3-5 | 61.0 | 79.5 |
| 6+  | 18.3 | 41.2 |

## Notes
- 3 seeds per config, std < 1.5 points everywhere.
- OOD test set: 10k problems, 9-16 digits, uniform over lengths.
