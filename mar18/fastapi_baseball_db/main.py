from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException, Query
from sqlmodel import Session, select

from models import Batting, Teams, People, engine

app = FastAPI()


@app.get("/years")
async def get_years():
    # Open a database session
    with Session(engine) as session:
        # Select all distinct yearID values from Teams table
        statement = select(Teams.yearID).distinct().order_by(Teams.yearID)
        results = session.exec(statement)
        years = results.all()  # unpack each tuple
    return years

@app.get("/teams")
async def get_teams(year: int = Query(..., description="The year to get teams for")):
    with Session(engine) as session:
        # Query team names for the given year
        statement = select(Teams.name).where(Teams.yearID == year).order_by(Teams.teamID)
        results = session.exec(statement).all()

        # Flatten the results: results may be a list of 1-tuples
        team_names = [r[0] if isinstance(r, tuple) else r for r in results]

        if not team_names:
            raise HTTPException(status_code=404, detail=f"No teams found for year {year}")

    return team_names


# Serve static files
app.mount("/", StaticFiles(directory="static", html=True), name="static")