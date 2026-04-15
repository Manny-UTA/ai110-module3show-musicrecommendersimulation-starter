# Reflection — Music Recommender Simulation

## Profile Comparisons

**High-Energy Pop Fan vs. Chill Lofi Listener**
These two profiles produced almost entirely opposite results. The Pop Fan consistently received high-tempo, upbeat songs like *Levitating* and *Blinding Lights*, while the Lofi Listener gravitated toward low-energy tracks like *Lo-Fi Study Beat* and *Weightless*. This makes sense because their `target_energy` values (0.85 vs. 0.2) are at opposite ends of the scale, and energy proximity is a key part of the score. The difference confirmed that my energy scoring function was working correctly.

**Deep Intense Rock Head vs. Sad Pop Night Drive**
Both profiles favor somewhat darker moods, but they diverge sharply on energy. The Rock Head received aggressive, high-BPM tracks like *Smells Like Teen Spirit* and *Mr. Brightside*, while the Sad Pop profile received slower, more introspective songs like *Midnight Rain* and *Ocean Eyes*. Interestingly, *Circles* by Post Malone appeared in the Sad Pop list even though it's not labeled "pop" in my dataset — this was a proximity surprise where its energy and valence were close enough to push it into the results.

**Hip-Hop Hype Machine vs. High-Energy Pop Fan**
These two profiles had similar energy targets but different genres and moods. The Hype Machine got *Sicko Mode*, *HUMBLE.*, and *Formation*, while the Pop Fan got *Levitating* and *Blinding Lights*. The genre match weight was strong enough to keep them separated even when energy scores were similar — which is the expected behavior.

---

## Biggest Learning Moment
The most surprising moment was running the `energy_focused` mode and watching *Weightless* (an ambient track with energy=0.1) score unexpectedly high for the Chill Lofi profile. It had near-perfect energy proximity, but it's not lofi at all. This showed me that **no single feature should dominate** — you always need a balance of signals or you get weird results that technically score well but feel wrong.

## How AI Tools Helped
AI was helpful for brainstorming the proximity scoring formula (`weight × (1 - |gap|)`) and for thinking through the tradeoffs between `.sort()` and `sorted()`. It also suggested the idea of returning `reasons` alongside the score, which I found really valuable for transparency.

Where I had to double-check: AI initially suggested using a Euclidean distance formula across all features simultaneously. That would have made the scoring logic much harder to read and debug, and the weights would have been harder to reason about. I opted for the simpler per-feature approach instead.

## What Surprised Me
Even a simple 7-line scoring function can produce results that genuinely "feel" like recommendations. When I ran the Chill Lofi profile and *Clair de Lune* appeared near the top, it actually made sense — it's peaceful, low-energy, and highly acoustic. A simple algorithm surfaced a genuinely good match.

## What I'd Try Next
1. Pull real audio features from the Spotify API to get a much larger and more accurate dataset
2. Add a "diversity penalty" so the same artist can't dominate the entire top-5
3. Build a simple web UI where users can input their own preferences and get live recommendations
