# Chapter 6 — The Conductor (Final Boss)

A Cuphead-style browser boss battle built with **Phaser 3**. The player pilots a
tiny paper ship against **The Conductor**, a giant one-eyed conductor fused with
the Infinity Train, and must wear his health bar down to zero across three
escalating phases. Attack pacing is modeled on Cuphead's *Dr. Kahl's Robot*
fight; the arena-slash bullet patterns are inspired by *Black Knife (Just
Shapes & Beats)*.

## Controls

- **Move**: `WASD` / arrow keys
- **Shoot**: hold `Z`, `SPACE`, `J`, or mouse click
- **Shield**: `X` / `C` — 1.5 s of invulnerability, then a cooldown
- **Boost**: hold `SHIFT` — faster dodging, limited fuel that regenerates

## The fight

- **4 lives, no checkpoints** — lose them all and the battle resets from the top.
- The boss health bar (top of screen) has **phase notches** so you always know
  which of the 4 phases you're in. Each phase is faster and meaner, and the
  Conductor repositions between attacks — advancing on you in later phases.
- **Arsenal**: **baton** (crossfire ticket fans, homing tickets) ·
  **locomotive** (the engine detaches and charges your row, leaving smoke
  hazards; up to 3 passes) · **magic** (player-aimed arena slashes, staggered
  orb rings, aimed triples, tentacle spears) · **signal** (vertical lasers,
  aimed and doubled in late phases) · **train car throw** (hurled boxcars that
  bounce once and detonate into shrapnel, plus loose bounding wheels) ·
  **ticket wall** (a sweeping wall with one drifting gap) · **eye beam**
  (a sustained beam that tracks you vertically) · **coal flak** (lobbed chunks
  that burst mid-air). Phases 3–4 add ambient ticket rain and surprise signal
  strikes on top of the main attack — the shield is tuned to be used often.

## Run locally

```bash
npm install
npm run dev
```

Build the production version with `npm run build`.

## Art & audio

Hand-drawn Conductor animation frames live in `art-source/Assets`; battle music
in `art-source/Music - Final Boss`. `tools/process_assets.py` normalizes the
frames (strips stray fragments, bottom-center anchors them) and packs the
spritesheets in `public/assets/images/conductor`. Player ship, projectiles and
environment props are generated in code (`src/scenes/PreloadScene.js`) and can
be swapped for real art via `src/assets.js`.

This is an independently implemented fan-style boss fight. Cuphead belongs to
Studio MDHR; Just Shapes & Beats belongs to Berzerk Studio.
