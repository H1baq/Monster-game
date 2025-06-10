def level_up_monster(player_monster, exp_points):
    player_monster.experience += exp_points
    level_threshold = 100 * player_monster.level  # Example threshold formula

    if player_monster.experience >= level_threshold:
        player_monster.level += 1
        player_monster.experience -= level_threshold
        apply_stat_growth(player_monster)
        print(f"{player_monster.nickname} leveled up to {player_monster.level}!")

def apply_stat_growth(player_monster):
    species_stats = player_monster.species.base_stats

    growth_factor = 1.1
    player_monster.current_hp = int(species_stats["hp"] * growth_factor ** (player_monster.level - 1))
