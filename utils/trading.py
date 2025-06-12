from models.trade import Trade
from models.player_monsters import PlayerMonster



def propose_trade(session, sender_id, receiver_id, offered_id, requested_id):
    trade = Trade(sender_id=sender_id, receiver_id=receiver_id,
                  offered_monster_id=offered_id, requested_monster_id=requested_id)
    session.add(trade)
    session.commit()
    print("Trade proposed!")



def respond_to_trade(session, trade_id, accept=True):
    trade = session.query(Trade).filter_by(id=trade_id).first()

    if not trade or trade.status != "pending":
        print("❌ Trade not found or already processed.")
        return

    if accept:
        offered = session.query(PlayerMonster).get(trade.offered_monster_id)
        requested = session.query(PlayerMonster).get(trade.requested_monster_id)

        # Debug prints
        print(f"🔍 Offered Monster: {offered}")
        print(f"🔍 Requested Monster: {requested}")

        if not offered or not requested:
            print("❌ One or both monsters in this trade do not exist.")
            return

        # Swap monster ownership
        offered.player_id, requested.player_id = trade.receiver_id, trade.sender_id

    trade.status = "accepted" if accept else "declined"
    session.commit()
    print(f"✅ Trade {'accepted' if accept else 'declined'}!")
