import spacy
from collections import defaultdict
import re

# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

# Helper: Check if entity looks like a full name
def is_full_name(name):
    return len(name.strip().split()) >= 2

# Helper: Filter out character names misclassified as locations
def is_valid_location(ent):
    false_positives = {
        "Neville Longbottom", "Harry Potter", "Hermione Granger",
        "Ron Weasley", "Albus Dumbledore"
    }
    return ent not in false_positives

# Helper: Try extracting a 4-digit year directly from sentence
def extract_year_from_sentence(sent):
    match = re.search(r"\b(18|19|20)\d{2}\b", sent)
    return match.group(0) if match else None

# Main entity extraction function
def extract_entities_from_text(text):
    doc = nlp(text)
    timeline = []

    for sent in doc.sents:
        sentence_text = sent.text
        date_found = None  # <-- must be reset per sentence

        entry = {
            "sentence": sentence_text,
            "characters": [],
            "locations": [],
            "date": None
        }

        person_set = set()
        location_set = set()

        for ent in sent.ents:
            if ent.label_ == "PERSON":
                if is_full_name(ent.text):
                    person_set.add(ent.text)
            elif ent.label_ in ["GPE", "LOC", "FAC"]:
                if is_valid_location(ent.text):
                    location_set.add(ent.text)
            elif ent.label_ == "DATE" and not date_found:
                # Prefer concrete years over vague dates
                year_match = re.search(r"\b(18|19|20)\d{2}\b", ent.text)
                if year_match:
                    date_found = year_match.group(0)
                else:
                    date_found = ent.text

        # Fallback if no date entity found
        if not date_found:
            date_found = extract_year_from_sentence(sentence_text)

        entry["characters"] = sorted(list(person_set))
        entry["locations"] = sorted(list(location_set))
        entry["date"] = date_found

        if person_set or location_set or date_found:
            timeline.append(entry)

    # Sort entries by date when possible
    def timeline_key(x):
        year_match = re.search(r"\b(18|19|20)\d{2}\b", x["date"] or "")
        return int(year_match.group(0)) if year_match else 9999

    timeline = sorted(timeline, key=timeline_key)
    return timeline
