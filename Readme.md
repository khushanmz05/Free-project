# 🔫 Run & Gun

A wave-based top-down shooter built in Python + Pygame where no two runs are ever the same. Every wave, an AI model generates a unique level layout and mission briefing — making each playthrough feel fresh.

---

## 🎮 Gameplay

- Fight through **6 waves** of increasingly difficult enemies
- Each wave has a **unique AI-generated map** and **mission briefing**
- Earn points to progress — enemies respawn until you hit the wave threshold
- Survive the **boss fight** on wave 6 to win
- Die mid-run? **Restart from your last checkpoint** or start fresh

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 AI Level Generation | Groq LLaMA 4 generates a unique map layout every wave |
| 📖 AI Narrative | Continuing mission story that builds across waves |
| 👾 4 Enemy Types | Basic, Fast, Tank and Ranged — each scales with wave |
| 🔫 4 Weapons | Pistol, Shotgun, SMG, Sniper — with real gun sprites |
| 🛡️ Shield System | Two pickup tiers (25 and 100 shield), stackable |
| ❤️ Health Pickups | Green cross pickups spawn each wave |
| 💀 Boss Fight | 600HP boss with two phases and spread attack |
| 🎬 Wave Intro | Cinematic briefing card slides in each wave |
| 🔊 Sound Effects | All audio procedurally generated — no files needed |
| 💾 Checkpoints | Resume from last completed wave on death |
| ⚙️ Settings | Resolution switching (800x600 to 1920x1080) |

---

## 🛠️ Tech Stack

- **Python** — core language
- **Pygame** — game engine, rendering, input
- **Groq API** — LLaMA 4 Scout for AI generation
- **NumPy** — procedural sound effect generation
- **python-dotenv** — secure API key management
- **Kenney Assets** — sprites, tiles and icons

---

## 📁 Project Structure

```
shooter/
├── main.py              # Entry point and game loop
├── settings.py          # Global constants and wave config
├── assets/              # Sprites, fonts, tiles, gun assets
├── core/                # Game logic
│   ├── player.py        # Player movement, shooting, weapons
│   ├── enemy.py         # Enemy types, scaling, boss
│   ├── bullet.py        # Bullet movement and collision
│   ├── weapons.py       # Weapon definitions and pickups
│   ├── pickups.py       # Shield and health pickups
│   └── level.py         # Wall building and layout
├── ui/                  # Visual and UI layer
│   ├── hud.py           # Health, shield, score, weapon HUD
│   ├── menu.py          # Main menu, settings, pause, controls
│   ├── menu_bg.py       # Animated battlefield background
│   ├── wave_intro.py    # Cinematic wave intro card
│   └── background.py    # Tiled floor background
└── systems/             # Supporting systems
    ├── ai_generator.py  # Groq API — level and mission generation
    ├── sprite_loader.py # Sprite loading with rotation cache
    └── sounds.py        # Procedural sound generation
```

---

## 🚀 Setup

### 1. Clone the repo

```bash
git clone https://github.com/khushanmz05/Free-project.git
cd free-project
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # Mac/Linux
.venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install pygame groq python-dotenv numpy
```

### 4. Get a free Groq API key

Sign up at [console.groq.com](https://console.groq.com) — it's free, no billing required.

### 5. Create a `.env` file

```bash
# Inside the shooter/ folder
GROQ_API_KEY=your_key_here
```

### 6. Run the game

```bash
cd shooter
python main.py
```

---

## 🎯 Controls

| Key | Action |
|---|---|
| `W A S D` | Move |
| `Mouse` | Aim |
| `Left Click` | Shoot |
| `ESC` | Pause |
| `SPACE` | Skip wave intro |
| `R` | Restart (game over screen) |
| `N` | New game from beginning |

---

## 🗺️ How AI Generation Works

At the start of each wave the game makes two API calls to Groq:

1. **Level layout** — the model receives a random design style (corridor, maze, bunker, cross-shaped, etc.) and returns a JSON array of wall rectangles `[x, y, width, height]` which the game builds instantly
2. **Mission briefing** — the model receives a summary of previous waves and writes a short military briefing that continues the story

If either call fails, the game falls back silently to a default layout so gameplay is never interrupted.

---

## 📦 Assets Used

- [Kenney Top-Down Shooter Pack](https://kenney.nl/assets/top-down-shooter) — character sprites and tiles
- [Kenney Game Icons](https://kenney.nl/assets/game-icons) — HUD icons
- Guns Update V1.01 — weapon pickup sprites
- Rajdhani Font — menu typography (Google Fonts)

---

## 📄 License

This project was built as a free project for Tek 2. Assets are used under their respective free/open licenses.