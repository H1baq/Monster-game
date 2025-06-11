import random
from models.player_monsters import PlayerMonster
from models.monster_species import MonsterSpecies

def reward_player(session, player, difficulty="normal"):
    """
    Grant post-battle rewards based on difficulty.
    - normal: baseline rewards
    - hard: better XP and money
    - epic: best rewards, chance to get a rare monster
    """
    rewards = {
        "normal": {"xp": random.randint(20, 40), "money": random.randint(50, 100), "crate": "Bronze"},
        "hard": {"xp": random.randint(50, 80), "money": random.randint(100, 200), "crate": "Silver"},
        "epic": {"xp": random.randint(100, 150), "money": random.randint(200, 500), "crate": "Gold"},
    }

    reward = rewards.get(difficulty, rewards["normal"])
    print(f"\n🎁 You earned a {reward['crate']} crate!")

    # Apply XP and money reward
    player.gain_experience(reward["xp"])
    player.money = getattr(player, "money", 0) + reward["money"]

    print(f"💰 You received {reward['money']} coins and {reward['xp']} XP.")

    # Rare monster reward for epic crates
    if reward["crate"] == "Gold":
        rare_species = session.query(MonsterSpecies).filter_by(rarity="Legendary").all()
        if rare_species:
            new_mon_species = random.choice(rare_species)
            new_mon = PlayerMonster(
                player_id=player.id,
                species_id=new_mon_species.id,
                nickname=new_mon_species.name,
                level=1,
                experience=0,
                current_hp=new_mon_species.base_stats.get("hp", 100)
            )
            session.add(new_mon)
            print(f"🌟 BONUS: You found a rare monster: {new_mon_species.name}!")

    session.commit()
