"""
recommender.py — Core logic for the Music Recommender Simulation.
Supports content-based filtering with weighted scoring and multiple ranking modes.
"""

import csv


def load_songs(filepath="data/songs.csv"):
    """Load songs from a CSV file and return a list of dictionaries with typed values."""
    songs = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = int(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            row["popularity"] = int(row["popularity"])
            songs.append(row)
    return songs


def score_song(user_prefs, song, mode="balanced"):
    """
    Score a single song against user preferences.

    Args:
        user_prefs (dict): User taste profile with target values.
        song (dict): A song dictionary loaded from CSV.
        mode (str): Ranking mode — 'balanced', 'genre_first', 'mood_first', or 'energy_focused'.

    Returns:
        tuple: (score: float, reasons: list of str)
    """
    score = 0.0
    reasons = []

    # --- Mode-based weights ---
    if mode == "genre_first":
        genre_w, mood_w, energy_w, valence_w, dance_w = 4.0, 0.5, 0.5, 0.5, 0.5
    elif mode == "mood_first":
        genre_w, mood_w, energy_w, valence_w, dance_w = 0.5, 4.0, 0.5, 0.5, 0.5
    elif mode == "energy_focused":
        genre_w, mood_w, energy_w, valence_w, dance_w = 0.5, 0.5, 4.0, 1.0, 1.0
    else:  # balanced
        genre_w, mood_w, energy_w, valence_w, dance_w = 2.0, 1.5, 1.5, 1.0, 1.0

    # Genre match
    if user_prefs.get("genre") and song["genre"].lower() == user_prefs["genre"].lower():
        score += genre_w
        reasons.append(f"genre match (+{genre_w})")

    # Mood match
    if user_prefs.get("mood") and song["mood"].lower() == user_prefs["mood"].lower():
        score += mood_w
        reasons.append(f"mood match (+{mood_w})")

    # Energy proximity (closer = higher score, max energy_w pts)
    if user_prefs.get("target_energy") is not None:
        energy_gap = abs(song["energy"] - user_prefs["target_energy"])
        energy_score = round(energy_w * (1 - energy_gap), 2)
        score += energy_score
        reasons.append(f"energy proximity (+{energy_score})")

    # Valence proximity (happiness level)
    if user_prefs.get("target_valence") is not None:
        valence_gap = abs(song["valence"] - user_prefs["target_valence"])
        valence_score = round(valence_w * (1 - valence_gap), 2)
        score += valence_score
        reasons.append(f"valence proximity (+{valence_score})")

    # Danceability proximity
    if user_prefs.get("target_danceability") is not None:
        dance_gap = abs(song["danceability"] - user_prefs["target_danceability"])
        dance_score = round(dance_w * (1 - dance_gap), 2)
        score += dance_score
        reasons.append(f"danceability proximity (+{dance_score})")

    # Decade preference bonus
    if user_prefs.get("preferred_decade") and song["release_decade"] == user_prefs["preferred_decade"]:
        score += 1.0
        reasons.append("decade match (+1.0)")

    return round(score, 2), reasons


def recommend_songs(user_prefs, songs, k=5, mode="balanced"):
    """
    Rank all songs by score and return the top-k recommendations.

    Args:
        user_prefs (dict): User taste profile.
        songs (list): List of song dicts loaded from CSV.
        k (int): Number of top recommendations to return.
        mode (str): Scoring mode — 'balanced', 'genre_first', 'mood_first', 'energy_focused'.

    Returns:
        list of tuples: [(song_dict, score, reasons), ...]
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, mode=mode)
        scored.append((song, score, reasons))

    # Sort descending by score, then alphabetically by title for ties
    ranked = sorted(scored, key=lambda x: (-x[1], x[0]["title"]))
    return ranked[:k]
