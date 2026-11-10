"""TalentHub backend - simple FastAPI service"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="TalentHub API")

class Candidate(BaseModel):
    id: int
    name: str
    role: str
    experience_years: int

candidates: List[Candidate] = []

@app.get("/candidates", response_model=List[Candidate])
async def list_candidates():
    return candidates

@app.post("/candidates", response_model=Candidate)
async def create_candidate(c: Candidate):
    if any(c.id == existing.id for existing in candidates):
        raise HTTPException(status_code=400, detail="Candidate with this ID already exists")
    candidates.append(c)
    return c

@app.get("/candidates/{candidate_id}", response_model=Candidate)
async def get_candidate(candidate_id: int):
    for c in candidates:
        if c.id == candidate_id:
            return c
    raise HTTPException(status_code=404, detail="Candidate not found")

@app.delete("/candidates/{candidate_id}")
async def delete_candidate(candidate_id: int):
    global candidates
    candidates = [c for c in candidates if c.id != candidate_id]
    return {"detail": "Deleted"}
