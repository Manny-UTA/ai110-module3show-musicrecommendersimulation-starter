# 🎵 Music Recommender Simulation

A content-based music recommendation simulator built in Python for the CodePath AI110 course.

---

## How The System Works

Real-world platforms like Spotify combine two major approaches: **collaborative filtering** (recommending what similar users liked) and **content-based filtering** (recommending songs with similar audio attributes). This project simulates the content-based approach.

VibeFinder compares each song's attributes — genre, mood, energy, valence, and danceability — against a user's taste profile. Songs that are closer to the user's preferences earn higher scores. The system returns the top-k songs with an explanation for each recommendation.

**Features used:**
- `genre` — categorical match (pop, rock, hip-hop, lofi, etc.)
- `mood` — categorical match (happy, sad, intense, peaceful, etc.)
- `energy` — numerical proximity (0.0 = calm, 1.0 = intense)
- `valence` — numerical proximity (0.0 = dark, 1.0 = joyful)
- `danceability` — numerical proximity (0.0 = low, 1.0 = high)
- `release_decade` — optional decade preference bonus

---

## Algorithm Recipe

| Signal | Balanced Weight | Notes |
|---|---|---|
| Genre match | +2.0 | Exact string match |
| Mood match | +1.5 | Exact string match |
| Energy proximity | up to +1.5 | `1.5 × (1 - \|gap\|)` |
| Valence proximity | up to +1.0 | `1.0 × (1 - \|gap\|)` |
| Danceability proximity | up to +1.0 | `1.0 × (1 - \|gap\|)` |
| Decade match | +1.0 | Optional bonus |

**Ranking modes** shift these weights:
- `genre_first` — amplifies genre match to 4.0
- `mood_first` — amplifies mood match to 4.0
- `energy_focused` — amplifies energy proximity to 4.0
- `balanced` — default weights above

**Potential bias**: genre match can dominate results if the user's genre makes up a large portion of the dataset. A song with a matching genre will always score higher than a non-matching song even if the non-matching song is a better fit on every other dimension.

---

## Project Structure

```
music-recommender/
├── data/
│   └── songs.csv          # 25 songs with 11 attributes each
├── src/
│   ├── recommender.py     # load_songs, score_song, recommend_songs
│   └── main.py            # CLI with 5 profiles and 4 ranking modes
├── model_card.md
├── reflection.md
└── README.md
```

---

## Setup & Running

```bash
# Install dependencies (optional, for formatted tables)
pip install tabulate

# Run the recommender
python -m src.main
```

You'll be prompted to choose a ranking mode (1–4) or run all profiles across all modes (5).

---

## Sample Output

```
=================================================================
 Profile : High-Energy Pop Fan
 Mode    : balanced
=================================================================
  #1  Levitating — Dua Lipa
       Score  : 7.18
       Why    : genre match (+2.0) | mood match (+1.5) | energy proximity (+1.28) | valence proximity (+0.90) | danceability proximity (+0.95)

  #2  Blinding Lights — The Weeknd
       Score  : 6.53
       Why    : genre match (+2.0) | mood match (+1.5) | energy proximity (+1.43) | ...
```

---

## User Profiles Tested

| Profile | Genre | Mood | Energy Target |
|---|---|---|---|
| High-Energy Pop Fan | pop | happy | 0.85 |
| Chill Lofi Listener | lofi | peaceful | 0.20 |
| Deep Intense Rock Head | rock | intense | 0.92 |
| Hip-Hop Hype Machine | hip-hop | intense | 0.88 |
| Sad Pop Night Drive | pop | sad | 0.40 |

Screenshots of terminal output for each profile are included below (add yours after running).

---

## AI Collaboration

- Used AI to design the proximity scoring formula and brainstorm weight strategies
- AI suggested Euclidean distance across all features; I simplified to per-feature scoring for readability
- AI helped structure the `reasons` return value for transparency
- See `reflection.md` for full details
