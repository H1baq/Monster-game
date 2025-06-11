from db import Session
from models.player import Player
from models.player_monsters import PlayerMonster
from utils.auth import login_or_create_player
from utils.catching import try_catch_monster
from utils.leveling import level_up_monster
from utils.view_inventory import view_inventory

def main(session):
    # 🔐 Login or create player
    player = login_or_create_player(session)

    while True:
        print(f"\n=== MONSTER TAMER HUB — Logged in as {player.username} ===")
        print(f"🔹 Level: {player.level} | 🧠 XP: {round(player.experience, 1)} | 💰 Money: ${round(player.money, 2)}")
        print("1. Catch a Monster")
        print("2. View Inventory")
        print("3. Level Up a Monster")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            try_catch_monster(session, player.id)
            session.refresh(player)  # Refresh to get updated EXP/Level
        elif choice == "2":
            view_inventory(session, player)
        elif choice == "3":
            monster_id = int(input("Enter monster ID to level up: "))
            monster = session.query(PlayerMonster).filter_by(id=monster_id).first()
            if monster and monster.player_id == player.id:
                level_up_monster(monster, exp_points=120)
                session.commit()
            else:
                print("❌ No monster found with that ID or it's not yours.")
        elif choice == "4":
            print("Rest well, fierce tamer!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    session = Session()
    main(session)
