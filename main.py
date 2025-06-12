from db import Session
from models.player import Player
from models.player_monsters import PlayerMonster
from utils.auth import login_or_create_player
from utils.catching import try_catch_monster
from utils.leveling import level_up_monster
from utils.view_inventory import view_inventory
from utils.view_profile import view_player_profile
from utils.view_monster_profile import view_monster_profile
from utils.battle_logger import log_battle
from utils.battle_engine import simulate_battle, simulate_ai_battle
from utils.battle_logger import view_battle_history
from utils.shop import open_monster_shop
from utils.trading import propose_trade, respond_to_trade, list_player_ids, list_player_monsters, list_pending_trades

def main(session):
    player = login_or_create_player(session)

    while True:
        session.refresh(player)
        print(f"\n=== MONSTER TAMER HUB — Logged in as {player.username} ===")
        print(f"🔹 Level: {player.level} | 🧠 XP: {round(player.experience, 1)} | 💰 Money: ${round(player.money, 2)}")
        print(f"⚔️ Battles: {player.total_battles} | ✅ Wins: {player.wins} | ❌ Losses: {player.losses} | 🏆 Win Rate: {player.win_rate}%")
        print("1. Catch a Monster")
        print("2. View Inventory")
        print("3. Level Up a Monster")
        print("4. View Player Profile")
        print("5. View Monster Profile")
        print("6. Battle a CPU Trainer")
        print("7. Battle Another Player")
        print("8. View Battle History")
        print("9. Visit Ultra Rare Monster Shop")
        print("10. Trade Monsters")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            try_catch_monster(session, player.id)

        elif choice == "2":
            view_inventory(session, player)

        elif choice == "3":
            try:
                monster_id = int(input("Enter monster ID to train: "))
                monster = session.query(PlayerMonster).filter_by(id=monster_id).first()
                if monster and monster.player_id == player.id:
                    level_up_monster(monster, exp_points=120)
                    session.commit()
                else:
                    print("❌ No monster found with that ID or it's not yours.")
            except ValueError:
                print("⚠️ Please enter a valid number.")

        elif choice == "4":
            view_player_profile(session, player)

        elif choice == "5":
            player_monsters = session.query(PlayerMonster).filter_by(player_id=player.id).all()

            if not player_monsters:
                print("⚠️ You don't have any monsters yet.")
                continue

            print("\n📖 Your Monsters:")
            for m in player_monsters:
                print(f"🆔 ID: {m.id} | 🐉 {m.species.name} | 🌚 Lvl: {m.level} | 🧠 EXP: {m.experience} | ❤️ HP: {m.current_hp} | 🏽 Nickname: {m.nickname or 'None'}")

            try:
                monster_id = int(input("\nEnter Monster ID to view profile: "))
                monster = session.query(PlayerMonster).filter_by(id=monster_id, player_id=player.id).first()

                if monster:
                    view_monster_profile(monster)
                else:
                    print("❌ Monster not found or doesn't belong to you.")
            except ValueError:
                print("⚠️ Invalid input. Please enter a valid number.")

        elif choice == "6":
            simulate_ai_battle(session, player)

        elif choice == "7":
            opponent_username = input("Enter the username of the player you want to battle: ").strip()
            simulate_battle(session, player.id, opponent_username)

        elif choice == "8":
            view_battle_history(session, player)

        elif choice == "9":
            open_monster_shop(session, player)

        elif choice == "10":
            print("\n📦 Monster Trading Center")
            print("\nAvailable Players:")
            list_player_ids(session)

            print("\nYour Monsters:")
            list_player_monsters(session, player.id)

            print("\nPending Trades:")
            list_pending_trades(session)

            sub_choice = input("\n1. Propose Trade\n2. Respond to Trade\nChoose: ")

            if sub_choice == "1":
                try:
                    receiver_id = int(input("Enter Receiver's Player ID: "))
                    offered_id = int(input("Enter YOUR Monster ID to offer: "))
                    requested_id = int(input("Enter Receiver's Monster ID to request: "))
                    propose_trade(session, player.id, receiver_id, offered_id, requested_id)
                except ValueError:
                    print("⚠️ Invalid input. Please enter valid numbers.")

            elif sub_choice == "2":
                try:
                    trade_id = int(input("Enter Trade ID to respond to: "))
                    decision = input("Accept trade? (yes/no): ").lower()
                    respond_to_trade(session, trade_id, accept=(decision == "yes"))
                except ValueError:
                    print("⚠️ Invalid input.")
            else:
                print("❌ Invalid choice.")

        elif choice == "0":
            print("Rest well, fierce tamer!")
            break

        else:
            print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    with Session() as session:
        main(session)
