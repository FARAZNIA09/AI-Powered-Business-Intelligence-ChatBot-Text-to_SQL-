import re

def extract_top_n(query):
    match = re.search(r'\d+', query)
    return int(match.group()) if match else 5

SYNONYMS = {

    "top": ["top", "best", "highest"],
    "product": ["product", "item", "goods"],
    "profit": ["profit", "earnings", "gain"],
    "sales": ["sales", "revenue", "income"],
    "region": ["region", "area", "location"],
}

def match_keywords(query, keywords):
    return any(word in query for word in keywords)