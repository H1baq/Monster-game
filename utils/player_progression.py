def calculate_level_up_threshold(level):
    """Returns the XP required to reach the next level"""
    return 100 + (level - 1) * 50 


def add_experience(player, exp_gained):
    player.experience += exp_gained
    leveled_up = False

    while player.experience >= calculate_level_up_threshold(player.level):
        player.experience -= calculate_level_up_threshold(player.level)
        player.level += 1
        leveled_up = True
        print(f"🎉 {player.username} leveled up! Now level {player.level}!")

    return leveled_up
