

from models.player import Player
from models.monster_species import MonsterSpecies
from models.player_monster import PlayerMonster
import random

# Catching a monster based on species rarity
def try_catch_monster(session, player_id):
    player = session.query(Player).filter_by(id=player_id).first()
    species = random.choice(session.query(MonsterSpecies).all())

    RARITY_PROBABILITIES = {
        "common": 0.8,
        "uncommon": 0.6,
        "rare": 0.4,
        "legendary": 0.2
    }

    catch_chance = RARITY_PROBABILITIES.get(species.rarity.lower(), 0.5)
    
    if random.random() <= catch_chance:
        new_monster = PlayerMonster(
            player=player,
            species=species,
            level=1,
            current_hp=species.base_stats["hp"],
            nickname=species.name,
        )
        session.add(new_monster)
        session.commit()
        print(f"✅ You caught {species.name}!")
    else:
        print(f"❌ {species.name} escaped.")


# Level up a player's monster
def level_up_monster(session, monster_id, exp_points):
    monster = session.query(PlayerMonster).filter_by(id=monster_id).first()
    if not monster:
        print("❌ Monster not found.")
        return

    if not hasattr(monster, "experience"):
        monster.experience = 0  

    monster.experience += exp_points
    level_threshold = 100 * monster.level  

    if monster.experience >= level_threshold:
        monster.level += 1
        monster.experience -= level_threshold
        apply_stat_growth(monster)
        print(f"🔼 {monster.nickname} leveled up to {monster.level}!")

    session.commit()


def apply_stat_growth(monster):
    stats = monster.species.base_stats
    growth_factor = 1.1
    monster.current_hp = int(stats["hp"] * growth_factor ** (monster.level - 1))
