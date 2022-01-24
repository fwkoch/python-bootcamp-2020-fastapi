from datetime import datetime
from typing import List
from urllib.parse import urlunparse
import uuid

import aiohttp
from fastapi import FastAPI, HTTPException
from fuzzywuzzy import process
from pydantic import AnyHttpUrl, BaseModel, Field
from starlette.requests import Request


async def fetch_team_wins() -> dict:
    """Use the NHL API to get teams and goals this season"""
    standings_url = "https://statsapi.web.nhl.com/api/v1/standings?season=20192020"
    session = aiohttp.ClientSession()
    resp = await session.get(standings_url)
    await session.close()
    standings = await resp.json()
    teams = {}
    try:
        for record in standings["records"]:
            for team_record in record["teamRecords"]:
                teams.update({team_record["team"]["name"]: team_record["goalsScored"]})
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid standings response")
    return teams


DB = {}  # Yikes! Please use a real database, not just a dictionary...
NAMESPACE_UUID = uuid.uuid4()


def db_uid(name: str) -> str:
    return str(uuid.uuid3(NAMESPACE_UUID, name))


app = FastAPI(name="Franklin's hockey pool")


class Links(BaseModel):
    self: AnyHttpUrl
    submissions: AnyHttpUrl
    rules: AnyHttpUrl

    @classmethod
    def from_url(cls, url):
        links = cls(
            self=str(url),
            submissions=urlunparse(
                (url.scheme, url.netloc, "/submissions", "", "", "")
            ),
            rules=urlunparse((url.scheme, url.netloc, "/rules", "", "", "")),
        )
        return links


class RulesResponse(BaseModel):
    rules: str
    links: Links


@app.get("/rules", response_model=RulesResponse)
async def get_the_pool_rules(request: Request):
    """Get the rules and links to submissions"""
    rules = (
        "Pick three teams, guess how many combined goals they will have "
        "at the end of the season, closest guess takes all!"
    )
    return {"rules": rules, "links": Links.from_url(request.url)}


class SubmissionsResponse(BaseModel):
    submissions: List[AnyHttpUrl]
    links: Links


@app.get("/submissions", response_model=SubmissionsResponse)
async def get_submissions(request: Request):
    """Get links to all submissions"""
    submissions = [f"{str(request.url)}/{db_uid(sub.name)}" for sub in DB.values()]
    return {"submissions": submissions, "links": Links.from_url(request.url)}


class Submission(BaseModel):
    name: str = Field(
        ...,
        description="user name",
    )
    teams: List[str] = Field(
        ...,
        description="team choices",
        min_items=3,
        max_items=3,
    )
    prediction: int = Field(
        ...,
        description="predicted total points at end of season",
        ge=0,
    )


class SubmissionDB(Submission):
    uid: str
    time: datetime


class SubmissionPostResponse(Submission):
    links: Links


@app.post("/submissions", response_model=SubmissionPostResponse)
async def post_submission(submission: Submission, request: Request):
    """Add your submission to the pool"""
    uid = db_uid(submission.name)
    if uid in DB:
        raise HTTPException(
            status_code=422, detail=f"Entry already exists for {submission.name}"
        )
    DB[uid] = SubmissionDB(uid=uid, time=datetime.utcnow(), **submission.dict())
    links = Links.from_url(request.url)
    links.self += f"/{uid}"
    return dict(links=links, **submission.dict())


class SubmissionGetResponse(SubmissionPostResponse):
    current_score: int


@app.get("/submissions/{uid}", response_model=SubmissionGetResponse)
async def get_submission(uid: str, request: Request):
    """Get a submission with the current score"""
    if uid not in DB:
        raise HTTPException(status_code=404, detail="Not found")
    submission = DB[uid]
    standings = await fetch_team_wins()
    current_score = 0
    for team in submission.teams:
        match = process.extractOne(team, standings.keys())
        current_score += standings[match[0]]
    links = Links.from_url(request.url)
    return dict(links=links, current_score=current_score, **submission.dict())
