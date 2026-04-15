"""
main.py — CLI entry point for the Music Recommender Simulation.
Run with: python -m src.main
"""

from recommender import load_songs, recommend_songs

try:
    from tabulate import tabulate
    USE_TABULATE = True
except ImportError:
    USE_TABULATE = False


# ─── User Profiles ────────────────────────────────────────────────────────────

PROFILES = {
    "High-Energy Pop Fan": {
        "genre": "pop",
        "mood": "happy",
        "target_energy": 0.85,
        "target_valence": 0.80,
        "target_danceability": 0.85,
    },
    "Chill Lofi Listener": {
        "genre": "lofi",
        "mood": "peaceful",
        "target_energy": 0.2,
        "target_valence": 0.55,
        "target_danceability": 0.45,
    },
    "Deep Intense Rock Head": {
        "genre": "rock",
        "mood": "intense",
        "target_energy": 0.92,
        "target_valence": 0.30,
        "target_danceability": 0.50,
    },
    "Hip-Hop Hype Machine": {
        "genre": "hip-hop",
        "mood": "intense",
        "target_energy": 0.88,
        "target_valence": 0.35,
        "target_danceability": 0.80,
    },
    "Sad Pop Night Drive": {
        "genre": "pop",
        "mood": "sad",
        "target_energy": 0.40,
        "target_valence": 0.35,
        "target_danceability": 0.55,
    },
}

MODES = ["balanced", "genre_first", "mood_first", "energy_focused"]


def print_recommendations(recommendations, profile_name, mode):
    """Print a formatted table of song recommendations."""
    print(f"\n{'='*65}")
    print(f" Profile : {profile_name}")
    print(f" Mode    : {mode}")
    print(f"{'='*65}")

    if USE_TABULATE:
        rows = []
        for rank, (song, score, reasons) in enumerate(recommendations, 1):
            rows.append([
                rank,
                song["title"],
                song["artist"],
                score,
                " | ".join(reasons) if reasons else "—"
            ])
        print(tabulate(rows, headers=["#", "Title", "Artist", "Score", "Why"], tablefmt="rounded_outline"))
    else:
        for rank, (song, score, reasons) in enumerate(recommendations, 1):
            print(f"\n  #{rank}  {song['title']} — {song['artist']}")
            print(f"       Score  : {score}")
            print(f"       Why    : {' | '.join(reasons) if reasons else '—'}")
    print()


def run_all_profiles(songs, mode="balanced"):
    """Run the recommender for all user profiles."""
    for profile_name, prefs in PROFILES.items():
        recs = recommend_songs(prefs, songs, k=5, mode=mode)
        print_recommendations(recs, profile_name, mode)


def main():
    print("\n🎵  Music Recommender Simulation")
    print("────────────────────────────────")

    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    print("Choose a mode:")
    for i, mode in enumerate(MODES, 1):
        print(f"  {i}. {mode}")
    print("  5. Run ALL profiles in ALL modes")

    choice = input("\nEnter choice (1-5): ").strip()

    if choice == "5":
        for mode in MODES:
            run_all_profiles(songs, mode=mode)
    elif choice in ("1", "2", "3", "4"):
        selected_mode = MODES[int(choice) - 1]
        run_all_profiles(songs, mode=selected_mode)
    else:
        print("Invalid choice. Running balanced mode.")
        run_all_profiles(songs, mode="balanced")


if __name__ == "__main__":
    main()
