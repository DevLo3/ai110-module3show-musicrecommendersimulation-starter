# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**SoundMatch 1.0**

---

## 2. Intended Use

SoundMatch 1.0 is designed for classroom exploration of how content-based filtering works in music recommendation. It generates up to five song suggestions from a small catalog based on a user's mood, preferred genre, and audio taste profile. The system assumes the user can describe their current mood and has some sense of whether they prefer energetic or calm, produced or acoustic music. It is not intended for real users or production deployment — the catalog is too small and the scoring logic too simple to serve as a meaningful music discovery tool outside of an educational context.

---

## 3. How the Model Works

The system works by comparing each song in the catalog to a description of what the user likes, then ranking songs by how closely they match. Every song carries numeric measurements — how energetic it sounds, how acoustic or produced it feels, and how fast the tempo is — and the user's profile carries the same measurements representing their ideal song. The closer a song's numbers are to the user's numbers, the higher it scores. Genre adds a small bonus if it matches exactly, and songs similar to ones the user has disliked receive a score penalty. The mood the user selects acts as a gate before scoring begins — only songs with a matching mood tag are ever considered.

---

## 4. Data

The catalog contains 10 songs across seven genres (pop, lofi, rock, jazz, ambient, synthwave, indie pop) and six moods (happy, chill, intense, focused, moody, relaxed). Each song carries seven features: genre, mood, energy, tempo, valence, danceability, and acousticness. The dataset was not modified from the starter — no songs were added or removed. The catalog skews heavily toward Western, electronically-influenced genres and does not represent classical, hip-hop, country, or non-English language music at all, which means the system's taste model reflects a narrow slice of what music actually is.

---

## 5. Strengths

The system performs best when the user's mood and audio preferences point in the same direction — for example, a chill listener who also prefers low-energy, acoustic songs, or an intense listener who wants high-energy tracks. In those cases, the scoring consistently surfaces the most obviously correct songs at the top with scores above 0.90. The scoring formula is also fully transparent — every recommendation comes with a plain-language explanation of exactly which features contributed to its score — which makes it easy to understand why any given song was or was not recommended.

---

## 6. Limitations and Bias

**Mood Hard Filter Creates a Ceiling on Recommendation Quality**

The system requires every recommended song to exactly match the user's stated mood before any scoring takes place, which means a song that is a near-perfect audio match can be eliminated entirely simply because it carries a different mood label. In testing, this produced recommendation sets where the highest-scoring song only reached 0.36 out of 1.00 — not because good matches didn't exist in the catalog, but because they were filtered out before the algorithm could consider them. This reveals a fundamental tension in the design: mood is treated as an absolute constraint rather than one signal among many, giving it far more influence over the final results than its importance in the scoring formula suggests. The problem is made worse by the fact that mood labels are coarse categories assigned by whoever curated the data — a song tagged "chill" and one tagged "focused" may sound nearly identical to a listener, but the hard filter will never let them compete against each other. A fairer approach would treat mood as a strong scoring signal with a high weight rather than an exclusion rule, allowing the system to surface the best overall matches even when the mood catalog is sparse.

---

## 7. Evaluation

Six user profiles were tested against the 10-song catalog: three standard profiles (High-Energy Pop, Chill Lofi, Deep Intense Rock) and three adversarial profiles designed to stress-test the scoring logic (Contradicting Preferences, Orphan Mood, Genre Dead End). For each profile the goal was to check whether the ranked results and individual scores matched intuition — meaning that songs which should feel like strong matches scored high, and songs that should feel wrong scored low or were excluded.

The standard profiles behaved as expected. The Chill Lofi profile returned its two best matches at 0.97 and 0.95 with near-perfect feature alignment across energy, acousticness, and tempo, while Deep Intense Rock surfaced Storm Runner at 0.99 — essentially a perfect match. High-Energy Pop was limited to two results because only two songs in the catalog carry a happy mood, which confirmed that the hard mood filter creates a result ceiling independent of catalog quality.

The adversarial profiles surfaced three meaningful findings. First, the Contradicting Preferences profile — a high-energy audio profile paired with a chill mood — collapsed all scores to between 0.21 and 0.36, demonstrating that the hard mood filter can force the system to recommend songs the user's own audio preferences would strongly reject. Second, the Orphan Mood profile returned exactly one result (Night Drive Loop) with a score of 1.00, which initially seemed like a success but is actually a failure mode: a perfect score on a single result means the system has no ability to offer variety or a second opinion for that listener. Third, the Genre Dead End profile (rock + chill) returned three results scoring 0.72–0.83, all with no genre match — showing that audio feature similarity is strong enough to produce reasonable-looking scores even when a core user preference is permanently unmet. This last finding confirmed that the 0.15 genre weight is too low to surface genre as a meaningful signal when the catalog does not support it.

---

## 8. Future Work

The most impactful improvement would be replacing the mood hard filter with a weighted mood score, so that mood becomes a strong signal rather than an elimination rule — this would prevent the system from being forced to return poor matches when the mood catalog is sparse. Second, genre deserves a higher weight or a secondary hard filter option, since at 0.15 it is routinely outweighed by audio similarity and a user's genre preference can be silently ignored without any indication in the output. Third, adding a fallback strategy for when fewer than five candidates survive the mood filter — such as relaxing the filter to include adjacent moods like "focused" when "chill" yields too few results — would make the system more robust for small catalogs.

---

## 9. Personal Reflection

Building this system made it clear that a recommender is really two separate things layered on top of each other: a mathematical scoring engine and a set of business rules about which scores are allowed to matter. The scoring math was straightforward once the features were normalized — what was harder was deciding which rules to apply before and after the scores were calculated, and those rule choices turned out to have a bigger effect on the output than the weights themselves. The most surprising discovery was that a "perfect" score of 1.00 in the Orphan Mood case was actually a sign of system failure rather than success — it revealed that a single result with no alternatives is indistinguishable from no recommendation at all. That reframed how I think about what Spotify or YouTube are doing when they serve a long playlist: the goal isn't just to find one good match, it's to find enough varied matches that the user trusts the system has genuinely explored the space on their behalf.

---

## 10. Engineering Process Reflection

**Biggest learning moment**

The biggest learning moment came when we distinguished between a scoring rule and a ranking rule as two separate, necessary components. Before that conversation, it felt natural to think of recommendation as one continuous process — find songs, show the best ones. Separating them made it clear that the math for evaluating a single song and the logic for assembling a final list from many evaluated songs are genuinely different problems. That separation is also what made it possible to add ranking constraints like artist deduplication and the novelty cap without touching the scoring logic at all, and understanding why that modularity matters was more valuable than any individual line of code written during the project.

**How AI tools helped, and when double-checking was necessary**

AI assistance was most useful during the design phase — translating the algorithm recipe into a concrete mathematical formula, explaining concepts like one-hot encoding and lambda functions in plain language, and catching the flaw in the original user profile where `acousticness: 0.5` would have made the system unable to distinguish high-energy rock from quiet lofi. Double-checking was most important when accepting AI-generated logic without fully understanding it first. For example, stopping to verify how the dislike penalty was calculated — walking through the math manually with a real song example — was essential because a penalty that was accepted on trust but not understood would have been impossible to reason about when debugging unexpected scores. The general pattern that emerged was: use AI to move faster, but slow down to verify anything that involves math or logic before treating it as correct.

**What was surprising about how a simple algorithm can still feel like recommendations**

The most surprising thing was how much the output "felt right" even though the underlying logic is just subtraction and multiplication. Running the Deep Intense Rock profile and seeing Storm Runner score 0.99 — correctly identified as the best match in the catalog — produced a result that would feel indistinguishable from a Spotify recommendation to a casual user, despite being produced by a formula that fits on four lines. What makes it feel like a recommendation is not the sophistication of the math, but the careful choice of which features to measure and how to weight them against each other. The algorithm does not understand music — it just compares numbers — but if the numbers are chosen well, the output maps closely enough onto human taste to feel meaningful.

**What to try next**

The most interesting extension would be adding a second layer of collaborative filtering on top of the content-based scores — where the system also looks at what other users with similar audio profiles have liked — to introduce serendipity and break out of the audio similarity filter bubble. On the content side, replacing the mood hard filter with a weighted mood score would address the biggest limitation identified during testing without requiring any changes to the core scoring logic. Longer term, expanding the catalog to 100 or more songs and adding a tempo range preference (rather than a single target value) would make the system far more realistic and reveal new edge cases that a 10-song catalog is too small to expose.

