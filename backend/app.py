from fastapi import FastAPI, Query, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
from pydantic import BaseModel
import query_engine

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

FRONTEND_URL = os.getenv("FRONTEND_URL")

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

app.add_middleware (
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
allowedLevels = ["Professional", "Semi-Professional", "Game-Changer"]
allowedIgls = ["yes", "no", "any"]
allowedRoles = ["duelist", "initiator", "controller", "sentinel"]
allowedSortBy = ["name", "attacking-kda", "defending-kda", "kills", "deaths", "assists", "year", "team"]
allowedSortOrder = ["ASC", "DESC"]

@app.get("/players")
def get_players(
    level: str = Query(..., description="The level of the player (e.g., Professional)"),
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

    sortSQLmap = {"name": "p.in_game_name", "attacking-kda":"p.attack_KDA", "defending-kda":"p.defense_KDA", "kills":"p.total_kills", "deaths":"p.total_deaths", "assists":"p.total_assists", "year":"p.years_active", "team":"t.team_name"}
    iglSQLmap = {"yes": "TRUE", "no": "FALSE"}
    levelSQLmap = {"Professional": "VCT International", "Semi-Professional": "VCT Challengers", "Game-Changer": "VCT Game Changers"}

    sql_query = ""

    if (igl == "any"):
        sql_query = f"""SELECT
        p.player_id, p.real_name, p.in_game_name,
        p.status, p.aces, p.four_kills, p.operator_kills,
        p.average_combat_score, p.pistol_kills,
        p.total_matches_played, p.in_game_leader, p.headshot_percentage,
        p.average_attack_first_kills, p.average_attack_first_deaths,
        p.average_defense_first_kills, p.average_defense_first_deaths,
        p.attack_KDA, p.defense_KDA, p.total_kills, p.total_deaths,
        p.total_assists, p.years_active, t.team_acronym,
        t.team_name,
        t.team_acronym,
        a.agent_name,
        pas.matches_played_as_agent,
        pas.KDA_as_agent,
        (SELECT ag.role FROM agents ag WHERE ag.agent_id = pas.agent_id) AS role
        FROM
        players p
        JOIN teams t ON p.home_team_id = t.team_id
        JOIN (
            SELECT
            player_id,
            agent_id,
            matches_played_as_agent,
            KDA_as_agent,
            ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY matches_played_as_agent DESC) AS row_num
            FROM
            player_agent_wise_stats
        ) pas ON p.player_id = pas.player_id
        JOIN agents a ON pas.agent_id = a.agent_id
        WHERE
        p.level = '{levelSQLmap[level]}'
        AND pas.row_num = 1
        AND p.average_combat_score > 0.0
        AND (SELECT ag.role FROM agents ag WHERE ag.agent_id = pas.agent_id) = '{role}'
        ORDER BY
        {sortSQLmap[sortBy]} {sortOrder};"""
    else:
        sql_query = f"""SELECT
        p.player_id, p.real_name, p.in_game_name,
        p.status, p.aces, p.four_kills, p.operator_kills,
        p.average_combat_score, p.pistol_kills,
        p.total_matches_played, p.in_game_leader, p.headshot_percentage,
        p.average_attack_first_kills, p.average_attack_first_deaths,
        p.average_defense_first_kills, p.average_defense_first_deaths,
        p.attack_KDA, p.defense_KDA, p.total_kills, p.total_deaths,
        p.total_assists, p.years_active, t.team_acronym,
        t.team_name,
        t.team_acronym,
        a.agent_name,
        pas.matches_played_as_agent,
        pas.KDA_as_agent,
        (SELECT ag.role FROM agents ag WHERE ag.agent_id = pas.agent_id) AS role
        FROM
        players p
        JOIN teams t ON p.home_team_id = t.team_id
        JOIN (
            SELECT
            player_id,
            agent_id,
            matches_played_as_agent,
            KDA_as_agent,
            ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY matches_played_as_agent DESC) AS row_num
            FROM
            player_agent_wise_stats
        ) pas ON p.player_id = pas.player_id
        JOIN agents a ON pas.agent_id = a.agent_id
        WHERE
        p.level = '{levelSQLmap[level]}'
        AND p.in_game_leader = {iglSQLmap[igl]}
        AND pas.row_num = 1
        AND p.average_combat_score > 0.0
        AND (SELECT ag.role FROM agents ag WHERE ag.agent_id = pas.agent_id) ='{role}'
        ORDER BY
        {sortSQLmap[sortBy]} {sortOrder};"""

    connection = connect_to_rds()
    if not connection:
        raise HTTPException(status_code=500, detail="Unable to connect to the database")

    cursor = connection.cursor(dictionary=True)

    cursor.execute (sql_query)
    players = cursor.fetchall()

    cursor.close()
    connection.close()

    if not players:
        raise HTTPException(status_code=404, detail="Players not found")

    # Convert player_id (bigint) to string to avoid precision loss in JavaScript
    for player in players:
        player['player_id'] = str(player['player_id'])

    return players

@app.post("/generate_response")
async def generate_response(request: QueryRequest):
    try:
        response = query_engine.run_query_engine (request.query)
        return response

    except Exception as e:
        print (e)
        return "Sorry, I think I'll need a Tech Pause. Anyways, you could try again, or format your question better, like this: agent Jett, player Aspas, region CN, team NRG "