from fastapi import FastAPI
from pydantic import BaseModel
import spacy
import uuid
import json
import os

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Create FastAPI app
app = FastAPI()

# Define request body structure
class StoryText(BaseModel):
    text: str

# Storage directory for saving analyzed data
if not os.path.exists("storage"):
    os.makedirs("storage")

@app.get("/")
def read_root():
    return {"message": "Fictional Universe Consistency Kit backend is running!"}

@app.post("/analyze")
def analyze_story(story: StoryText):
    # Process the story text with spaCy
    doc = nlp(story.text)

    # Organize extracted entities by type
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

    # Prepare the response data
    response_data = {
        "original_text": story.text,
        "categorized_entities": categorized_entities
    }

    # Save the analyzed data in the storage folder
    file_name = f"storage/{uuid.uuid4()}.json"
    with open(file_name, "w") as f:
        json.dump(response_data, f, indent=2)

    # Return the analyzed response
    return response_data

@app.get("/analyzed")
def get_all_analyzed():
    # Read all files in the storage folder
    analyzed_files = []
    for file_name in os.listdir("storage"):
        with open(f"storage/{file_name}", "r") as f:
            analyzed_files.append(json.load(f))

    # Return all saved analysis
    return analyzed_files
