from sqlalchemy import func
from models.player import Player
from models.player_monsters import PlayerMonster

def leaderboard_by_collection(session, limit=10):
    results = (
        session.query(
            Player.id,
            Player.username,
            func.count(PlayerMonster.id).label("monster_count")
        )
        .join(PlayerMonster, Player.id == PlayerMonster.player_id)
        .group_by(Player.id)
        .order_by(func.count(PlayerMonster.id).desc())
        .limit(limit)
        .all()
    )

    print("\n🏆 Monster Collection Leaderboard:")
    for rank, (pid, username, count) in enumerate(results, start=1):
        print(f"{rank}. 👤 {username} — 🐉 Monsters: {count}")

def leaderboard_by_wins(session, limit=10):
    results = (
        session.query(
            Player.id,
            Player.username,
            Player.wins
        )
        .order_by(Player.wins.desc())
        .limit(limit)
        .all()
    )

    print("\n🏆 Battle Wins Leaderboard:")
    for rank, (pid, username, wins) in enumerate(results, start=1):
        print(f"{rank}. 👤 {username} — ✅ Wins: {wins}")
