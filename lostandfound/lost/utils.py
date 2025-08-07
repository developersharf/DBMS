import difflib
from datetime import timedelta

def calculate_match_score(lost_item, found_item):
    score = 0

    # Title similarity (0-30)
    title_score = difflib.SequenceMatcher(None, lost_item['title'], found_item['title']).ratio() * 30
    score += title_score

    # Description similarity (0-30)
    desc_score = difflib.SequenceMatcher(None, lost_item['description'], found_item['description']).ratio() * 30
    score += desc_score

    # Location match (10)
    if lost_item['location'].lower() == found_item['location'].lower():
        score += 10

    # Date proximity (max 30)
    date_diff = abs((lost_item['date_lost'] - found_item['date_found']).days)
    if date_diff == 0:
        score += 30
    elif date_diff <= 3:
        score += 20
    elif date_diff <= 7:
        score += 10

    return round(score, 2)
