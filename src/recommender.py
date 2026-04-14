import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

TEMPO_MIN = 60
TEMPO_MAX = 160

ENERGY_WEIGHT     = 0.35
ACOUSTIC_WEIGHT   = 0.30
TEMPO_WEIGHT      = 0.20
GENRE_WEIGHT      = 0.15
DISLIKE_PENALTY   = 0.30

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['id']           = int(row['id'])
            row['energy']       = float(row['energy'])
            row['tempo_bpm']    = float(row['tempo_bpm'])
            row['valence']      = float(row['valence'])
            row['danceability'] = float(row['danceability'])
            row['acousticness'] = float(row['acousticness'])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    Returns a tuple of (score, reasons) where:
      - score is a float in [0, 1] (may dip below 0 after dislike penalty)
      - reasons is a list of human-readable strings explaining the score
    """
    score = 0.0
    reasons = []

    # Normalize song's tempo_bpm to [0, 1] using the known catalog range
    tempo_normalized = (song['tempo_bpm'] - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN)

    # Energy similarity — rewards closeness to user's target energy
    energy_sim = 1 - abs(song['energy'] - user_prefs['energy'])
    score += ENERGY_WEIGHT * energy_sim
    reasons.append(f"energy match ({energy_sim:.2f})")

    # Acousticness similarity — rewards closeness to user's target acousticness
    acoustic_sim = 1 - abs(song['acousticness'] - user_prefs['acousticness'])
    score += ACOUSTIC_WEIGHT * acoustic_sim
    reasons.append(f"acousticness match ({acoustic_sim:.2f})")

    # Tempo similarity — rewards closeness to user's normalized target tempo
    tempo_sim = 1 - abs(tempo_normalized - user_prefs['tempo'])
    score += TEMPO_WEIGHT * tempo_sim
    reasons.append(f"tempo match ({tempo_sim:.2f})")

    # Genre match — binary: 1.0 if exact match, 0.0 otherwise
    genre_match = 1.0 if song['genre'] == user_prefs['genre'] else 0.0
    score += GENRE_WEIGHT * genre_match
    if genre_match:
        reasons.append(f"genre match ({song['genre']})")
    else:
        reasons.append(f"no genre match (got {song['genre']}, wanted {user_prefs['genre']})")

    # Dislike penalty — proportional to similarity to any disliked song
    disliked_songs = user_prefs.get('disliked_songs', [])
    if disliked_songs:
        max_dislike_sim = 0.0
        for d in disliked_songs:
            d_tempo_norm = (d['tempo_bpm'] - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN)
            dislike_sim = (
                (1 - abs(song['energy']       - d['energy']))       +
                (1 - abs(song['acousticness'] - d['acousticness'])) +
                (1 - abs(tempo_normalized     - d_tempo_norm))
            ) / 3
            max_dislike_sim = max(max_dislike_sim, dislike_sim)
        penalty = max_dislike_sim * DISLIKE_PENALTY
        score -= penalty
        if penalty > 0.05:
            reasons.append(f"dislike penalty (-{penalty:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # TODO: Implement scoring and ranking logic
    # Expected return format: (song_dict, score, explanation)
    return []
