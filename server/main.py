from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import json
import os
from extractors.named_entity_extractor import extract_entities

app = FastAPI()

class StoryText(BaseModel):
    text: str

if not os.path.exists("storage"):
    os.makedirs("storage")

@app.get("/")
def read_root():
    return {"message": "Fictional Universe Consistency Kit backend is running!"}

@app.post("/analyze")
def analyze_story(story: StoryText):
    timeline = extract_entities(story.text)

    # Save to storage (optional)
    # filename = f"storage/{uuid.uuid4()}.json"
    # with open(filename, "w") as f:
    #     json.dump({"timeline": timeline, "original_text": story.text}, f)

    return {
        "timeline": timeline,
        "original_text": story.text
    }

@app.get("/analyzed")
def get_all_analyzed():
    analyzed_files = []
    for file_name in os.listdir("storage"):
        with open(f"storage/{file_name}", "r") as f:
            analyzed_files.append(json.load(f))
    return analyzed_files
