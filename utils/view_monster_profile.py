def view_monster_profile(monster):
    print("\n=== MONSTER PROFILE ===")
    print(f"🆔 ID: {monster.id}")
    print(f"🐉 Species: {monster.species.name}")
    print(f"🏷️ Nickname: {monster.nickname or 'None'}")
    print(f"🎚️ Level: {monster.level}")
    print(f"🧠 EXP: {monster.experience} / {monster.level * 100}")
    print(f"❤️ HP: {monster.current_hp}")
    print(f"👤 Owner: {monster.player.username}")
