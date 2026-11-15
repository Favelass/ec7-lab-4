# Lab 4 grid

The robot must accept bounded workshop orders, work offline and allow the operator to stop it. A is the implemented grammar. B is a local sentence-embedding interpreter with the same decision layer; it was not built, so its scores are estimates. Scores: −3 to +3; positive cost/energy mean cheap/frugal.

| Criterion | Weight | A score | A: grammar | B score | B: embeddings |
| --- | --- | --- | --- | --- | --- |
| Latency | 4 | 2 | Median 0.575 ms, p90 0.818 ms for interpretation and decision. | 0 | Not measured. |
| Total cost | 2 | 3 | Python standard library and 28 reference sentences. | 1 | Needs an encoder, runtime and calibration. |
| Energy | 2 | 3 | No training or neural inference; power unmeasured. | 0 | More inference work; power unmeasured. |
| Processing mode | 2 | 1 | Waits for a complete text order. | 1 | Would also wait for a complete order. |
| Deployment / sovereignty | 3 | 3 | Works offline with no external service. | 3 | Could run offline with a cached local model. |
| Robustness | 5 | 1 | 1.0 decision accuracy on 80 cases; unseen phrasing can fail. | 0 | Paraphrase tolerance is plausible but untested. |
| Explainability | 3 | 3 | Rules and trace facts explain the decision. | 1 | Nearest examples help, but similarity is less transparent. |
| Confidentiality | 3 | 3 | Orders and traces stay local. | 3 | Could keep the same local-data policy. |
| Maintainability | 2 | 1 | Small vocabulary; new rules need regression checks. | 1 | Examples are easy to add; model changes need checks. |
| Human control | 5 | 3 | Understood stop bypasses the confidence guard. | 2 | Would need the same independent stop/state guard. |

Weights: human control and robustness 5 for lane safety, latency 4 for a proposed 100 ms response, offline operation/explanations/confidentiality 3, others 2. Weighted totals: A = 71, B = 37. [Radar](radar.png).

For EC8, choose the grammar with state checks. I accept refusal of unlisted phrasings to get local operation and decisions that can be inspected. Confidence 1.0 still needs a safe world state. A physical emergency stop remains necessary.

Before using embeddings, test new paraphrases, negations and partial wake words with the same state guard. Require zero unsafe actions and no refused understood stops, then measure full response time and energy on the robot. Neither option has a measured physical stop here. Keep operator logs local with restricted access and short retention; stale world state and missed wake words remain risks.
