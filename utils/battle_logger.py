from models.battle import Battle
from models.player import Player
from datetime import datetime

def log_battle(session, player1_id, player2_id, winner_id=None, result="draw"):
    battle = Battle(
        player1_id=player1_id,
        player2_id=player2_id,
        winner_id=winner_id,
        result=result,
        timestamp=datetime.utcnow()
    )
    session.add(battle)
    session.commit()
    print(f"✅ Battle Results: {result.upper()} Player {player1_id} between Player {player2_id}!")


def view_battle_history(session, player: Player):
    print("\n📜 Battle History:\n")

    battles = session.query(Battle).filter(
        (Battle.player1_id == player.id) | (Battle.player2_id == player.id)
    ).order_by(Battle.timestamp.desc()).limit(10).all()

    if not battles:
        print("You haven't fought any battles yet.")
        return

    for b in battles:
        opponent_id = b.player2_id if b.player1_id == player.id else b.player1_id
        opponent = session.query(Player).get(opponent_id) if opponent_id else "CPU"
        opponent_name = opponent.username if isinstance(opponent, Player) else "CPU"

        if b.winner_id == player.id:
            result = "🏆 Victory"
        elif b.winner_id is None:
            result = "🤝 Draw"
        else:
            result = "💀 Defeat"

        print(f"🆚 vs {opponent_name} — {result} — {b.timestamp.strftime('%Y-%m-%d %H:%M')}")
