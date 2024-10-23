TABLE_INFO = """
CREATE TABLE agents (
        agent_id VARCHAR(255) NOT NULL,
        agent_name VARCHAR(50),
        `role` VARCHAR(50),
        PRIMARY KEY (agent_id)
)COLLATE utf8mb4_0900_ai_ci ENGINE=InnoDB DEFAULT CHARSET=utf8mb4

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
)COLLATE utf8mb4_0900_ai_ci ENGINE=InnoDB DEFAULT CHARSET=utf8mb4

/*
3 rows from leagues table:
league_id       league_region    league_name
105555608835603034      BR       Challengers BR
105555627532605797      SEA      Challengers SEA ID
105555635175479654      NA       Challengers NA
*/


CREATE TABLE player_agent_wise_stats (
        player_id BIGINT NOT NULL,
        agent_id VARCHAR(255) NOT NULL,
        matches_played_as_agent SMALLINT,
        `KDA_as_agent` DECIMAL(5, 2),
        PRIMARY KEY (player_id, agent_id),
        CONSTRAINT player_agent_wise_stats_ibfk_1 FOREIGN KEY(player_id) REFERENCES players (player_id),
        CONSTRAINT player_agent_wise_stats_ibfk_2 FOREIGN KEY(agent_id) REFERENCES agents (agent_id)
)COLLATE utf8mb4_0900_ai_ci ENGINE=InnoDB DEFAULT CHARSET=utf8mb4

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
        `attack_KDA` DECIMAL(5, 2),
        `defense_KDA` DECIMAL(5, 2),
        total_kills SMALLINT,
        total_deaths SMALLINT,
        total_assists SMALLINT,
        years_active VARCHAR(30),
        PRIMARY KEY (player_id, home_team_id),
        CONSTRAINT players_ibfk_1 FOREIGN KEY(home_team_id) REFERENCES teams (team_id)
)COLLATE utf8mb4_0900_ai_ci ENGINE=InnoDB DEFAULT CHARSET=utf8mb4

/*
3 rows from players table:
player_id       real_name       in_game_name    status  home_team_id    aces    four_kills      operator_kills  average_combat_score     pistol_kills    total_matches_played    level   in_game_leader  headshot_percentage     average_attack_first_kills      average_attack_first_deaths      average_defense_first_kills     average_defense_first_deaths    gender  attack_KDA      defense_KDA      total_kills     total_deaths    total_assists   years_active
99566407765334300       Gustavo Rossi   Sacy    active  105629840698508229      0       0       0       0.00    0       0       VCT International        0       0.00    0.00    0.00    0.00    0.00    male    0.00    0.00    0       0       0
99566407765334300       Gustavo Henrique Rossi da Silva Sacy    active  105665869861005803      0       15      1       185.12  158      105     VCT Challengers       0       27.23   0.64    0.82    0.80    0.91    male    1.38    1.60    1399    1518    858      2023,2024
99566407765334300       Gustavo  Rossi  Sacy    active  107745125595754895      0       3       0       184.15  0       23      VCT Game Changers        0       24.97   0.39    0.61    1.00    0.61    female/others    1.43    1.85    321     313     188     2022
*/


CREATE TABLE team_league_mapping (
        team_id BIGINT NOT NULL,
        league_id BIGINT NOT NULL,
        CONSTRAINT team_league_mapping_ibfk_1 FOREIGN KEY(team_id) REFERENCES teams (team_id),
        CONSTRAINT team_league_mapping_ibfk_2 FOREIGN KEY(league_id) REFERENCES leagues (league_id)
)COLLATE utf8mb4_0900_ai_ci ENGINE=InnoDB DEFAULT CHARSET=utf8mb4

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
)COLLATE utf8mb4_0900_ai_ci ENGINE=InnoDB DEFAULT CHARSET=utf8mb4

/*
3 rows from teams table:
team_id team_acronym team_name
105623615126176209      TYP       TYPHOON
105623673790617219      AUS       Australs
105623676467282396      WYG     Wygers Argentina
*/
"""

EXAMPLES = [
            {
                "input": "Build a team using only players from VCT International. Assign roles to each player and explain why this composition would be effective in a competitive match.",
                "query": """
```sql((
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    WHERE p.level = 'VCT International'
    AND a.role = 'duelist'
    GROUP BY p.player_id
    HAVING MAX(pas.matches_played_as_agent) = (
        SELECT MAX(inner_pas.matches_played_as_agent)
        FROM player_agent_wise_stats inner_pas
        WHERE inner_pas.player_id = p.player_id
    )
    ORDER BY RAND()
    LIMIT 1
)
UNION
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    WHERE p.level = 'VCT International'
    AND a.role = 'controller'
    GROUP BY p.player_id
    HAVING MAX(pas.matches_played_as_agent) = (
        SELECT MAX(inner_pas.matches_played_as_agent)
        FROM player_agent_wise_stats inner_pas
        WHERE inner_pas.player_id = p.player_id
    )
    ORDER BY RAND()
    LIMIT 1
)
UNION
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    WHERE p.level = 'VCT International'
    AND a.role = 'sentinel'
    GROUP BY p.player_id
    HAVING MAX(pas.matches_played_as_agent) = (
        SELECT MAX(inner_pas.matches_played_as_agent)
        FROM player_agent_wise_stats inner_pas
        WHERE inner_pas.player_id = p.player_id
    )
    ORDER BY RAND()
    LIMIT 1
)
UNION
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    WHERE p.level = 'VCT International'
    AND a.role = 'initiator'
    GROUP BY p.player_id
    HAVING MAX(pas.matches_played_as_agent) = (
        SELECT MAX(inner_pas.matches_played_as_agent)
        FROM player_agent_wise_stats inner_pas
        WHERE inner_pas.player_id = p.player_id
    )
    ORDER BY RAND()
    LIMIT 1
)
UNION
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    WHERE p.level = 'VCT International'
    AND p.in_game_leader = 1
    GROUP BY p.player_id
    ORDER BY RAND()
    LIMIT 1
);)```
"""
            },
            {
                "input": "Build a team that includes at least two semi-professional players, such as from VCT Challengers or VCT Game Changers. Define roles and discuss details of how these players were chosen.",
                "query" : """
```sql((
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    WHERE p.level = 'VCT International'
    AND a.role = 'duelist'
    GROUP BY p.player_id
    HAVING MAX(pas.matches_played_as_agent) = (
        SELECT MAX(inner_pas.matches_played_as_agent)
        FROM player_agent_wise_stats inner_pas
        WHERE inner_pas.player_id = p.player_id
    )
    ORDER BY RAND()
    LIMIT 1
)
UNION
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    WHERE p.level = 'VCT International'
    AND a.role = 'controller'
    GROUP BY p.player_id
    HAVING MAX(pas.matches_played_as_agent) = (
        SELECT MAX(inner_pas.matches_played_as_agent)
        FROM player_agent_wise_stats inner_pas
        WHERE inner_pas.player_id = p.player_id
    )
    ORDER BY RAND()
    LIMIT 1
)
UNION
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    WHERE p.level = 'VCT International'
    AND a.role = 'sentinel'
    GROUP BY p.player_id
    HAVING MAX(pas.matches_played_as_agent) = (
        SELECT MAX(inner_pas.matches_played_as_agent)
        FROM player_agent_wise_stats inner_pas
        WHERE inner_pas.player_id = p.player_id
    )
    ORDER BY RAND()
    LIMIT 1
)
UNION
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    WHERE p.level = 'VCT International'
    AND a.role = 'initiator'
    GROUP BY p.player_id
    HAVING MAX(pas.matches_played_as_agent) = (
        SELECT MAX(inner_pas.matches_played_as_agent)
        FROM player_agent_wise_stats inner_pas
        WHERE inner_pas.player_id = p.player_id
    )
    ORDER BY RAND()
    LIMIT 1
)
UNION
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    WHERE p.level = 'VCT International'
    AND p.in_game_leader = 1
    GROUP BY p.player_id
    ORDER BY RAND()
    LIMIT 1
);)```"""
            },
            {
                "input": "Which teams has Demon1 played for?",
                "query": """
```sql(
SELECT t.team_name, t.team_acronym
FROM players p
JOIN teams t ON p.home_team_id = t.team_id
WHERE p.in_game_name ='Demon1';)```
"""
            },
            {
                "input": "Analyse Demon1's performance on Astra",
                "query": """
```sql(
SELECT p.*, a.agent_name, pas.matches_played_as_agent, pas.KDA_as_agent
FROM players p
JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
JOIN agents a ON pas.agent_id = a.agent_id
WHERE p.in_game_name ='Demon1'
AND a.agent_name = 'Astra'
GROUP BY p.player_id;
)```
"""
            },
            {
                "input": "Analyse EG Demon1's performance on Astra",
                "query": """
```sql(
SELECT p.*, a.agent_name, a.role, pas.matches_played_as_agent, pas.KDA_as_agent
FROM players p
JOIN teams t ON p.home_team_id = t.team_id
JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
JOIN agents a ON pas.agent_id = a.agent_id
WHERE p.in_game_name ='Demon1'
AND t.team_acronym = 'EG'
AND a.agent_name = 'Astra';
)```
"""
            },
            {
                "input": "Build a team consisting of players from EMEA region. Assign them roles and discuss why this is a good composition.",
                "query": """
```sql(
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    WHERE l.league_region = 'EMEA'
    AND a.role = 'duelist'
    GROUP BY p.player_id
    HAVING MAX(pas.matches_played_as_agent) = (
        SELECT MAX(inner_pas.matches_played_as_agent)
        FROM player_agent_wise_stats inner_pas
        WHERE inner_pas.player_id = p.player_id
    )
    ORDER BY RAND()
    LIMIT 1
)
UNION
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    WHERE l.league_region = 'EMEA'
    AND a.role = 'controller'
    GROUP BY p.player_id
    HAVING MAX(pas.matches_played_as_agent) = (
        SELECT MAX(inner_pas.matches_played_as_agent)
        FROM player_agent_wise_stats inner_pas
        WHERE inner_pas.player_id = p.player_id
    )
    ORDER BY RAND()
    LIMIT 1
)
UNION
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    WHERE l.league_region = 'EMEA'
    AND a.role = 'sentinel'
    GROUP BY p.player_id
    HAVING MAX(pas.matches_played_as_agent) = (
        SELECT MAX(inner_pas.matches_played_as_agent)
        FROM player_agent_wise_stats inner_pas
        WHERE inner_pas.player_id = p.player_id
    )
    ORDER BY RAND()
    LIMIT 1
)
UNION
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    WHERE l.league_region = 'EMEA'
    AND a.role = 'initiator'
    GROUP BY p.player_id
    HAVING MAX(pas.matches_played_as_agent) = (
        SELECT MAX(inner_pas.matches_played_as_agent)
        FROM player_agent_wise_stats inner_pas
        WHERE inner_pas.player_id = p.player_id
    )
    ORDER BY RAND()
    LIMIT 1
)
UNION
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    WHERE l.league_region = 'EMEA'
    AND p.in_game_leader = 1
    GROUP BY p.player_id
    ORDER BY RAND()
    LIMIT 1
);)
"""
            },
            {
                "input": "Build a team using only players from VCT Challengers. Assign roles to each player and explain why this composition would be effective in a competitive match.",
                "query": """
```sql(
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    WHERE p.level = 'VCT Challengers'
    AND a.role = 'duelist'
    GROUP BY p.player_id
    HAVING MAX(pas.matches_played_as_agent) = (
        SELECT MAX(inner_pas.matches_played_as_agent)
        FROM player_agent_wise_stats inner_pas
        WHERE inner_pas.player_id = p.player_id
    )
    ORDER BY RAND()
    LIMIT 1
)
UNION
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    WHERE p.level = 'VCT Challengers'
    AND a.role = 'controller'
    GROUP BY p.player_id
    HAVING MAX(pas.matches_played_as_agent) = (
        SELECT MAX(inner_pas.matches_played_as_agent)
        FROM player_agent_wise_stats inner_pas
        WHERE inner_pas.player_id = p.player_id
    )
    ORDER BY RAND()
    LIMIT 1
)
UNION
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    WHERE p.level = 'VCT Challengers'
    AND a.role = 'sentinel'
    GROUP BY p.player_id
    HAVING MAX(pas.matches_played_as_agent) = (
        SELECT MAX(inner_pas.matches_played_as_agent)
        FROM player_agent_wise_stats inner_pas
        WHERE inner_pas.player_id = p.player_id
    )
    ORDER BY RAND()
    LIMIT 1
)
UNION
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    WHERE p.level = 'VCT Challengers'
    AND a.role = 'initiator'
    GROUP BY p.player_id
    HAVING MAX(pas.matches_played_as_agent) = (
        SELECT MAX(inner_pas.matches_played_as_agent)
        FROM player_agent_wise_stats inner_pas
        WHERE inner_pas.player_id = p.player_id
    )
    ORDER BY RAND()
    LIMIT 1
)
UNION
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    WHERE p.level = 'VCT Challengers'
    AND p.in_game_leader = 1
    GROUP BY p.player_id
    ORDER BY RAND()
    LIMIT 1
);)```
"""
            },
            {
                "input": "Build a team using only players from VCT Game Changers. Assign roles to each player and explain why this composition would be effective in a competitive match.",
                "query": """
```sql(
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    WHERE p.level = 'VCT Game Changers'
    AND a.role = 'duelist'
    GROUP BY p.player_id
    HAVING MAX(pas.matches_played_as_agent) = (
        SELECT MAX(inner_pas.matches_played_as_agent)
        FROM player_agent_wise_stats inner_pas
        WHERE inner_pas.player_id = p.player_id
    )
    ORDER BY RAND()
    LIMIT 1
)
UNION
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    WHERE p.level = 'VCT Game Changers'
    AND a.role = 'controller'
    GROUP BY p.player_id
    HAVING MAX(pas.matches_played_as_agent) = (
        SELECT MAX(inner_pas.matches_played_as_agent)
        FROM player_agent_wise_stats inner_pas
        WHERE inner_pas.player_id = p.player_id
    )
    ORDER BY RAND()
    LIMIT 1
)
UNION
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    WHERE p.level = 'VCT Game Changers'
    AND a.role = 'sentinel'
    GROUP BY p.player_id
    HAVING MAX(pas.matches_played_as_agent) = (
        SELECT MAX(inner_pas.matches_played_as_agent)
        FROM player_agent_wise_stats inner_pas
        WHERE inner_pas.player_id = p.player_id
    )
    ORDER BY RAND()
    LIMIT 1
)
UNION
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    WHERE p.level = 'VCT Game Changers'
    AND a.role = 'initiator'
    GROUP BY p.player_id
    HAVING MAX(pas.matches_played_as_agent) = (
        SELECT MAX(inner_pas.matches_played_as_agent)
        FROM player_agent_wise_stats inner_pas
        WHERE inner_pas.player_id = p.player_id
    )
    ORDER BY RAND()
    LIMIT 1
)
UNION
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    WHERE p.level = 'VCT Game Changers'
    AND p.in_game_leader = 1
    GROUP BY p.player_id
    ORDER BY RAND()
    LIMIT 1
);)```
"""
            },
            {
                "input": "Build a team that includes at least two players from an underrepresented group, such as the Game Changers program. Define roles and discuss the advantages of this inclusive team structure.",
                "query": """
```sql(
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    WHERE p.level = 'VCT Game Changers'
    AND a.role = 'duelist'
    GROUP BY p.player_id
    HAVING MAX(pas.matches_played_as_agent) = (
        SELECT MAX(inner_pas.matches_played_as_agent)
        FROM player_agent_wise_stats inner_pas
        WHERE inner_pas.player_id = p.player_id
    )
    ORDER BY RAND()
    LIMIT 1
)
UNION
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    WHERE p.level = 'VCT Game Changers'
    AND a.role = 'controller'
    GROUP BY p.player_id
    HAVING MAX(pas.matches_played_as_agent) = (
        SELECT MAX(inner_pas.matches_played_as_agent)
        FROM player_agent_wise_stats inner_pas
        WHERE inner_pas.player_id = p.player_id
    )
    ORDER BY RAND()
    LIMIT 1
)
UNION
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    AND a.role = 'sentinel'
    GROUP BY p.player_id
    HAVING MAX(pas.matches_played_as_agent) = (
        SELECT MAX(inner_pas.matches_played_as_agent)
        FROM player_agent_wise_stats inner_pas
        WHERE inner_pas.player_id = p.player_id
    )
    ORDER BY RAND()
    LIMIT 1
)
UNION
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    AND a.role = 'initiator'
    GROUP BY p.player_id
    HAVING MAX(pas.matches_played_as_agent) = (
        SELECT MAX(inner_pas.matches_played_as_agent)
        FROM player_agent_wise_stats inner_pas
        WHERE inner_pas.player_id = p.player_id
    )
    ORDER BY RAND()
    LIMIT 1
)
UNION
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    AND p.in_game_leader = 1
    GROUP BY p.player_id
    ORDER BY RAND()
    LIMIT 1
);
)```
"""
            },
            {
                "input": "Build a team with players from at least three different regions. Assign each player a role and explain the benefits of this diverse composition.",
                "query": """
```sql(
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    WHERE l.league_region = 'NA'
    AND a.role = 'duelist'
    GROUP BY p.player_id
    HAVING MAX(pas.matches_played_as_agent) = (
        SELECT MAX(inner_pas.matches_played_as_agent)
        FROM player_agent_wise_stats inner_pas
        WHERE inner_pas.player_id = p.player_id
    )
    ORDER BY RAND()
    LIMIT 1
)
UNION
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    WHERE l.league_region = 'BR'
    AND a.role = 'controller'
    GROUP BY p.player_id
    HAVING MAX(pas.matches_played_as_agent) = (
        SELECT MAX(inner_pas.matches_played_as_agent)
        FROM player_agent_wise_stats inner_pas
        WHERE inner_pas.player_id = p.player_id
    )
    ORDER BY RAND()
    LIMIT 1
)
UNION
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    WHERE l.league_region = 'EMEA'
    AND a.role = 'sentinel'
    GROUP BY p.player_id
    HAVING MAX(pas.matches_played_as_agent) = (
        SELECT MAX(inner_pas.matches_played_as_agent)
        FROM player_agent_wise_stats inner_pas
        WHERE inner_pas.player_id = p.player_id
    )
    ORDER BY RAND()
    LIMIT 1
)
UNION
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    AND a.role = 'initiator'
    GROUP BY p.player_id
    HAVING MAX(pas.matches_played_as_agent) = (
        SELECT MAX(inner_pas.matches_played_as_agent)
        FROM player_agent_wise_stats inner_pas
        WHERE inner_pas.player_id = p.player_id
    )
    ORDER BY RAND()
    LIMIT 1
)
UNION
(
    SELECT p.*, a.agent_name, a.role, MAX(pas.matches_played_as_agent) AS most_played_matches, l.league_region
    FROM players p
    JOIN player_agent_wise_stats pas ON p.player_id = pas.player_id
    JOIN agents a ON pas.agent_id = a.agent_id
    JOIN teams t ON p.home_team_id = t.team_id
    JOIN team_league_mapping tlm ON t.team_id = tlm.team_id
    JOIN leagues l ON tlm.league_id = l.league_id
    AND p.in_game_leader = 1
    GROUP BY p.player_id
    ORDER BY RAND()
    LIMIT 1
);
)```
"""
            },
            {
                "input": "",
                "query": """
```sql(

)```
"""
            }
        ]


FEW_SHOT_PREFIX = "You are a MySQL expert. Given an input question, create a syntactically correct mysql query to run. Unless otherwise specificed, do not return more than {top_k} rows.\n\n VALORANT is a 5 player team based first person shooter game, where players pick and use agents, and play matches in teams. Teams participate in leagues, and leagues have regions. Each agent has a role, and every team has players who use one of each roles. There are 4 roles in total, and the fifth player is always an IGL (in-game-leader). Here is the relevant table info: {table_info}\n\n Below are a number of examples of questions and their corresponding SQL queries."

RECHECK_QUERY_PROMPT = "\nGiven the database table information: {table_info}\n\nQuery:\n{query}\nDouble check the mysql query above for common mistakes, including:\n- Using NOT IN with NULL values\n- Using BETWEEN for exclusive ranges\n- Data type mismatch in predicates\n- Properly quoting identifiers\n- Using the correct number of arguments for functions\n- Casting to the correct data type\n- Generating a write/modify query which changes data\n- Using the proper columns for joins\n\nIf there are any of the above mistakes, rewrite the query. If there are no mistakes, just reproduce the original query.\n\nOutput the final SQL query ONLY. Join the query here:\n\nSQL Query: "

DATA_ANALYST_PROMPT = "You are an expert Data Analyst. Here is some information about the data you will be working with:\n\nVALORANT is a team-based first person shooter video game, where players form a team of 5, and plant/defuse the spike and kill their opponents to win. Each player picks an agent, and each agent has a role associated to it. There are 4 kinds of roles:\n- Duelist, the one who takes fights, entries into the spike site, takes the most duels. So, this role has to be high in first kills, compared to first deaths.\n- Initiator, the one who uses utilities to make it easier for the duelists and other players to enter into the site. Their assists are a major factor apart from their KDA's.\n- Controller, the one who smokes or walls off regions in the game to provide support to all players and make it harder for the opposite team to enter into a site. This is a defensive role and their defense related stats matter more.\n- Sentinel, this role is majorly defensive, where they have set abilities which they utilise to set up traps, have special weapons and grenades. They thrive around the site.\n\n 5 players of all roles, and one in game leader form a strong team. Each team then goes on to compete in leagues. Leagues are region-wise. A player belongs to a team, which plays in leagues, which has a region.\n\n Based on the given information, analyse the data below, which has been assigned with the question from the user. Take into consideration each and every stat you can see, into how it would be beneficial for that role. Remember, don't use the word data. You must behave as if this data was in your training set, and not provided by the user. So, do not use phrases like 'According to the data' Start analysing data straight-away. Always call players by their in game name, not real name. No need for wrapper text. Also, do not suggest if any data is missing. Only use what you have. Don't give new suggestions. If no data, no need to analyse. Just apologise and say some error occured.\nUser: {query}\nSQL Query:{sql_query}\nData: {data}\nDetailed analysis:"