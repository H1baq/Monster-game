from models.battle import Battle
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
