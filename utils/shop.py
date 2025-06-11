from models.monster_species import MonsterSpecies
from models.player_monsters import PlayerMonster
import random

RARITY_PRICES = {
    "Common": 100,
    "Uncommon": 250,
    "Rare": 400,
    "Legendary": 600
}

def open_monster_shop(session, player):
    print("\n🏪 Welcome to the Ultra Rare Monster Shop!")
    print(f"💰 Your Balance: {player.money:.2f} coins")

    rarity_order = {"Legendary": 0, "Rare": 1, "Uncommon": 2, "Common": 3}
    monsters = session.query(MonsterSpecies).all()
    monsters.sort(key=lambda m: rarity_order.get(m.rarity, 4))

    if not monsters:
        print("⚠️ No monsters available in the shop right now.")
        return

    print("\n🧾 Available Monsters:\n")
    for idx, m in enumerate(monsters, 1):
        stats = m.base_stats
        price = RARITY_PRICES.get(m.rarity, 500)
        print(f"{idx}. {m.name} ({m.type} - {m.rarity}) - 💰 {price} coins")
        print(f"   HP: {stats['hp']}, ATK: {stats['attack']}, DEF: {stats['defense']}, SPD: {stats['speed']}")
        print(f"   Abilities: {', '.join(m.abilities)}")

    choice = input("\nEnter the number of the monster you want to buy (or press Enter to cancel): ").strip()
    if not choice.isdigit():
        print("❌ Cancelled or invalid input.")
        return

    index = int(choice) - 1
    if 0 <= index < len(monsters):
        selected = monsters[index]
        price = RARITY_PRICES.get(selected.rarity, 500)

        if player.money < price:
            print(f"❌ Not enough coins! You have {player.money:.2f}, but {selected.name} costs {price}.")
            return

        level = random.randint(1, 5)
        monster = PlayerMonster(
            player_id=player.id,
            species_id=selected.id,
            nickname=selected.name,
            level=level,
            experience=0,
            current_hp=selected.base_stats["hp"]
        )

        player.money -= price 
        session.add(monster)
        session.commit()

        print(f"🎉 You purchased {selected.name} (Lvl {level}) for {price} coins!")
        print(f"💰 Remaining Balance: {player.money:.2f} coins")
    else:
        print("❌ Invalid selection.")
