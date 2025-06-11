from models.player import Player

def login_or_create_player(session):
    print("🎮 Welcome to Monster Collector!")
    username = input("Enter your username: ").strip()

    player = session.query(Player).filter_by(username=username).first()

    if player:
        print(f"✅ Welcome back, {player.username} (Lv.{player.level})!")
    else:
        print(f"🔍 No profile found for '{username}'.")
        create = input("Do you want to create a new player? (y/n): ").lower()
        if create == 'y':
            player = Player(username=username)
            session.add(player)
            session.commit()
            print(f"🎉 Player '{username}' created successfully!")
        else:
            print("❌ Exiting game.")
            exit()

    return player
