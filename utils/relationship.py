from models.relationship import Relationship
from models.player import Player

def add_relationship(session, player_id, target_id, relation_type):
    if player_id == target_id:
        print("⚠️ You can't befriend yourself.")
        return

    exists = session.query(Relationship).filter_by(
        player_id=player_id, target_player_id=target_id, relation_type=relation_type).first()

    if exists:
        print(f"⚠️ This {relation_type} relationship already exists.")
        return

    new_rel = Relationship(player_id=player_id, target_player_id=target_id, relation_type=relation_type)
    session.add(new_rel)
    session.commit()
    print(f"✅ {relation_type.capitalize()} added successfully.")

def list_relationships(session, player_id, relation_type):
    query = session.query(Relationship).filter_by(player_id=player_id, relation_type=relation_type)
    rels = query.all()

    if not rels:
        print("⚠️ No relationships found.")
        return

    for rel in rels:
        target = session.query(Player).filter_by(id=rel.target_player_id).first()
        if target:
            print(f"🆔 {target.id} | 👤 {target.username} | Type: {rel.relation_type}")
        else:
            print(f"⚠️ Invalid relationship found — player ID {rel.target_player_id} does not exist.")

def clean_invalid_relationships(session):
    all_relationships = session.query(Relationship).all()
    for rel in all_relationships:
        target = session.query(Player).get(rel.target_player_id)
        if not target:
            print(f"🧹 Removing invalid relationship with missing player ID: {rel.target_player_id}")
            session.delete(rel)
    session.commit()

def get_related_player_ids(session, player_id, relation_type):
    rels = session.query(Relationship).filter_by(player_id=player_id, relation_type=relation_type).all()
    return [rel.target_player_id for rel in rels]
