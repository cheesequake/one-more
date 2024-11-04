TABLE_INFO = """
CREATE TABLE agents (
        agent_id VARCHAR(255) NOT NULL,
        agent_name VARCHAR(50),
        role VARCHAR(50),
        PRIMARY KEY (agent_id)
)

/*
3 rows from agents table:
agent_id        agent_name      role
0e38b510-41a8-5780-5e8f-568b2a4f2d6c    Iso     duelist
117ed9e3-49f3-6512-3ccf-0cada7e3823b    Cypher  sentinel
1dbf2edd-4729-0984-3115-daa5eed44993    Clove   controller
*/


CREATE TABLE leagues (
        league_id BIGINT NOT NULL,
        league_region VARCHAR(5) NOT NULL,
        league_name VARCHAR(255) NOT NULL,
        PRIMARY KEY (league_id)
)

/*
3 rows from leagues table:
league_id       league_region       league_name
105555608835603034      BR          Challengers BR
105555627532605797      SEA         Challengers SEA ID
105555635175479654      NA          Challengers NA
*/


CREATE TABLE player_agent_wise_stats (
        player_id BIGINT NOT NULL,
        agent_id VARCHAR(255) NOT NULL,
        matches_played_as_agent SMALLINT,
        KDA_as_agent DECIMAL(5, 2),
        PRIMARY KEY (player_id, agent_id),
        CONSTRAINT player_agent_wise_stats_ibfk_2 FOREIGN KEY(agent_id) REFERENCES agents (agent_id),
        CONSTRAINT player_agent_wise_stats_ibfk_3 FOREIGN KEY(player_id) REFERENCES players (player_id)
)

/*
3 rows from player_agent_wise_stats table:
player_id       agent_id        matches_played_as_agent KDA_as_agent
99566407765334300       0e38b510-41a8-5780-5e8f-568b2a4f2d6c    0       0.00
99566407765334300       117ed9e3-49f3-6512-3ccf-0cada7e3823b    0       0.00
99566407765334300       1dbf2edd-4729-0984-3115-daa5eed44993    0       0.00
*/


CREATE TABLE players (
        player_id BIGINT NOT NULL,
        real_name VARCHAR(255),
        in_game_name VARCHAR(50),
        status VARCHAR(20),
        home_team_id BIGINT NOT NULL,
        aces SMALLINT,
        four_kills SMALLINT,
        operator_kills SMALLINT,
        average_combat_score DECIMAL(6, 2),
        pistol_kills SMALLINT,
        total_matches_played SMALLINT,
        level VARCHAR(50),
        in_game_leader TINYINT(1),
        headshot_percentage DECIMAL(5, 2),
        average_attack_first_kills DECIMAL(4, 2),
        average_attack_first_deaths DECIMAL(4, 2),
        average_defense_first_kills DECIMAL(4, 2),
        average_defense_first_deaths DECIMAL(4, 2),
        gender VARCHAR(20),
        attack_KDA DECIMAL(5, 2),
        defense_KDA DECIMAL(5, 2),
        total_kills SMALLINT,
        total_deaths SMALLINT,
        total_assists SMALLINT,
        years_active VARCHAR(30),
        most_played_agent_id VARCHAR(255),
        region VARCHAR(255),
        PRIMARY KEY (player_id, home_team_id),
        CONSTRAINT players_ibfk_1 FOREIGN KEY(home_team_id) REFERENCES teams (team_id),
        CONSTRAINT players_ibfk_2 FOREIGN KEY(most_played_agent_id) REFERENCES agents (agent_id)
)

/*
3 rows from players table:
player_id       real_name       in_game_name    status  home_team_id    aces    four_kills      operator_kills  average_combat_score     pistol_kills    total_matches_played    level   in_game_leader  headshot_percentage     average_attack_first_kills      average_attack_first_deaths      average_defense_first_kills     average_defense_first_deaths    gender  attack_KDA      defense_KDA      total_kills     total_deaths    total_assists   years_active    most_played_agent_id    region
99566407765334300       Gustavo Henrique Rossi da Silva Sacy    active  105665869861005803      0       15      1       185.12  158      105     VCT International       0       27.23   0.64    0.82    0.80    0.91    male    1.38    1.60    1399    1518    858      2023,2024       dade69b4-4f5a-8528-247b-219e5a1facd6    INTL, NA
99566407765334300       Gustavo  Rossi  Sacy    active  107745125595754895      0       3       0       184.15  0       23      VCT International        0       24.97   0.39    0.61    1.00    0.61    male    1.43    1.85    321     313     188     2022    dade69b4-4f5a-8528-247b-219e5a1facd6     BR, INTL
103537287230111095      Jake  Howlett   Boaster active  105680972836508184      1       17      25      163.69  225     166     VCT Game Changers        1       20.76   0.73    1.08    0.80    0.97    female/others    1.45    1.56    1939    2245    1440    2022,2023,2024   8e253930-4c05-31dd-1b6c-968525494517    INTL
*/


CREATE TABLE team_league_mapping (
        team_id BIGINT NOT NULL,
        league_id BIGINT NOT NULL,
        CONSTRAINT team_league_mapping_ibfk_1 FOREIGN KEY(team_id) REFERENCES teams (team_id),
        CONSTRAINT team_league_mapping_ibfk_2 FOREIGN KEY(league_id) REFERENCES leagues (league_id)
)

/*
3 rows from team_league_mapping table:
team_id league_id
106976751141239255      106976737954740691
109993931544840354      106375817979489820
108065446853266621      106976737954740691
*/


CREATE TABLE teams (
        team_id BIGINT NOT NULL,
        team_acronym VARCHAR(5) NOT NULL,
        team_name VARCHAR(255) NOT NULL,
        PRIMARY KEY (team_id)
)

/*
3 rows from teams table:
team_id     team_acronym    team_name
105623615126176209      TYP     TYPHOON
105623673790617219      AUS     Australs
105623676467282396      WYG     Wygers Argentina
*/
"""

EXAMPLES = [
            {
                "input": "Build a team using only players from VCT International. Assign roles to each player and explain why this composition would be effective in a competitive match.",
                "query": """
(
SELECT 
p.*, 
a.agent_name, 
'duelist' AS assigned_role, 
s.KDA_as_agent, 
s.matches_played_as_agent
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN player_agent_wise_stats s ON p.player_id = s.player_id AND a.agent_id = s.agent_id
WHERE a.role = 'duelist'
AND p.level = 'VCT International'
ORDER BY RAND()
LIMIT 1)

UNION

(SELECT 
p.*, 
a.agent_name, 
'sentinel' AS assigned_role, 
s.KDA_as_agent, 
s.matches_played_as_agent
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN player_agent_wise_stats s ON p.player_id = s.player_id AND a.agent_id = s.agent_id
WHERE a.role = 'sentinel'
AND p.level = 'VCT International'
ORDER BY RAND()
LIMIT 1)

UNION

(SELECT 
p.*, 
a.agent_name, 
'controller' AS assigned_role, 
s.KDA_as_agent, 
s.matches_played_as_agent
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN player_agent_wise_stats s ON p.player_id = s.player_id AND a.agent_id = s.agent_id
WHERE a.role = 'controller'
AND p.level = 'VCT International'
ORDER BY RAND()
LIMIT 1)

UNION

(SELECT 
p.*, 
a.agent_name, 
'initiator' AS assigned_role, 
s.KDA_as_agent, 
s.matches_played_as_agent
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN player_agent_wise_stats s ON p.player_id = s.player_id AND a.agent_id = s.agent_id
WHERE a.role = 'initiator'
AND p.level = 'VCT International'
ORDER BY RAND()
LIMIT 1)

UNION

(SELECT 
p.*, 
a.agent_name, 
'IGL' AS assigned_role, 
s.KDA_as_agent, 
s.matches_played_as_agent
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN player_agent_wise_stats s ON p.player_id = s.player_id AND a.agent_id = s.agent_id
WHERE p.in_game_leader = 1
AND p.level = 'VCT International'
ORDER BY RAND()
LIMIT 1);
"""
            },
            {
                "input": "Build a team that includes at least two semi-professional players, such as from VCT Challengers or VCT Game Changers. Define roles and discuss details of how these players were chosen.",
                "query" : """
(
SELECT 
p.*, 
a.agent_name, 
'duelist' AS assigned_role, 
s.KDA_as_agent, 
s.matches_played_as_agent
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN player_agent_wise_stats s ON p.player_id = s.player_id AND a.agent_id = s.agent_id
WHERE a.role = 'duelist'
AND (p.level = 'VCT Challengers' OR p.level = 'VCT Game Changers')
ORDER BY RAND()
LIMIT 1
)

UNION

(
SELECT 
p.*, 
a.agent_name, 
'sentinel' AS assigned_role, 
s.KDA_as_agent, 
s.matches_played_as_agent
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN player_agent_wise_stats s ON p.player_id = s.player_id AND a.agent_id = s.agent_id
WHERE a.role = 'sentinel'
AND (p.level = 'VCT Challengers' OR p.level = 'VCT Game Changers')
ORDER BY RAND()
LIMIT 1
)

UNION

(
SELECT 
p.*, 
a.agent_name, 
'controller' AS assigned_role, 
s.KDA_as_agent, 
s.matches_played_as_agent
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN player_agent_wise_stats s ON p.player_id = s.player_id AND a.agent_id = s.agent_id
WHERE a.role = 'controller'
ORDER BY RAND()
LIMIT 1
)

UNION

(
SELECT 
p.*, 
a.agent_name, 
'initiator' AS assigned_role, 
s.KDA_as_agent, 
s.matches_played_as_agent
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN player_agent_wise_stats s ON p.player_id = s.player_id AND a.agent_id = s.agent_id
WHERE a.role = 'initiator'
ORDER BY RAND()
LIMIT 1
)

UNION

(
SELECT 
p.*, 
a.agent_name, 
'IGL' AS assigned_role, 
s.KDA_as_agent, 
s.matches_played_as_agent
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN player_agent_wise_stats s ON p.player_id = s.player_id AND a.agent_id = s.agent_id
WHERE p.in_game_leader = 1
ORDER BY RAND()
LIMIT 1
);
"""
            },
            {
                "input": "Which teams has Demon1 played for?",
                "query": """
SELECT t.team_name, t.team_acronym
FROM players p
JOIN teams t ON p.home_team_id = t.team_id
WHERE p.in_game_name ='Demon1';
"""
            },
            {
                "input": "Analyse Demon1's performance on Astra",
                "query": """
SELECT p.*, a.agent_name, pas.matches_played_as_agent, pas.KDA_as_agent
FROM players p
JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
JOIN agents a ON pas.agent_id = a.agent_id
WHERE p.in_game_name ='Demon1'
AND a.agent_name = 'Astra'
GROUP BY p.player_id;
"""
            },
            {
                "input": "Analyse EG Demon1's performance on Astra",
                "query": """
SELECT p.*, a.agent_name, a.role, pas.matches_played_as_agent, pas.KDA_as_agent
FROM players p
JOIN teams t ON p.home_team_id = t.team_id
JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
JOIN agents a ON pas.agent_id = a.agent_id
WHERE p.in_game_name ='Demon1'
AND t.team_acronym = 'EG'
AND a.agent_name = 'Astra';
"""
            },
            {
                "input": "Build a team consisting of players from EMEA region. Assign them roles and discuss why this is a good composition.",
                "query": """
(
SELECT 
    p.*, 
    a.agent_name, 
    'duelist' AS assigned_role, 
    s.KDA_as_agent, 
    s.matches_played_as_agent
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN player_agent_wise_stats s ON p.player_id = s.player_id AND a.agent_id = s.agent_id
WHERE a.role = 'duelist'
AND p.region LIKE '%EMEA%'
ORDER BY RAND()
LIMIT 1
)

UNION

(
SELECT 
    p.*, 
    a.agent_name, 
    'sentinel' AS assigned_role, 
    s.KDA_as_agent, 
    s.matches_played_as_agent
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN player_agent_wise_stats s ON p.player_id = s.player_id AND a.agent_id = s.agent_id
WHERE a.role = 'sentinel'
AND p.region LIKE '%EMEA%'
ORDER BY RAND()
LIMIT 1
)

UNION

(
SELECT 
    p.*, 
    a.agent_name, 
    'controller' AS assigned_role, 
    s.KDA_as_agent, 
    s.matches_played_as_agent
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN player_agent_wise_stats s ON p.player_id = s.player_id AND a.agent_id = s.agent_id
WHERE a.role = 'controller'
AND p.region LIKE '%EMEA%'
ORDER BY RAND()
LIMIT 1
)

UNION

(
SELECT 
    p.*, 
    a.agent_name, 
    'initiator' AS assigned_role, 
    s.KDA_as_agent, 
    s.matches_played_as_agent
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN player_agent_wise_stats s ON p.player_id = s.player_id AND a.agent_id = s.agent_id
WHERE a.role = 'initiator'
AND p.region LIKE '%EMEA%'
ORDER BY RAND()
LIMIT 1
)

UNION

(
SELECT 
    p.*, 
    a.agent_name, 
    'IGL' AS assigned_role, 
    s.KDA_as_agent, 
    s.matches_played_as_agent
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN player_agent_wise_stats s ON p.player_id = s.player_id AND a.agent_id = s.agent_id
WHERE p.in_game_leader = 1
AND p.region LIKE '%EMEA%'
ORDER BY RAND()
LIMIT 1
);
"""
            },
            {
                "input": "Build a team which only has duelists. Tell why this composition will or will not work.",
                "query": """
SELECT 
p.*, 
a.agent_name, 
'duelist' AS assigned_role, 
s.KDA_as_agent, 
s.matches_played_as_agent
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN player_agent_wise_stats s ON p.player_id = s.player_id AND a.agent_id = s.agent_id
WHERE a.role = 'duelist'
ORDER BY RAND()
LIMIT 5;
"""
            },
            {
                "input": "Build a team where the IGL is from NA region, and is a controller. Assign players roles and discuss why this composition will work.",
                "query": """
(
SELECT 
p.*, 
a.agent_name, 
'controller' AS assigned_role, 
s.KDA_as_agent, 
s.matches_played_as_agent
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN player_agent_wise_stats s ON p.player_id = s.player_id AND a.agent_id = s.agent_id
WHERE a.role = 'controller'
AND p.in_game_leader = 1
AND p.region LIKE '%NA%'
ORDER BY RAND()
LIMIT 1
)

UNION

(
SELECT 
p.*, 
a.agent_name, 
'duelist' AS assigned_role, 
s.KDA_as_agent, 
s.matches_played_as_agent
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN player_agent_wise_stats s ON p.player_id = s.player_id AND a.agent_id = s.agent_id
WHERE a.role = 'duelist'
ORDER BY RAND()
LIMIT 1
)

UNION

(
SELECT 
p.*, 
a.agent_name, 
'sentinel' AS assigned_role, 
s.KDA_as_agent, 
s.matches_played_as_agent
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN player_agent_wise_stats s ON p.player_id = s.player_id AND a.agent_id = s.agent_id
WHERE a.role = 'sentinel'
ORDER BY RAND()
LIMIT 1
)

UNION

(
SELECT 
p.*, 
a.agent_name, 
'initiator' AS assigned_role, 
s.KDA_as_agent, 
s.matches_played_as_agent
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN player_agent_wise_stats s ON p.player_id = s.player_id AND a.agent_id = s.agent_id
WHERE a.role = 'initiator'
ORDER BY RAND()
LIMIT 1
)

UNION

(
SELECT 
p.*, 
a.agent_name, 
'controller' AS assigned_role, 
s.KDA_as_agent, 
s.matches_played_as_agent
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN player_agent_wise_stats s ON p.player_id = s.player_id AND a.agent_id = s.agent_id
WHERE a.role = 'controller'
ORDER BY RAND()
LIMIT 1
);
"""
            },
            {
                "input": "Who played for Evil Geniuses in the year 2023? What roles did each player have?",
                "query": """
SELECT
p.*,
a.role AS assigned_role
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN teams t ON p.home_team_id = t.team_id
WHERE t.team_name = 'Evil Geniuses'
AND p.years_active LIKE '%2023%';
"""
            },
            {
                "input": "Compare G2 Esports team to Sentinels team in the year 2023. Discuss each role and which team is likely to win",
                "query": """
SELECT 
p.*,
t.team_name,
a.role AS assigned_role
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN teams t ON p.home_team_id = t.team_id
JOIN player_agent_wise_stats ps ON p.player_id = ps.player_id AND a.agent_id = ps.agent_id
WHERE t.team_name IN ('G2 Esports', 'Sentinels')
AND p.years_active LIKE '%2023%'
ORDER BY t.team_name, a.role;
"""
            },
            {
                "input": "Build a team of players each from a different region. Assign them roles and discuss why this composition is good",
                "query": """
(
SELECT 
    p.*, 
    a.agent_name, 
    'duelist' AS assigned_role, 
    s.KDA_as_agent, 
    s.matches_played_as_agent
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN player_agent_wise_stats s ON p.player_id = s.player_id AND a.agent_id = s.agent_id
WHERE a.role = 'duelist'
AND p.region LIKE '%BR%'
ORDER BY RAND()
LIMIT 1
)

UNION

(
SELECT 
    p.*, 
    a.agent_name, 
    'sentinel' AS assigned_role, 
    s.KDA_as_agent, 
    s.matches_played_as_agent
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN player_agent_wise_stats s ON p.player_id = s.player_id AND a.agent_id = s.agent_id
WHERE a.role = 'sentinel'
AND p.region LIKE '%NA%'
ORDER BY RAND()
LIMIT 1
)

UNION

(
SELECT 
    p.*, 
    a.agent_name, 
    'controller' AS assigned_role, 
    s.KDA_as_agent, 
    s.matches_played_as_agent
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN player_agent_wise_stats s ON p.player_id = s.player_id AND a.agent_id = s.agent_id
WHERE a.role = 'controller'
AND p.region LIKE '%EMEA%'
ORDER BY RAND()
LIMIT 1
)

UNION

(
SELECT 
    p.*, 
    a.agent_name, 
    'initiator' AS assigned_role, 
    s.KDA_as_agent, 
    s.matches_played_as_agent
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN player_agent_wise_stats s ON p.player_id = s.player_id AND a.agent_id = s.agent_id
WHERE a.role = 'initiator'
AND p.region LIKE '%SEA%'
ORDER BY RAND()
LIMIT 1
)

UNION

(
SELECT 
    p.*, 
    a.agent_name, 
    'IGL' AS assigned_role, 
    s.KDA_as_agent, 
    s.matches_played_as_agent
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN player_agent_wise_stats s ON p.player_id = s.player_id AND a.agent_id = s.agent_id
WHERE p.in_game_leader = 1
AND p.region LIKE '%LATAM%'
ORDER BY RAND()
LIMIT 1
);
"""
            },
            {
                "input": "Generate a team of players from VCT International, but do not include anyone from Evil Geniuses. Assign them roles and discuss the composition",
                "query": """
(
SELECT 
p.*, 
a.agent_name, 
'duelist' AS assigned_role,
t.team_name,
s.KDA_as_agent, 
s.matches_played_as_agent
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN player_agent_wise_stats s ON p.player_id = s.player_id AND a.agent_id = s.agent_id
JOIN teams t ON p.home_team_id = t.team_id
WHERE a.role = 'duelist'
AND p.level = 'VCT International'
AND t.team_name <> 'Evil Geniuses'
ORDER BY RAND()
LIMIT 1
)

UNION

(
SELECT 
p.*, 
a.agent_name, 
'sentinel' AS assigned_role, 
t.team_name,
s.KDA_as_agent, 
s.matches_played_as_agent
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN player_agent_wise_stats s ON p.player_id = s.player_id AND a.agent_id = s.agent_id
JOIN teams t ON p.home_team_id = t.team_id
WHERE a.role = 'sentinel'
AND p.level = 'VCT International'
AND t.team_name <> 'Evil Geniuses'
ORDER BY RAND()
LIMIT 1
)

UNION

(
SELECT 
p.*, 
a.agent_name, 
'controller' AS assigned_role, 
t.team_name,
s.KDA_as_agent, 
s.matches_played_as_agent
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN player_agent_wise_stats s ON p.player_id = s.player_id AND a.agent_id = s.agent_id
JOIN teams t ON p.home_team_id = t.team_id
WHERE a.role = 'controller'
AND p.level = 'VCT International'
AND t.team_name <> 'Evil Geniuses'
ORDER BY RAND()
LIMIT 1
)

UNION

(
SELECT 
p.*, 
a.agent_name, 
'initiator' AS assigned_role,
t.team_name, 
s.KDA_as_agent, 
s.matches_played_as_agent
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN player_agent_wise_stats s ON p.player_id = s.player_id AND a.agent_id = s.agent_id
JOIN teams t ON p.home_team_id = t.team_id
WHERE a.role = 'initiator'
AND p.level = 'VCT International'
AND t.team_name <> 'Evil Geniuses'
ORDER BY RAND()
LIMIT 1
)

UNION

(
SELECT 
p.*, 
a.agent_name, 
'IGL' AS assigned_role,
t.team_name,
s.KDA_as_agent, 
s.matches_played_as_agent
FROM players p
JOIN agents a ON p.most_played_agent_id = a.agent_id
JOIN player_agent_wise_stats s ON p.player_id = s.player_id AND a.agent_id = s.agent_id
JOIN teams t ON p.home_team_id = t.team_id
WHERE p.in_game_leader = 1
AND p.level = 'VCT International'
AND t.team_name <> 'Evil Geniuses'
ORDER BY RAND()
LIMIT 1
);
"""
            }
        ]


FEW_SHOT_PREFIX = "You are a MySQL expert. Given an input question, create only one syntactically correct raw mysql query to run. Unless otherwise specificed, do not return more than {top_k} rows.\n\n VALORANT is a 5 player team based first person shooter game, where players pick and use agents, and play matches in teams. Teams participate in leagues, and leagues have regions. Each agent has a role, and every team has players who use one of each roles. There are 4 roles in total, and the fifth player is always an IGL (in-game-leader).\n\n When a player detail is asked, always SELECT p.* along with the player's stats, role, and details on their most_played_agent.\nRemember to use brackets () between two UNION statements. Do not ORDER BY unless asked in user's query. No extra text other the sql query around anything. I only and only want the query, no extra text Not even formatting. Just plain, raw query. Here is the relevant table info: {table_info}\n\n Below are a number of examples of questions and their corresponding SQL queries:"

RECHECK_QUERY_PROMPT = "\nGiven the database table information: {table_info}\n\nQuery:\n{query}\n\nException: {exception}\n\nDouble check the mysql query above for mistakes, including:\n- Using NOT IN with NULL values\n- Using BETWEEN for exclusive ranges\n- Data type mismatch in predicates\n- Properly quoting identifiers\n- Using the correct number of arguments for functions\n- Casting to the correct data type\n- Generating a write/modify query which changes data\n- Using the proper columns for joins\n\nIf there are any of the above mistakes, rewrite the query. If there are no mistakes, just reproduce the original query.\n\nOutput the final SQL query ONLY, do not explain anything Do not format, just plain raw query. Join the query here:\n\nSQL Query: "

DATA_ANALYST_PROMPT = "You are an expert Data Analyst with extensive knowledge of VALORANT stats, player roles, and map strategies. Here’s context for analyzing competitive VALORANT performances:\nVALORANT is a team-based, first-person shooter where 5-player teams plant/defuse the spike and eliminate opponents to win. Players select agents, each associated with one of these roles:\n\n- Duelist: Leads in engagements, often first to enter sites. Prioritizes high first kills, low first deaths. Examples: Iso has a shield for extra armour, Jett has smokes, Raze has grenades and firepower. Neon and Jett have a lot of speed. Phoenix, Yoru, Reyna can flash players. Reyna can heal from enemy kills, whereas Yoru can teleport and make his clones. \n- Initiator: Uses utilities to ease site entry. Excels in assists. Examples: Sova's recon dart, owl drone, Skye's trailblazer, KAY/O's ZERO/POINT knife, Fade's prowler locates enemies. Skye, KAYO, Breach, Fade and Gekko have flashes. Breach has a stun and Fade has a Haunt, which disrupt and stun the enemies. \n- Controller: Limits enemy movement with smokes and walls. Defensive, focusing on stalling enemy entries. Examples: All controllers have smokes. Viper, Harbour and Astra have walls also. Clove can smoke areas even after dying, and also heal. Omen can teleport and flash.\n- Sentinel: Defensive support, gathering intel and anchoring sites to prevent flanking. Examples: Chamber has teleporting abilities and special weapons. Cypher, Killjoy, Deadlock and Chamber have traps to detect flanking enemies. Sage has a wall and healing ability to aid the team defensively. Killjoy has bots to attack enemies. Cypher has a cage, which is similar to a smoke.\n\nEach team needs 5 role players, including an in-game leader, to be successful. Teams compete regionally in leagues, with players belonging to teams that play in these leagues by region.\n\nMaps, each with unique features, affect strategies:\nLotus: 3 sites, attack-favored.\nAscent: 2 sites, defense-heavy.\nBind: 2 sites, defense-heavy. Has teleporters for fast movement and rotation.\nSplit: 2 sites, defense-favored. Both sites have heavens (areas at height) B site is smaller than A site.\nSunset: 2 sites, balanced. Large mid.\nIcebox: 2 sites, attack-favored. Large sites.\nBreeze: 2 sites, attack-favored.\nFracture: 2 sites, balanced.\nAbyss: 2 sites, attack-favored. Botomless map, players can fall off.\nPearl: 2 sites, attack-favored. Long B-long, small A site.\nHaven: 3 sites, slightly attack-favored. A and C sites have prominent longs, whereas B site is compact\n\nWith average performance benchmarks:\n- Combat Score: 191.74\n- Headshot Rate: 26.02%\n- Attack first kills/deaths: 0.89 / 1.13\n- Defense first kills/deaths: 1.06 / 0.96\n\nUsing this as reference, analyze each player’s stats with the following goals:\nEvaluate each player’s role effectiveness based on inferred stats, highlight strengths, and call out areas for improvement, in an extremely detailed manner.\nIdentify suitable maps and strategies for players and teams.\nConfidence in Data: Treat every stat as actual; infer meaning without referring to column names or mentioning 'data.'\nZero Values: Confidently interpret a value of 0 as fact (e.g., 'this player has not played any matches'). Zero values don't mean a lack of data.\nDirectly analyze, referring to players by in-game names only, and analyse properly, using long sentences. Use Markdown formatting.\n\nThis is the history of teams previously formed, for added context. Only use this when follow-up questions are asked: {team}\nThis is the team previous to the question. Only use this data if asked in the User Query. \n\nNever mention anything about SQL Query, or 'data'. You must always strictly behave as if this is your training data and not any SQL data.\n\nUser Query: {query}\nSQL Query: {sql_query}\nData: {data}\n\nDetailed analysis:"