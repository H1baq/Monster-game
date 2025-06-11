import random
from models.battle import Battle
from models.player import Player
from models.player_monsters import PlayerMonster
from utils.battle_logger import log_battle
from models.monster_species import MonsterSpecies
from utils.rewards import reward_player

def calculate_damage(attacker, defender):
    attack = attacker.species.base_stats.get("attack", 10)
    defense = defender.species.base_stats.get("defense", 5)
    return max(1, attack - defense // 2)

def simulate_turn_based_combat(player_mon, opponent_mon):
    player_hp = player_mon.species.base_stats.get("hp", 100)
    opponent_hp = opponent_mon.species.base_stats.get("hp", 100)

    print("\n🌀 Turn-Based Battle Begins!")
    while player_hp > 0 and opponent_hp > 0:
        # Player attacks first
        dmg = calculate_damage(player_mon, opponent_mon)
        opponent_hp -= dmg
        print(f"👉 {player_mon.nickname} hits for {dmg} damage! (Opponent HP: {max(opponent_hp, 0)})")
        if opponent_hp <= 0:
            return "player"

        # Opponent counter-attacks
        dmg = calculate_damage(opponent_mon, player_mon)
        player_hp -= dmg
        print(f"👈 {opponent_mon.nickname} hits for {dmg} damage! (Your HP: {max(player_hp, 0)})")
        if player_hp <= 0:
            return "opponent"

    return None

def determine_difficulty(player_level, opponent_level):
    level_diff = opponent_level - player_level
    if level_diff >= 3:
        return "epic"
    elif level_diff >= 1:
        return "hard"
    return "normal"

def simulate_battle(session, player1_id, opponent_username):
    player1 = session.query(Player).get(player1_id)
    player2 = session.query(Player).filter_by(username=opponent_username).first()

    if not player1 or not player2:
        print("❌ One or both players not found.")
        return

    if player1.id == player2.id:
        print("❌ You can't battle yourself!")
        return

    p1_monsters = session.query(PlayerMonster).filter_by(player_id=player1.id).all()
    p2_monsters = session.query(PlayerMonster).filter_by(player_id=player2.id).all()

    if not p1_monsters or not p2_monsters:
        print("❌ Both players need at least one monster to battle.")
        return

    p1_mon = random.choice(p1_monsters)
    p2_mon = random.choice(p2_monsters)

    print(f"\n⚔️ Battle Start! {player1.username} vs {player2.username}")
    print(f"{player1.username}'s Monster: {p1_mon.species.name} (Lvl {p1_mon.level})")
    print(f"{player2.username}'s Monster: {p2_mon.species.name} (Lvl {p2_mon.level})")

    outcome = simulate_turn_based_combat(p1_mon, p2_mon)
    if outcome == "player":
        winner = player1
        loser = player2
        difficulty = determine_difficulty(p1_mon.level, p2_mon.level)
    elif outcome == "opponent":
        winner = player2
        loser = player1
        difficulty = determine_difficulty(p2_mon.level, p1_mon.level)
    else:
        print("\n🤝 It's a draw!")
        log_battle(session, player1.id, player2.id, None, result="draw")
        player1.total_battles += 1
        player2.total_battles += 1
        session.commit()
        return

    print(f"\n🏆 {winner.username} wins the battle!")

    log_battle(session, player1.id, player2.id, winner.id, result="win")
    winner.total_battles += 1
    winner.wins += 1
    loser.total_battles += 1

    reward_player(session, winner, difficulty=difficulty)
    session.commit()

def simulate_ai_battle(session, player):
    player_monsters = session.query(PlayerMonster).filter_by(player_id=player.id).all()

    if not player_monsters:
        print("\n⚠️ You need at least one monster to battle!")
        return

    player_mon = random.choice(player_monsters)

    species_list = session.query(MonsterSpecies).all()
    if not species_list:
        print("❌ No monster species available in the database.")
        return

    species = random.choice(species_list)
    ai_mon_level = max(1, player_mon.level + random.choice([-1, 0, 1]))
    ai_mon = PlayerMonster(
        species_id=species.id,
        nickname="CPU-Mon",
        level=ai_mon_level,
        experience=ai_mon_level * 100,
        current_hp=species.base_stats.get("hp", 100)
    )

    player_mon.current_hp = player_mon.species.base_stats.get("hp", 100)

    print("\n⚔️ Battle Start! Player vs CPU")
    print(f"Your Monster: {player_mon.species.name} (Lvl {player_mon.level})")
    print(f"CPU Monster: {species.name} (Lvl {ai_mon.level})")

    player_stats = player_mon.species.base_stats
    ai_stats = species.base_stats

    turn = 0
    while player_mon.current_hp > 0 and ai_mon.current_hp > 0:
        attacker = "Player" if turn % 2 == 0 else "CPU"
        if attacker == "Player":
            damage = max(1, player_stats["attack"] - ai_stats["defense"])
            ai_mon.current_hp -= damage
            print(f"\n🗡️ {player_mon.species.name} attacks CPU for {damage} damage! CPU HP: {max(ai_mon.current_hp, 0)}")
        else:
            damage = max(1, ai_stats["attack"] - player_stats["defense"])
            player_mon.current_hp -= damage
            print(f"\n🛡️ CPU attacks {player_mon.species.name} for {damage} damage! Your HP: {max(player_mon.current_hp, 0)}")

        turn += 1

    difficulty = determine_difficulty(player_mon.level, ai_mon.level)

    if player_mon.current_hp > 0:
        winner = player
        result = "win"
        print("\n🏆 You won the battle!")
        player.wins += 1
        reward_player(session, player, difficulty=difficulty)
    else:
        winner = None
        result = "loss"
        print("\n💀 You lost the battle!")

    player.total_battles += 1
    log_battle(session, player.id, None, player.id if winner else None, result=result)
    session.commit()
