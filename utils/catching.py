from models.player import Player
from models.player_monsters import PlayerMonster
from models.monster_species import MonsterSpecies
from utils.player_progression import add_experience

import random

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
            nickname=species.name
        )
        session.add(new_monster)

        exp_gained = 50 if species.rarity == "common" else 100
        leveled_up = player.gain_experience(exp_gained)

        session.commit()

        print(f"✅ You caught {species.name}!")
        print(f"🧠 You gained {exp_gained} EXP!")
        if leveled_up:
            print(f"⬆️ You leveled up to Level {player.level}!")
    else:
        print(f"❌ {species.name} escaped.")

