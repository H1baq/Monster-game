from rich import print

from db import Session
from models.player import Player
from models.player_monsters import PlayerMonster

# Auth and profile
from utils.auth import login_or_create_player
from utils.view_profile import view_player_profile
from utils.view_monster_profile import view_monster_profile

# Gameplay
from utils.catching import try_catch_monster
from utils.leveling import level_up_monster
from utils.view_inventory import view_inventory
from utils.battle_engine import simulate_battle, simulate_ai_battle
from utils.battle_logger import log_battle, view_battle_history

# Shop and trading
from utils.shop import open_monster_shop
from utils.trading import (
    propose_trade,
    respond_to_trade,
    list_player_ids,
    list_player_monsters,
    list_pending_trades,
)

# Social features
from utils.relationship import (
    add_relationship,
    list_relationships,
    get_related_player_ids,
    clean_invalid_relationships,
)

# Leaderboards
from utils.leaderboard import leaderboard_by_collection, leaderboard_by_wins

from utils.ui import (
    print_title,
    print_subtitle,
    print_success,
    print_error,
    print_warning,
    ask,
    pause,
    loading
)

def main(session):
    clean_invalid_relationships(session)
    player = login_or_create_player(session)

    while True:
        session.refresh(player)

        print_title(f"🧬 MONSTER TAMER HUB — Logged in as {player.username}")
        print(f"🔹 Level: {player.level} | 🧠 XP: {round(player.experience, 1)} | 💰 Money: £{round(player.money, 2)}")
        print(f"⚔️ Battles: {player.total_battles} | ✅ Wins: {player.wins} | ❌ Losses: {player.losses} | 🏆 Win Rate: {player.win_rate}%")

        print_subtitle("📜 MAIN MENU:")
        print("[bold yellow]1.[/bold yellow] 🐾 Gameplay")
        print("[bold yellow]2.[/bold yellow] 🎒 Inventory")
        print("[bold yellow]3.[/bold yellow] ⚔️ Battles")
        print("[bold yellow]4.[/bold yellow] 🛒 Monster Shop")
        print("[bold yellow]5.[/bold yellow] 🔁 Trade Monsters")
        print("[bold yellow]6.[/bold yellow] 👥 Social")
        print("[bold yellow]7.[/bold yellow] 🧑 Profile")
        print("[bold yellow]8.[/bold yellow] 🏆 Leaderboards")
        print("[bold yellow]0.[/bold yellow] 🚪 Exit Game")

        choice = ask("Choose a menu")

        if choice == "1":
            print_subtitle("🎮 Gameplay Menu")
            print("1. Catch a Monster")
            print("2. Level Up a Monster")
            sub = ask("Choose an option")
            if sub == "1":
                loading("Catching monster...")
                try_catch_monster(session, player.id)
            elif sub == "2":
                try:
                    monster_id = int(ask("Enter monster ID to train"))
                    monster = session.query(PlayerMonster).filter_by(id=monster_id).first()
                    if monster and monster.player_id == player.id:
                        loading("Training monster...")
                        level_up_monster(monster, exp_points=120)
                        session.commit()
                        print_success("Monster trained successfully!")
                    else:
                        print_error("No monster found or it's not yours.")
                except ValueError:
                    print_warning("Invalid number.")
            else:
                print_error("Invalid option.")
            pause()

        elif choice == "2":
            print_subtitle("🎒 Inventory Menu")
            print("1. View My Monsters")
            print("2. View Monster Profile")
            sub = ask("Choose an option")
            if sub == "1":
                view_inventory(session, player)
            elif sub == "2":
                monsters = session.query(PlayerMonster).filter_by(player_id=player.id).all()
                if not monsters:
                    print_warning("You don't have any monsters.")
                else:
                    for m in monsters:
                        print(f"🆔 {m.id} | 🐉 {m.species.name} | 🌚 Lvl: {m.level} | ❤️ HP: {m.current_hp}")
                    try:
                        monster_id = int(ask("Enter Monster ID"))
                        monster = session.query(PlayerMonster).filter_by(id=monster_id, player_id=player.id).first()
                        if monster:
                            view_monster_profile(monster)
                        else:
                            print_error("Not your monster.")
                    except ValueError:
                        print_warning("Invalid input.")
            else:
                print_error("Invalid option.")
            pause()

        elif choice == "3":
            print_subtitle("⚔️ Battle Menu")
            print("1. Battle CPU Trainer")
            print("2. Battle Another Player")
            print("3. Battle History")
            sub = ask("Choose an option")
            if sub == "1":
                simulate_ai_battle(session, player)
            elif sub == "2":
                opponent = ask("Enter opponent's username")
                simulate_battle(session, player.id, opponent)
            elif sub == "3":
                view_battle_history(session, player)
            else:
                print_error("Invalid option.")
            pause()

        elif choice == "4":
            open_monster_shop(session, player)
            pause()

        elif choice == "5":
            print_subtitle("🔁 Trade Menu")
            print("1. Propose Trade")
            print("2. Respond to Trade")
            print("3. View Pending Trades")
            sub = ask("Choose an option")
            if sub == "1":
                list_player_ids(session)
                list_player_monsters(session, player.id)
                try:
                    receiver_id = int(ask("Receiver's Player ID"))
                    offered_id = int(ask("Your Monster ID"))
                    requested_id = int(ask("Their Monster ID"))
                    propose_trade(session, player.id, receiver_id, offered_id, requested_id)
                except ValueError:
                    print_warning("Invalid input.")
            elif sub == "2":
                try:
                    trade_id = int(ask("Trade ID to respond to"))
                    decision = ask("Accept trade? (yes/no)").lower()
                    respond_to_trade(session, trade_id, accept=(decision == "yes"))
                except ValueError:
                    print_warning("Invalid input.")
            elif sub == "3":
                list_pending_trades(session)
            else:
                print_error("Invalid option.")
            pause()

        elif choice == "6":
            print_subtitle("👥 Social Menu")
            print("1. Add Friend/Rival")
            print("2. View Friends")
            print("3. View Rivals")
            print("4. Battle Friend/Rival")
            sub = ask("Choose")

            if sub == "1":
                try:
                    target_id = int(ask("Enter Player ID"))
                    relation_type = ask("Type ('friend' or 'rival')").strip().lower()
                    if relation_type in ["friend", "rival"]:
                        add_relationship(session, player.id, target_id, relation_type)
                    else:
                        print_error("Invalid type.")
                except ValueError:
                    print_error("Invalid input.")

            elif sub in ["2", "3"]:
                rel = "friend" if sub == "2" else "rival"
                list_relationships(session, player.id, rel)

            elif sub == "4":
                relation = ask("Battle a friend or rival?").strip().lower()
                if relation not in ["friend", "rival"]:
                    print_error("Invalid choice.")
                else:
                    ids = get_related_player_ids(session, player.id, relation)
                    if not ids:
                        print_warning(f"No {relation}s found.")
                    else:
                        for pid in ids:
                            p = session.query(Player).get(pid)
                            print(f"🆔 {p.id} | 👤 {p.username}")
                        try:
                            opponent_id = int(ask("Enter opponent ID"))
                            if opponent_id in ids:
                                simulate_battle(session, player.id, session.query(Player).get(opponent_id).username)
                            else:
                                print_error(f"Not a valid {relation}.")
                        except ValueError:
                            print_error("Invalid input.")
            else:
                print_error("Invalid option.")
            pause()

        elif choice == "7":
            view_player_profile(session, player)
            pause()

        elif choice == "8":
            print_subtitle("🏆 Leaderboards")
            print("1. Monster Collection")
            print("2. Battle Wins")
            sub = ask("Choose")
            if sub == "1":
                leaderboard_by_collection(session)
            elif sub == "2":
                leaderboard_by_wins(session)
            else:
                print_error("Invalid option.")
            pause()

        elif choice == "0":
            print("👋 Thanks for playing, tamer. Until next time!")
            break

        else:
            print_error("Invalid choice. Please try again.")


if __name__ == "__main__":
    with Session() as session:
        main(session)
