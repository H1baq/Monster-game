type_chart = {
    "Fire": {
        "strong_against": ["Grass", "Air"],
        "weak_against": ["Water", "Earth"]
    },
    "Water": {
        "strong_against": ["Fire", "Earth"],
        "weak_against": ["Grass", "Electric"]
    },
    "Grass": {
        "strong_against": ["Water", "Earth"],
        "weak_against": ["Fire", "Air"]
    },
    "Electric": {
        "strong_against": ["Water", "Air"],
        "weak_against": ["Earth"]
    },
    "Earth": {
        "strong_against": ["Electric", "Fire"],
        "weak_against": ["Water", "Grass"]
    },
    "Air": {
        "strong_against": ["Grass"],
        "weak_against": ["Electric", "Fire"]
    }
}

def get_type_effectiveness(attacker_type, defender_type):
    if defender_type in type_chart.get(attacker_type, {}).get("strong_against", []):
        return "strong"
    elif defender_type in type_chart.get(attacker_type, {}).get("weak_against", []):
        return "weak"
    else:
        return "neutral"
