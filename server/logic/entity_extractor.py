import spacy

# Load spaCy model for entity extraction
nlp = spacy.load("en_core_web_sm")

def extract_entities_from_text(text):
    doc = nlp(text)
    categorized_entities = {
        "characters": [],
        "locations": [],
        "dates": [],
        "organizations": []
    }

    # Classify entities into their respective categories
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            categorized_entities["characters"].append(ent.text)
        elif ent.label_ == "GPE" or ent.label_ == "LOC":
            categorized_entities["locations"].append(ent.text)
        elif ent.label_ == "DATE":
            categorized_entities["dates"].append(ent.text)
        elif ent.label_ == "ORG":
            categorized_entities["organizations"].append(ent.text)

    return categorized_entities
