"""Franklin's hockey pool

Rules: Pick three teams, guess how many combined goals they will have
       at the end of the season, closest guess takes all!
"""
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Rules(BaseModel):
    rules: str

@app.get('/rules', response_model=Rules)
async def get_pool_rules():
    rules = (
        'Pick three teams, guess how many combined goals they will have '
        'at the end of the season, closest guess takes all!'
    )
    return {'rules': rules}

class SubmissionsList(BaseModel):
    submissions: List[str]

@app.get('/submissions', response_model=SubmissionsList)
async def get_submissions():
    return {'submissions': []}


class HockeyPoolEntry(BaseModel):
    """Entry for Franklin's 2020 Hockey Pool"""

    name: str = Field(
        ...,
        description='user name',
    )
    teams: List[str] = Field(
        ...,
        description='team choices',
        min_items=3,
        max_items=3,
    )
    prediction: int  = Field(
        ...,
        description='predicted total points at end of season',
        ge=0,
    )

@app.post('/submissions', response_model=HockeyPoolEntry)
async def add_submission(submission: HockeyPoolEntry):
    return submission
