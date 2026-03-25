from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException, Query
from sqlmodel import Session, select

from models import Batting, Teams, People, engine

app = FastAPI()


@app.get("/years")
async def get_years():
    with Session(engine) as session:
        statement = select(Teams.yearID).distinct().order_by(Teams.yearID)
        results = session.exec(statement).all()
        # Flatten tuples
        years = [r[0] if isinstance(r, tuple) else r for r in results]
    return years

@app.get("/teams")
async def get_teams(year: int = Query(..., description="The year to get teams for")):
    with Session(engine) as session:
        statement = select(
            Teams.teamID,
            Teams.name,
            Teams.lgID,
            Teams.divID
        ).where(Teams.yearID == year).order_by(Teams.teamID)

        results = session.exec(statement).all()

        # Convert results into a list of dicts
        teams = [{"teamID": r[0], "name": r[1], "lgID": r[2], "divID": r[3]} for r in results]

        if not teams:
            raise HTTPException(status_code=404, detail=f"No teams found for year {year}")

    return teams

@app.get("/players")
async def get_players(year: int = Query(...), teamID: str = Query(...)):
    with Session(engine) as session:
        # Join Batting and People to get first/last name
        statement = (
            select(People.playerID, People.nameFirst, People.nameLast)
            .join(Batting, People.playerID == Batting.playerID)
            .where(Batting.yearID == year, Batting.teamID == teamID)
            .order_by(People.nameLast, People.nameFirst)
        )
        results = session.exec(statement).all()

        if not results:
            raise HTTPException(status_code=404, detail=f"No players found for team {teamID} in {year}")

        # Combine first + last into single 'name' field
        players = [{"playerID": r[0], "name": f"{r[1]} {r[2]}"} for r in results]

    return players

from datetime import date, datetime
from decimal import Decimal
from fastapi import HTTPException, Query
from sqlmodel import Session, select


@app.get("/player-info-full")
async def get_player_info_full(playerID: str):
    with Session(engine) as session:
        # Personal info
        person = session.exec(select(People).where(People.playerID == playerID)).first()
        if not person:
            raise HTTPException(status_code=404, detail="Player not found")

        personal_info = {field: getattr(person, field) for field in person.__fields__}

        # Batting stats
        batting_rows = session.exec(select(Batting).where(Batting.playerID == playerID)).all()
        batting_stats = []
        for row in batting_rows:
            # Use Python attribute names only
            row_dict = {field: getattr(row, field) for field in row.__fields__}
            batting_stats.append(row_dict)

    return {"personal": personal_info, "battingStats": batting_stats}


# Serve static files
app.mount("/", StaticFiles(directory="static", html=True), name="static")