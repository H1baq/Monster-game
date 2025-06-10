from models.player_monsters import PlayerMonster

def view_inventory(session, player):
    monsters = session.query(PlayerMonster).filter_by(player_id=player.id).all()
    if monsters:
        print(f"\n{player.username}'s Monster Collection:")
        for pm in monsters:
            print(f"- {pm.nickname or pm.species.name} (Level {pm.level}) - {pm.species.type}")
    else:
        print("You have no monsters yet!")
