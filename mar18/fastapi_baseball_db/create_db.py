import pandas as pd
import sqlite3

# Connect to database (creates Baseball.db)
conn = sqlite3.connect("Baseball.db")
cursor = conn.cursor()

# Enable foreign keys
cursor.execute("PRAGMA foreign_keys = ON;")

# -------------------------
# Load CSV files
# -------------------------
people_df = pd.read_csv("people.csv")
teams_df = pd.read_csv("teams.csv")
batting_df = pd.read_csv("Batting.csv")

# -------------------------
# Drop tables if they exist
# -------------------------
cursor.executescript("""
DROP TABLE IF EXISTS batting;
DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS people;
""")

# -------------------------
# Create PEOPLE table
# -------------------------
cursor.execute("""
CREATE TABLE people (
    playerID TEXT PRIMARY KEY,
    ID INTEGER,
    birthYear INTEGER,
    birthMonth INTEGER,
    birthDay INTEGER,
    birthCity TEXT,
    birthCountry TEXT,
    birthState TEXT,
    deathYear INTEGER,
    deathMonth INTEGER,
    deathDay INTEGER,
    deathCountry TEXT,
    deathState TEXT,
    deathCity TEXT,
    nameFirst TEXT,
    nameLast TEXT,
    nameGiven TEXT,
    weight INTEGER,
    height INTEGER,
    bats TEXT,
    throws TEXT,
    debut TEXT,
    bbrefID TEXT,
    finalGame TEXT,
    retroID TEXT
);
""")

# -------------------------
# Create TEAMS table
# -------------------------
cursor.execute("""
CREATE TABLE teams (
    yearID INTEGER,
    lgID TEXT,
    teamID TEXT,
    franchID TEXT,
    divID TEXT,
    Rank INTEGER,
    G INTEGER,
    Ghome INTEGER,
    W INTEGER,
    L INTEGER,
    DivWin TEXT,
    WCWin TEXT,
    LgWin TEXT,
    WSWin TEXT,
    R INTEGER,
    AB INTEGER,
    H INTEGER,
    "2B" INTEGER,
    "3B" INTEGER,
    HR INTEGER,
    BB INTEGER,
    SO INTEGER,
    SB INTEGER,
    CS INTEGER,
    HBP INTEGER,
    SF INTEGER,
    RA INTEGER,
    ER INTEGER,
    ERA REAL,
    CG INTEGER,
    SHO INTEGER,
    SV INTEGER,
    IPouts INTEGER,
    HA INTEGER,
    HRA INTEGER,
    BBA INTEGER,
    SOA INTEGER,
    E INTEGER,
    DP INTEGER,
    FP REAL,
    name TEXT,
    park TEXT,
    attendance INTEGER,
    BPF INTEGER,
    PPF INTEGER,
    teamIDBR TEXT,
    teamIDlahman45 TEXT,
    teamIDretro TEXT,
    PRIMARY KEY (teamID, yearID)
);
""")

# -------------------------
# Create BATTING table
# -------------------------
cursor.execute("""
CREATE TABLE batting (
    playerID TEXT,
    yearID INTEGER,
    stint INTEGER,
    teamID TEXT,
    lgID TEXT,
    G INTEGER,
    AB INTEGER,
    R INTEGER,
    H INTEGER,
    "2B" INTEGER,
    "3B" INTEGER,
    HR INTEGER,
    RBI INTEGER,
    SB INTEGER,
    CS INTEGER,
    BB INTEGER,
    SO INTEGER,
    IBB INTEGER,
    HBP INTEGER,
    SH INTEGER,
    SF INTEGER,
    GIDP INTEGER,
    PRIMARY KEY (playerID, yearID, stint),
    FOREIGN KEY (playerID) REFERENCES people(playerID),
    FOREIGN KEY (teamID, yearID) REFERENCES teams(teamID, yearID)
);
""")

# -------------------------
# Insert data
# -------------------------

# IMPORTANT: ensure correct column order
people_df = people_df[[
    "playerID","ID","birthYear","birthMonth","birthDay","birthCity","birthCountry","birthState",
    "deathYear","deathMonth","deathDay","deathCountry","deathState","deathCity",
    "nameFirst","nameLast","nameGiven","weight","height","bats","throws",
    "debut","bbrefID","finalGame","retroID"
]]

teams_df = teams_df[[
    "yearID","lgID","teamID","franchID","divID","Rank","G","Ghome","W","L","DivWin","WCWin",
    "LgWin","WSWin","R","AB","H","2B","3B","HR","BB","SO","SB","CS","HBP","SF","RA","ER","ERA",
    "CG","SHO","SV","IPouts","HA","HRA","BBA","SOA","E","DP","FP","name","park","attendance",
    "BPF","PPF","teamIDBR","teamIDlahman45","teamIDretro"
]]

batting_df = batting_df[[
    "playerID","yearID","stint","teamID","lgID","G","AB","R","H","2B","3B","HR","RBI","SB",
    "CS","BB","SO","IBB","HBP","SH","SF","GIDP"
]]

# Insert into database
people_df.to_sql("people", conn, if_exists="append", index=False)
teams_df.to_sql("teams", conn, if_exists="append", index=False)
batting_df.to_sql("batting", conn, if_exists="append", index=False)

# -------------------------
# Finalize
# -------------------------
conn.commit()
conn.close()

print("✅ Baseball.db created successfully!")