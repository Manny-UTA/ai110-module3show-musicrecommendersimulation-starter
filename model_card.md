# Model Card: VibeFinder 1.0

## Model Name
**VibeFinder 1.0** — A content-based music recommendation simulator.

---

## Goal / Task
VibeFinder recommends songs from a curated catalog that best match a user's taste profile. Given preferences like genre, mood, energy level, and danceability, it scores every song and returns the top-k ranked suggestions with human-readable explanations for each recommendation.

---

## Data Used
- **Source**: Manually curated `data/songs.csv`
- **Size**: 25 songs
- **Features per song**:
  - Categorical: `title`, `artist`, `genre`, `mood`, `release_decade`
  - Numerical (0.0–1.0): `energy`, `valence`, `danceability`, `acousticness`
  - Other: `tempo_bpm` (integer), `popularity` (0–100)
- **Genre coverage**: pop, rock, hip-hop, lofi, classical, ambient, soul, electronic
- **Limitations**: Dataset is small (25 songs). Genre distribution skews toward pop and hip-hop.

---

## Algorithm Summary
VibeFinder uses **weighted content-based filtering**:

1. **Genre match** → adds points if song genre equals user's preferred genre
2. **Mood match** → adds points if song mood matches user's preferred mood
3. **Proximity scoring** → for numerical features (energy, valence, danceability), the score = `weight × (1 - |song_value - user_target|)`. Songs closer to the user's target earn more points.
4. **Decade bonus** → small bonus if song release decade matches user preference
5. **Ranking modes** shift the weights — `genre_first` amplifies genre match, `energy_focused` amplifies energy proximity, etc.

No machine learning is used. Scores are deterministic and fully explainable.

---

## Observed Behavior / Biases

- **Genre dominance**: When using `genre_first` mode, genre match overwhelms all other signals. A sad slow pop song will outscore a high-energy mood match from another genre.
- **Filter bubble risk**: If a user's preferred genre (e.g., pop) makes up 40%+ of the dataset, most recommendations will be pop regardless of mood or energy preferences.
- **Small dataset sensitivity**: With only 25 songs, small weight changes can drastically reorder the entire top-5.
- **Popularity ignored**: The `popularity` column is loaded but not used in scoring — a deliberate choice to avoid recommending only mainstream hits.
- **Mood vocabulary is limited**: Moods are single words (e.g., "happy", "sad"). Nuanced moods like "nostalgic" or "bittersweet" are not captured.

---

## Evaluation Process

Five distinct user profiles were tested across four ranking modes (balanced, genre_first, mood_first, energy_focused):

| Profile | Notable Finding |
|---|---|
| High-Energy Pop Fan | Levitating and Blinding Lights consistently topped results |
| Chill Lofi Listener | Only 1–2 songs matched genre exactly; system fell back on energy proximity |
| Deep Intense Rock Head | Smells Like Teen Spirit dominated; system correctly deprioritized acoustic songs |
| Hip-Hop Hype Machine | Sicko Mode and HUMBLE. scored highest; mood + energy alignment was strong |
| Sad Pop Night Drive | Midnight Rain and Ocean Eyes ranked well; Circles appeared as a surprise match |

**Experiment**: Doubling energy weight in `energy_focused` mode caused Weightless (ambient, energy=0.1) to score higher than expected for the "Sad Pop" profile because its energy proximity was perfect — showing that genre filtering must remain present.

---

## Intended Use
- Educational simulation to demonstrate content-based filtering concepts
- Exploring how weights affect recommendation outcomes
- Understanding algorithmic bias and filter bubbles

## Non-Intended Use
- Production music platform (dataset too small, no user behavior data)
- Replacing collaborative filtering systems (no user-to-user signals)
- Serving real users without substantial dataset expansion and validation

---

## Ideas for Improvement
1. **Expand the dataset** to 500+ songs with real audio features from the Spotify API
2. **Add collaborative filtering** layer using user listening history to complement content scores
3. **Diversity penalty**: penalize songs from the same artist already in the top-5 to prevent artist monopolization
4. **Mood embedding**: replace single-word moods with multi-dimensional mood vectors (valence + arousal) for richer matching
5. **User feedback loop**: allow thumbs up/down to dynamically adjust weights per session
