"""
Dungeon Crawler - A Text-Based RPG
Author: [Your Name]
Description: A dungeon-crawling RPG where the player fights monsters,
             collects loot, and tries to survive as long as possible.
             Game progress is saved and loaded from a file.
"""

import random
import json
import os

# ─────────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────────
SAVE_FILE = "save_game.json"

# Monster templates: name -> (min_hp, max_hp, min_atk, max_atk, xp_reward, gold_reward)
MONSTERS = {
    "Goblin":   (10, 20,  2,  5,  10, 5),
    "Orc":      (25, 40,  5, 10,  25, 12),
    "Troll":    (40, 60,  8, 15,  50, 20),
    "Dragon":   (80, 120, 15, 25, 100, 50),
}

# Shop items: name -> (cost, effect_key, effect_value)
SHOP_ITEMS = {
    "Health Potion":  (15, "heal",        30),
    "Iron Sword":     (30, "atk_boost",    5),
    "Shield":         (25, "def_boost",    5),
    "Lucky Charm":    (40, "luck",          1),
}


# ─────────────────────────────────────────────
#  PLAYER FUNCTIONS
# ─────────────────────────────────────────────

def create_player(name: str) -> dict:
    """Create and return a new player dictionary with default stats."""
    return {
        "name":     name,
        "hp":       100,
        "max_hp":   100,
        "atk":      10,
        "defense":  3,
        "level":    1,
        "xp":       0,
        "xp_next":  30,
        "gold":     20,
        "luck":     0,          # extra luck = higher crit chance
        "inventory": [],        # list of item name strings
        "kills":    0,
        "floor":    1,
    }


def level_up(player: dict) -> None:
    """Level up the player if XP threshold is reached, boosting stats."""
    while player["xp"] >= player["xp_next"]:
        player["xp"]      -= player["xp_next"]
        player["level"]   += 1
        player["xp_next"]  = int(player["xp_next"] * 1.5)
        player["max_hp"]  += 15
        player["hp"]       = player["max_hp"]   # full heal on level up
        player["atk"]     += 3
        player["defense"] += 1
        print(f"\n✨ LEVEL UP! You are now level {player['level']}!")
        print(f"   Max HP → {player['max_hp']}  ATK → {player['atk']}  DEF → {player['defense']}")


def show_stats(player: dict) -> None:
    """Display the player's current stats."""
    print("\n" + "=" * 40)
    print(f"  {player['name']}  |  Floor {player['floor']}")
    print("=" * 40)
    print(f"  HP      : {player['hp']}/{player['max_hp']}")
    print(f"  Level   : {player['level']}  (XP: {player['xp']}/{player['xp_next']})")
    print(f"  ATK     : {player['atk']}    DEF: {player['defense']}")
    print(f"  Gold    : {player['gold']}   Kills: {player['kills']}")
    print(f"  Luck    : {player['luck']}")
    if player["inventory"]:
        print(f"  Items   : {', '.join(player['inventory'])}")
    print("=" * 40)


# ─────────────────────────────────────────────
#  MONSTER FUNCTIONS
# ─────────────────────────────────────────────

def spawn_monster(floor: int) -> dict:
    """
    Randomly spawn a monster scaled to the current floor.
    Higher floors have a greater chance of tougher monsters.
    """
    # Weight tougher monsters more heavily on higher floors
    weights = [max(1, 10 - floor), max(1, 8 - floor), floor, floor // 2]
    monster_name = random.choices(list(MONSTERS.keys()), weights=weights, k=1)[0]
    base = MONSTERS[monster_name]

    # Scale HP and ATK slightly with floor number
    scale = 1 + (floor - 1) * 0.1
    hp    = int(random.randint(base[0], base[1]) * scale)
    atk   = int(random.randint(base[2], base[3]) * scale)

    return {
        "name": monster_name,
        "hp":   hp,
        "atk":  atk,
        "xp":   base[4],
        "gold": base[5] + random.randint(0, floor * 2),
    }


# ─────────────────────────────────────────────
#  COMBAT
# ─────────────────────────────────────────────

def combat(player: dict, monster: dict) -> bool:
    """
    Run a turn-based combat loop between the player and a monster.
    Returns True if the player wins, False if the player dies.
    """
    print(f"\n⚔️  A wild {monster['name']} appears! (HP: {monster['hp']}  ATK: {monster['atk']})")

    while monster["hp"] > 0 and player["hp"] > 0:
        print(f"\n  Your HP: {player['hp']}  |  {monster['name']} HP: {monster['hp']}")
        print("  [1] Attack   [2] Use Potion   [3] Flee")
        choice = input("  > ").strip()

        if choice == "1":
            # ── Player attacks ──
            crit_chance = 10 + player["luck"] * 5   # base 10 % crit
            is_crit     = random.randint(1, 100) <= crit_chance
            dmg         = random.randint(int(player["atk"] * 0.8), player["atk"])
            if is_crit:
                dmg = int(dmg * 2)
                print(f"  💥 CRITICAL HIT! You deal {dmg} damage!")
            else:
                print(f"  You hit the {monster['name']} for {dmg} damage.")
            monster["hp"] -= dmg

        elif choice == "2":
            # ── Use health potion ──
            if "Health Potion" in player["inventory"]:
                player["inventory"].remove("Health Potion")
                heal = 30
                player["hp"] = min(player["max_hp"], player["hp"] + heal)
                print(f"  🧪 You drink a potion and recover {heal} HP. (HP: {player['hp']})")
            else:
                print("  You have no potions!")
                continue    # don't let monster attack on a failed action

        elif choice == "3":
            # ── Attempt to flee (50 % chance) ──
            if random.random() < 0.5:
                print("  🏃 You successfully flee!")
                return True     # treat flee as survival (no rewards)
            else:
                print("  You failed to flee!")

        else:
            print("  Invalid choice.")
            continue

        # ── Monster attacks (if still alive) ──
        if monster["hp"] > 0:
            m_dmg = max(0, random.randint(int(monster["atk"] * 0.7), monster["atk"]) - player["defense"])
            player["hp"] -= m_dmg
            print(f"  {monster['name']} hits you for {m_dmg} damage.")

    # ── Resolve outcome ──
    if player["hp"] <= 0:
        print(f"\n💀 You were slain by the {monster['name']}...")
        return False
    else:
        print(f"\n🎉 You defeated the {monster['name']}!")
        player["xp"]   += monster["xp"]
        player["gold"] += monster["gold"]
        player["kills"] += 1
        print(f"   +{monster['xp']} XP  |  +{monster['gold']} Gold")
        level_up(player)
        return True


# ─────────────────────────────────────────────
#  SHOP
# ─────────────────────────────────────────────

def visit_shop(player: dict) -> None:
    """Let the player spend gold on items that boost stats or restore HP."""
    print("\n🏪 Welcome to the Shop!")
    while True:
        print(f"\n  Your Gold: {player['gold']}")
        print("  Items for sale:")
        items = list(SHOP_ITEMS.items())
        for i, (item, (cost, _, _)) in enumerate(items, 1):
            print(f"    [{i}] {item}  — {cost} Gold")
        print("  [0] Leave shop")

        choice = input("  > ").strip()
        if choice == "0":
            break
        if not choice.isdigit() or not (1 <= int(choice) <= len(items)):
            print("  Invalid choice.")
            continue

        item_name, (cost, effect, value) = items[int(choice) - 1]

        if player["gold"] < cost:
            print("  Not enough gold!")
            continue

        # Apply purchase
        player["gold"] -= cost
        if effect == "heal":
            player["inventory"].append(item_name)
            print(f"  ✅ Bought {item_name} — added to inventory.")
        elif effect == "atk_boost":
            player["atk"] += value
            print(f"  ✅ ATK increased by {value}! (Now {player['atk']})")
        elif effect == "def_boost":
            player["defense"] += value
            print(f"  ✅ DEF increased by {value}! (Now {player['defense']})")
        elif effect == "luck":
            player["luck"] += value
            print(f"  ✅ Luck increased by {value}! (Now {player['luck']})")


# ─────────────────────────────────────────────
#  FILE SAVE / LOAD
# ─────────────────────────────────────────────

def save_game(player: dict) -> None:
    """Serialize player data to a JSON save file."""
    with open(SAVE_FILE, "w") as f:
        json.dump(player, f, indent=2)
    print(f"  💾 Game saved to '{SAVE_FILE}'.")


def load_game() -> dict | None:
    """Load and return player data from the JSON save file, or None if not found."""
    if not os.path.exists(SAVE_FILE):
        return None
    with open(SAVE_FILE, "r") as f:
        player = json.load(f)
    print(f"  📂 Save file loaded. Welcome back, {player['name']}!")
    return player


def delete_save() -> None:
    """Delete the save file to start fresh."""
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)


# ─────────────────────────────────────────────
#  FLOOR EVENTS
# ─────────────────────────────────────────────

def random_event(player: dict) -> None:
    """
    Trigger a random non-combat floor event:
    finding gold, a trap, or a healing spring.
    """
    events = ["gold", "trap", "spring", "nothing"]
    event  = random.choice(events)

    if event == "gold":
        amount = random.randint(5, 20) + player["floor"] * 2
        player["gold"] += amount
        print(f"\n💰 You find a hidden stash of {amount} gold!")
    elif event == "trap":
        dmg = random.randint(5, 15)
        player["hp"] = max(1, player["hp"] - dmg)  # can't die from a trap
        print(f"\n🪤 You trigger a trap and take {dmg} damage! (HP: {player['hp']})")
    elif event == "spring":
        heal = random.randint(10, 25)
        player["hp"] = min(player["max_hp"], player["hp"] + heal)
        print(f"\n💧 You find a healing spring and recover {heal} HP! (HP: {player['hp']})")
    else:
        print("\n🌫️  The corridor is quiet. Nothing happens.")


# ─────────────────────────────────────────────
#  MAIN GAME LOOP
# ─────────────────────────────────────────────

def main() -> None:
    """Entry point — handles the main menu and the primary game loop."""
    print("=" * 40)
    print("   🗡️  DUNGEON CRAWLER  🗡️")
    print("=" * 40)

    # ── Main menu ──
    print("\n  [1] New Game")
    print("  [2] Load Game")
    print("  [3] Quit")
    menu_choice = input("\n  > ").strip()

    if menu_choice == "3":
        print("Goodbye, adventurer!")
        return

    if menu_choice == "2":
        player = load_game()
        if player is None:
            print("  No save file found. Starting a new game instead.")
            menu_choice = "1"

    if menu_choice == "1":
        delete_save()   # clear any old save for a fresh run
        name = input("\n  Enter your hero's name: ").strip() or "Hero"
        player = create_player(name)
        print(f"\n  Welcome, {player['name']}! Your adventure begins on Floor 1.")

    # ── Primary game loop ──
    running = True
    while running and player["hp"] > 0:
        print(f"\n\n{'─' * 40}")
        print(f"  Floor {player['floor']}  — What do you do?")
        print("─" * 40)
        print("  [1] Explore (fight monster)")
        print("  [2] Random Event")
        print("  [3] Visit Shop")
        print("  [4] View Stats")
        print("  [5] Save & Quit")

        action = input("\n  > ").strip()

        if action == "1":
            monster = spawn_monster(player["floor"])
            survived = combat(player, monster)
            if not survived:
                running = False
            else:
                # Advance floor every 3 kills
                if player["kills"] % 3 == 0 and player["kills"] > 0:
                    player["floor"] += 1
                    print(f"\n🏆 You descend to Floor {player['floor']}! The dungeon grows darker…")

        elif action == "2":
            random_event(player)

        elif action == "3":
            visit_shop(player)

        elif action == "4":
            show_stats(player)

        elif action == "5":
            save_game(player)
            print("  Farewell, brave adventurer!")
            running = False

        else:
            print("  Please enter a valid option.")

    # ── Game over screen ──
    if player["hp"] <= 0:
        print("\n" + "=" * 40)
        print("        💀  GAME OVER  💀")
        print("=" * 40)
        print(f"  Hero  : {player['name']}")
        print(f"  Level : {player['level']}")
        print(f"  Floor : {player['floor']}")
        print(f"  Kills : {player['kills']}")
        print("=" * 40)
        delete_save()   # wipe save on death (roguelike style)


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()
