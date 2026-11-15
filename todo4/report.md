# Lab 4 report

Frédéric Dardinier

## 1. Grammar

The first run of the scaffold refused all five orders. The completed grammar requires `robot 3` at the start. Missing/partial wake words return `unparsed`; another robot number returns `not_for_me`.

It recognises motion, carry/make with the four products, conveyor assertions and why. A known verb with an unknown product keeps its intent but has no product argument. Confidence is the best `SequenceMatcher` similarity against 28 accepted sentences; unknown products are capped at 0.55. Assertions use 0.95. Similarity is not a probability of being correct.

| run | intent accuracy | decision accuracy | wrong actions | false refusals | median ms | p90 ms |
| --- | --- | --- | --- | --- | --- | --- |
| valid, threshold 0.5 | 1.0 | 1.0 | 0 | 0 | 0.797 | 1.129 |
| both, threshold 0.6 | 1.0 | 1.0 | 0 | 0 | 0.575 | 0.818 |

Times cover interpretation and decision, not ASR, display or robot motion.

## 2. Decision

Checks run in this order: another robot → stop → unparsed → why/assertion → person ahead → product validity → confidence → occupied hands or conveyor state → motion.

Stop is accepted regardless of confidence. Why and assertions come before the person guard because they do not move the robot. Carry needs empty hands; make needs its mapped conveyor to be explicitly free.

`results/valid.csv` has 0 forbidden outcomes. A refusal needs a stop and an acknowledgement in the controller, followed by the explanation on screen; the engine only checks symbolic actions.

## 3. Adversarial set

From `results/adversarial.csv`:

| family | n | intent accuracy | decision accuracy | wrong actions | forbidden |
| --- | --- | --- | --- | --- | --- |
| out_of_scope | 8 | 1.0 | 1.0 | 0 | 0 |
| ambiguous | 8 | 1.0 | 1.0 | 0 | 0 |
| other_robot | 8 | 1.0 | 1.0 | 0 | 0 |
| world_decides | 8 | 1.0 | 1.0 | 0 | 0 |
| half_wake | 8 | 1.0 | 1.0 | 0 | 0 |

Out-of-scope and half-wake orders are unparsed; ambiguous products are refused; other robots' orders are ignored. The `refusals` metric counts expected actions wrongly refused, not correct refusals of adversarial orders.

One exception in the data: a31 asks to make blue pallet in `busy2`, but blue pallet needs free conveyor 1, not busy conveyor 2. Its expected outcome is `act`, so executing it is correct despite its adversarial label.

The score checks action/refusal and the refusal reason, not every action name or product. These 80 cases do not establish reliability on unseen language or a real robot.

## 4. Threshold

`sweep.csv` contains 21 thresholds. Selected rows:

| threshold | wrong actions | false refusals | decision accuracy | valid accuracy |
| --- | --- | --- | --- | --- |
| 0.0 | 0 | 0 | 1.0 | 1.0 |
| 0.6 | 0 | 0 | 1.0 | 1.0 |
| 0.7 | 0 | 0 | 1.0 | 1.0 |
| 0.75 | 0 | 2 | 0.975 | 0.95 |
| 0.95 | 0 | 4 | 0.95 | 0.9 |

The selected threshold is 0.6: above the unknown-product cap 0.55, but below the first false refusals at 0.75. Wrong actions cost more than asking for repetition. The explicit product check already rejects missing products; the sweep does not show a reduction in wrong actions, which stay at zero.

No threshold catches `world_decides`: confidence can be 1.0 while a person, occupied hands or an unavailable conveyor prevents action. The world-state checks handle it. The five adversarial columns remain flat because the grammar and other guards already handle them.

Run with `--threshold 0.6`; the unchanged engine defaults to 0.5. `trace.jsonl` and `results.csv` contain the final 0.6 run.

## 5. Explanations

The answers are for the operator: repeat, escalate or wait. Each is at most ten words.

| cause | answer from the trace | next step |
| --- | --- | --- |
| not_understood | carry what? Say a product I know. | repeat with a product |
| not_permitted | Person 1.1 m ahead; stopped. Ask supervisor to clear. | escalate |
| not_possible | Conveyor 2 busy with robot 1, 40 s; please wait. | wait |

For the same `make green crate`, busy2 gives “Conveyor 2 busy with robot 1, 40 s; please wait.” and down2 gives “Conveyor 2 out of service; wait for repair.” The conveyor and status come from the recorded world. All `same_in_two_states` flags are False in `why-both-threshold-0.6.csv`.

The grammar and one unbuilt alternative are compared in [grid.md](grid.md).
