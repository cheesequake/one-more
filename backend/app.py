from fastapi import FastAPI, Query, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
from pydantic import BaseModel
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_aws import ChatBedrock
from langchain.chains.sql_database.query import create_sql_query_chain

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

FRONTEND_URL = os.getenv("FRONTEND_URL")

app = FastAPI()

origins = [
    FRONTEND_URL,
]

app.add_middleware (
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

llm = ChatBedrock (
    model="amazon.titan-text-express-v1",
    model_kwargs={"temperature": 0},
)

def connect_to_rds ():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )

        if connection.is_connected():
            print("Connected to AWS RDS MySQL")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None


# Get list of teams based on league ID (required parameter)
@app.get("/teams")
async def get_teams(leagueId: int = Query(..., description="ID of the league to filter teams")):
    connection = connect_to_rds()
    if not connection:
        raise HTTPException(status_code=500, detail="Unable to connect to the database")

    cursor = connection.cursor(dictionary=True)

    # Query to fetch teams by league ID
    query = """
        SELECT *
        FROM teams t
        JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
        WHERE tlm.league_id = %s
    """
    cursor.execute(query, (leagueId,))
    teams = cursor.fetchall()

    cursor.close()
    connection.close()

    if not teams:
        raise HTTPException(status_code=404, detail="No teams found for the given league ID")

    for team in teams:
        team['team_id'] = str(team['team_id'])
    return teams

# Get all leagues information
@app.get("/leagues")
async def get_league():
    connection = connect_to_rds()
    if not connection:
        raise HTTPException(status_code=500, detail="Unable to connect to the database")

    cursor = connection.cursor(dictionary=True)

    # Query to fetch all leagues
    query = "SELECT * FROM leagues"
    cursor.execute(query)
    leagues = cursor.fetchall()

    cursor.close()
    connection.close()

    if not leagues:
        raise HTTPException(status_code=404, detail="Leagues not found")

    # Convert league_id (bigint) to string to avoid precision loss in JavaScript
    for league in leagues:
        league['league_id'] = str(league['league_id'])

    return leagues

# Get league information by league ID
@app.get("/leagues/{leagueId}")
async def get_league(leagueId: int = Path(..., description="ID of the league to retrieve information")):
    connection = connect_to_rds()
    if not connection:
        raise HTTPException(status_code=500, detail="Unable to connect to the database")

    cursor = connection.cursor(dictionary=True)

    # Query to fetch league information by league ID
    query = "SELECT * FROM leagues WHERE league_id = %s"
    cursor.execute(query, (leagueId,))
    league = cursor.fetchone()

    cursor.close()
    connection.close()

    if not league:
        raise HTTPException(status_code=404, detail="League not found")

    league['league_id'] = str(league['league_id'])
    return league

# Allowed values for each parameter
allowedLevels = ["professional", "semi-professional", "game-changer"]
allowedIgls = ["yes", "no", "any"]
allowedRoles = ["duelist", "initiator", "controller", "sentinel"]
allowedSortBy = ["name", "attacking-kda", "defending-kda", "kills", "deaths", "assists", "year", "team"]
allowedSortOrder = ["ASC", "DESC"]

@app.get("/players")
def get_players(
    level: str = Query(..., description="The level of the player (e.g., professional)"),
    igl: str = Query(..., description="The IGL status of the player"),
    role: str = Query(..., description="The role of the player (e.g., duelist, initiator)"),
    sortBy: str = Query(..., description="Field to sort by (e.g., name, kda)"),
    sortOrder: str = Query(..., description="Sort order, either ASC or DESC")
):
    # Validation for each parameter
    if level not in allowedLevels:
        raise HTTPException(status_code=400, detail=f"Invalid level. Allowed values: {allowedLevels}")

    if igl not in allowedIgls:
        raise HTTPException(status_code=400, detail=f"Invalid igl. Allowed values: {allowedIgls}")

    if role not in allowedRoles:
        raise HTTPException(status_code=400, detail=f"Invalid role. Allowed values: {allowedRoles}")

    if sortBy not in allowedSortBy:
        raise HTTPException(status_code=400, detail=f"Invalid sortBy. Allowed values: {allowedSortBy}")

    if sortOrder not in allowedSortOrder:
        raise HTTPException(status_code=400, detail=f"Invalid sortOrder. Allowed values: {allowedSortOrder}")

    return None

@app.post("/generate_response")
async def generate_response(request: QueryRequest):

    db = SQLDatabase.from_uri (f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")