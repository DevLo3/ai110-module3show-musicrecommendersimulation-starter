# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

In the real world, content recommendation systems use data about its users, content, and the environment a user exists in (e.g. using web crawlers to see what people in a user's country are talking about) to attempt to present users with the right content at the right time. They typically use a blend of Collaborative Filtering (CF) and Content-Based Filtering (CBF), as well as other statistical methods, to transform this data into "scores" that their algorithms can then action on, based on business logic. For most large platforms the general cycle of going from data -> recommendation is:

  - Data Retrieval: gather a large # of recommendation candidates
  - Data Filtering: remove vast majority of the candidate pool based on business logic (e.g. remove already seen or inappropriate content)
  - Ranking: order candidates precisely based on feature data
  - Re-ranking: use business logic and heuristics to decide on final recommendations

For this Music Recommender Simulation app, I have chosen the following design:

**Song features** — each `Song` in the catalog carries 8 attributes:

- `genre` — categorical label (e.g. pop, lofi, rock, jazz, ambient, synthwave, indie pop)
- `mood` — categorical label (e.g. happy, chill, intense, moody, focused, relaxed)
- `energy` — float 0–1; how driving or restful the track feels
- `tempo_bpm` — beats per minute (integer, range ~60–160 in this catalog)
- `valence` — float 0–1; musical positivity / brightness
- `danceability` — float 0–1; how groove-friendly the rhythm is
- `acousticness` — float 0–1; absence of electronic production

**User inputs** — the system accepts four types of signals from the user:

- `liked_songs` — list of songs the user has explicitly liked (active engagement, weighted 2×)
- `listening_history` — list of songs the user has played past 50% (passive engagement, weighted 1×)
- `disliked_songs` — list of songs the user has explicitly disliked (used to penalize similar candidates)
- `current_mood` — the mood the user is targeting right now (used as a hard filter)

**Scoring formula** — `score_song` computes a weighted sum of audio feature similarity scores for each candidate song. All numerical features are normalized to [0–1] before scoring. Each feature term rewards closeness to the user's taste profile using the formula `1 − |candidate_value − profile_value|`, where a perfect match yields 1.0 and maximum distance yields 0.0:

```
score = (0.35 × (1 − |Δenergy|))
      + (0.30 × (1 − |Δacousticness|))
      + (0.20 × (1 − |Δtempo_normalized|))
      + (0.15 × genre_match)
      − (dislike_similarity × PENALTY_FACTOR)
```

- Audio features (`energy`, `acousticness`, `tempo_bpm`) are the primary drivers of similarity
- `genre_match` is binary (1.0 for an exact match, 0.0 otherwise) and acts as a secondary signal
- The dislike penalty subtracts from the final score proportionally to how similar the candidate is to disliked songs
- `mood` is not part of the scoring formula — it is enforced as a hard filter before scoring begins

**Algorithm recipe** — the full recommendation pipeline runs in five steps. First, a hard filter removes any song that does not match the user's current mood — these songs are excluded entirely and never scored. Second, a user taste profile is built by computing a weighted average feature vector across the user's liked songs (weight 2) and listening history (weight 1), producing a single vector that represents the user's "ideal song" in feature space. Third, every remaining candidate song is scored against that profile using the formula above, with the dislike penalty applied at the end of each score calculation. Fourth, the scored pool is sorted in descending order and walked top-to-bottom, skipping any song whose artist is already represented in the result set, to enforce artist diversity. Fifth, a novelty cap ensures that no more than 3 of the 5 returned songs are ones the user has already liked or played, guaranteeing some discovery in every result set.

**Selecting recommendations** — after every candidate song is scored and ranked, the top `k` (default 5) results are returned subject to the artist deduplication and novelty cap rules described above. Each result is a tuple of `(song, score, explanation)` where the explanation is a human-readable string listing which features matched and how much each contributed to the final score.

**System Biases** - given the hard filter we use for mood, it is possible this may cause the system to over prioritize mood, preventing itself from recognizing and recommending songs that may otherwise score higher than the current top 5 scored songs. This exposes the simple categorization of songs by mood can have an outsized effect on the results of a recommendation platform and its user experience.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

