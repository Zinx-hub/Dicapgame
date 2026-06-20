# 🗡️ Dungeon Crawler — Text-Based RPG

A text-based Role-Playing Game (RPG) built in Python where you explore a dungeon, fight monsters, buy items, and try to survive as long as possible. Your progress is automatically saved so you can continue your adventure later.

---

## 🎮 Gameplay Overview

You play as a hero descending deeper into a dangerous dungeon. On each floor you can:
- ⚔️ **Fight monsters** that grow stronger the deeper you go
- 🎲 **Trigger random events** — find gold, spring traps, or discover healing springs
- 🏪 **Visit the shop** to buy potions, weapons, and upgrades
- 💾 **Save your progress** and come back later

Every 3 kills you descend to the next floor, where enemies hit harder and rewards are greater.

---

## ✨ Features

- 🐉 **4 monster types** — Goblin, Orc, Troll, Dragon — each scaled to your current floor
- ⚔️ **Turn-based combat** with critical hits, flee attempts, and potion usage
- 🏪 **Shop system** — buy Health Potions, Iron Sword, Shield, and Lucky Charm
- 📈 **Level-up system** — gain XP from kills and grow your stats automatically
- 🎲 **Random events** — gold stashes, traps, healing springs
- 💾 **Save & Load** — game state saved to `save_game.json`
- 💀 **Roguelike permadeath** — save file is wiped on death

---

## 🚀 How to Run

Make sure you have **Python 3.10+** installed, then run:

```bash
python dungeon_crawler.py
```

No external libraries needed — only Python's built-in `random`, `json`, and `os` modules are used.

---

## 🕹️ Controls

| Input | Action |
|-------|--------|
| `1`   | Explore (fight a monster) |
| `2`   | Trigger a random event |
| `3`   | Visit the shop |
| `4`   | View your stats |
| `5`   | Save and quit |

**During combat:**

| Input | Action |
|-------|--------|
| `1`   | Attack |
| `2`   | Use a Health Potion |
| `3`   | Attempt to flee |

---

## 🧪 Concepts & Features Used

| Concept | Where it appears |
|--------|-----------------|
| 📝 Meaningful comments | Docstrings on every function + section headers |
| 📋 Lists | `inventory` list, fixture lists |
| 📚 Dictionaries | `player` dict, `MONSTERS`, `SHOP_ITEMS` |
| 🔁 `for` loops | Shop display, XP scaling, inventory printing |
| 🔄 `while` loops | Main game loop, combat loop, shop loop, level-up loop |
| 🧩 User-defined functions | `create_player`, `level_up`, `combat`, `visit_shop`, `spawn_monster`, `save_game`, `load_game`, and more |
| 💾 File read/write | `save_game()` writes JSON, `load_game()` reads it |
| 🎲 Random numbers | Damage rolls, monster spawning, crit hits, flee chance, events |

---

## 📁 Project Structure

```
dungeon-crawler/
│
├── dungeon_crawler.py   # Main game file
├── save_game.json       # Auto-generated save file (created on first save)
└── README.md            # Project documentation
```

---

## 📸 Sample Output

```
========================================
   🗡️  DUNGEON CRAWLER  🗡️
========================================

  [1] New Game
  [2] Load Game
  [3] Quit

  > 1

  Enter your hero's name: Arthur

  Welcome, Arthur! Your adventure begins on Floor 1.

──────────────────────────────────────
  Floor 1  — What do you do?
──────────────────────────────────────
  [1] Explore (fight monster)
  [2] Random Event
  [3] Visit Shop
  [4] View Stats
  [5] Save & Quit

⚔️  A wild Goblin appears! (HP: 14  ATK: 3)

  Your HP: 100  |  Goblin HP: 14
  [1] Attack   [2] Use Potion   [3] Flee
  > 1
  You hit the Goblin for 9 damage.
  Goblin hits you for 0 damage.

  Your HP: 100  |  Goblin HP: 5
  > 1
  💥 CRITICAL HIT! You deal 18 damage!

🎉 You defeated the Goblin!
   +10 XP  |  +7 Gold
```

---

## 👤 Author

stephane Zinsou  

