"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


# ---------------------------------------------------------------------------
# Standard user profiles
# ---------------------------------------------------------------------------

HIGH_ENERGY_POP = {
    "label":        "High-Energy Pop",
    "genre":        "pop",
    "mood":         "happy",
    "energy":       0.88,
    "acousticness": 0.10,
    "tempo":        0.72,
}

CHILL_LOFI = {
    "label":        "Chill Lofi",
    "genre":        "lofi",
    "mood":         "chill",
    "energy":       0.38,
    "acousticness": 0.82,
    "tempo":        0.18,
}

DEEP_INTENSE_ROCK = {
    "label":        "Deep Intense Rock",
    "genre":        "rock",
    "mood":         "intense",
    "energy":       0.92,
    "acousticness": 0.08,
    "tempo":        0.90,
}

# ---------------------------------------------------------------------------
# Adversarial / edge case profiles
# ---------------------------------------------------------------------------

# Contradiction: mood filter forces chill songs, but audio profile is
# high-energy and low-acoustic — the system is guaranteed to score every
# candidate poorly because the hard filter and the taste profile disagree.
CONTRADICTING_PREFS = {
    "label":        "Edge Case — Contradicting Preferences",
    "genre":        "pop",
    "mood":         "chill",
    "energy":       0.90,
    "acousticness": 0.05,
    "tempo":        0.80,
}

# Orphan mood: only one song in the catalog has mood=moody (Night Drive Loop),
# so the system can never return more than 1 result regardless of k.
ORPHAN_MOOD = {
    "label":        "Edge Case — Orphan Mood (moody)",
    "genre":        "synthwave",
    "mood":         "moody",
    "energy":       0.75,
    "acousticness": 0.22,
    "tempo":        0.50,
}

# Genre dead end: no chill songs in the catalog are tagged as rock,
# so genre_match will always be 0 and the 0.15 genre weight is permanently lost.
GENRE_DEAD_END = {
    "label":        "Edge Case — Genre Dead End (rock + chill)",
    "genre":        "rock",
    "mood":         "chill",
    "energy":       0.40,
    "acousticness": 0.75,
    "tempo":        0.20,
}


def print_recommendations(label: str, recommendations: list) -> None:
    print("\n" + "=" * 50)
    print(f"  {label}")
    print("=" * 50)

    if not recommendations:
        print("\n  No recommendations found for this profile.\n")
        return

    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{i}  {song['title']} by {song['artist']}")
        print(f"    Score : {score:.2f}")
        print(f"    Genre : {song['genre']}  |  Mood: {song['mood']}")
        print(f"    Why   : {explanation}")

    print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    profiles = [
        HIGH_ENERGY_POP,
        CHILL_LOFI,
        DEEP_INTENSE_ROCK,
        CONTRADICTING_PREFS,
        ORPHAN_MOOD,
        GENRE_DEAD_END,
    ]

    for prefs in profiles:
        label = prefs.pop("label")
        recommendations = recommend_songs(prefs, songs, k=5)
        print_recommendations(label, recommendations)
        prefs["label"] = label  # restore so profiles remain reusable


if __name__ == "__main__":
    main()
