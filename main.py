from fastapi import FastAPI, Query
from typing import List
from rapidfuzz import process, fuzz
from random import shuffle

app = FastAPI(title="Product Matcher API")

# Global corpus of titles (index = ID)
title_corpus: List[str] = []

@app.on_event("startup")
def load_titles():
    global title_corpus
    with open("title_corpus.txt", "r", encoding="utf-8") as f:
        title_corpus = [line.strip() for line in f]
    shuffle(title_corpus)

@app.get("/match-products")
def match_products(input_title: str = Query(..., description="Product title to match")):
    if not title_corpus:
        return {"error": "Title corpus not loaded."}

    matches = process.extract(
        input_title,
        title_corpus,
        scorer=fuzz.ratio,
        score_cutoff=80,
        limit=5
    )

    results = [
        {"title": match[0], "id": match[2], "score": match[1]}
        for match in matches
    ]

    return {"input_title": input_title, "matches": results}
