from models.player_monsters import PlayerMonster

def view_player_profile(session, player):
    print("\n=== 📊 PLAYER PROFILE ===")
    print(f"👤 Username: {player.username}")
    print(f"🎚️ Level: {player.level}")
    print(f"🧠 Experience: {round(player.experience, 1)}")
    print(f"💰 Money: £{round(player.money, 2)}")

    monster_count = session.query(PlayerMonster).filter_by(player_id=player.id).count()
    print(f"👾 Monsters Caught: {monster_count}")

    # Optional: Most powerful monster
    top_monster = (
        session.query(PlayerMonster)
        .filter_by(player_id=player.id)
        .order_by(PlayerMonster.level.desc())
        .first()
    )

    if top_monster:
        print(f"🏆 Strongest Monster: {top_monster.nickname} (Lv {top_monster.level})")
    else:
        print("📉 You haven't caught any monsters yet.")
