import json
from sqlExecutor import connect_to_rds, execute_sql

def insert_players_from_json(json_file_path):
    """
    insert_players_from_json

    :param json_file_path: A json file which contains data to be sent to SQL.
    :return: void
    """
    connection = connect_to_rds()

    with open(json_file_path, 'r') as file:
        players_data = json.load(file)

    for player in players_data:
        player_id = int(player['player_id'])
        real_name = player['real_name']
        in_game_name = player['inGameName']
        status = player['status']
        home_team_id = int(player['home_team_id'])

        attack_kills_2022 = int(player['attackKills2022'])
        attack_kills_2023 = int(player['attackKills2023'])
        attack_kills_2024 = int(player['attackKills2024'])

        defense_kills_2022 = int(player['defenseKills2022'])
        defense_kills_2023 = int(player['defenseKills2023'])
        defense_kills_2024 = int(player['defenseKills2024'])

        attack_deaths_2022 = int(player['attackDeaths2022'])
        attack_deaths_2023 = int(player['attackDeaths2023'])
        attack_deaths_2024 = int(player['attackDeaths2024'])

        defense_deaths_2022 = int(player['defenseDeaths2022'])
        defense_deaths_2023 = int(player['defenseDeaths2023'])
        defense_deaths_2024 = int(player['defenseDeaths2024'])

        attack_assists_2022 = int(player['attackAssists2022'])
        attack_assists_2023 = int(player['attackAssists2023'])
        attack_assists_2024 = int(player['attackAssists2024'])

        defense_assists_2022 = int(player['defenseAssists2022'])
        defense_assists_2023 = int(player['defenseAssists2023'])
        defense_assists_2024 = int(player['defenseAssists2024'])

        aces = int(player['aces'])
        four_kills = int(player['fourKills'])
        operator_kills = int(player['operatorKills'])
        average_combat_score = float(player['ACS'])
        pistol_kills = int(player['pistolKills'])
        total_matches_played = int(player['matchesPlayed'])
        level = player['level']
        in_game_leader = bool(player['IGL'])
        headshot_percentage = float(player['headshotPercentage'])
        average_attack_first_kills = float(player['averageAttackFirstKills'])
        average_attack_first_deaths = float(player['averageAttackFirstDeaths'])
        average_defense_first_kills = float(player['averageDefenseFirstKills'])
        average_defense_first_deaths = float(player['averageDefenseFirstDeaths'])
        gender = player['gender']

        # Prepare the SQL insert query
        sql_query = f"""
        INSERT INTO players (
            player_id, real_name, in_game_name, status, home_team_id,
            attack_kills_2022, attack_kills_2023, attack_kills_2024,
            defense_kills_2022, defense_kills_2023, defense_kills_2024,
            attack_deaths_2022, attack_deaths_2023, attack_deaths_2024,
            defense_deaths_2022, defense_deaths_2023, defense_deaths_2024,
            attack_assists_2022, attack_assists_2023, attack_assists_2024,
            defense_assists_2022, defense_assists_2023, defense_assists_2024,
            aces, four_kills, operator_kills, average_combat_score,
            pistol_kills, total_matches_played, level, in_game_leader,
            headshot_percentage, average_attack_first_kills,
            average_attack_first_deaths, average_defense_first_kills,
            average_defense_first_deaths, gender
        ) VALUES (
            {player_id}, "{real_name}", "{in_game_name}", "{status}", {home_team_id},
            {attack_kills_2022}, {attack_kills_2023}, {attack_kills_2024},
            {defense_kills_2022}, {defense_kills_2023}, {defense_kills_2024},
            {attack_deaths_2022}, {attack_deaths_2023}, {attack_deaths_2024},
            {defense_deaths_2022}, {defense_deaths_2023}, {defense_deaths_2024},
            {attack_assists_2022}, {attack_assists_2023}, {attack_assists_2024},
            {defense_assists_2022}, {defense_assists_2023}, {defense_assists_2024},
            {aces}, {four_kills}, {operator_kills}, {average_combat_score},
            {pistol_kills}, {total_matches_played}, "{level}", {in_game_leader},
            {headshot_percentage}, {average_attack_first_kills},
            {average_attack_first_deaths}, {average_defense_first_kills},
            {average_defense_first_deaths}, "{gender}"
        );
        """

        # Execute the SQL query
        execute_sql(connection, sql_query)

        print (in_game_name + " has been added to SQL")

    # Close the database connection
    connection.close()

def insert_player_agent_mapping(json_file_path, start_index=0):
    """
    Inserts player-agent mapping data into the database.

    Parameters:
    - json_file_path: Path to the JSON file containing the player-agent data.
    - start_index: The index in the JSON array from which to start inserting data.
    """
    # Read the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Connect to the database
    connection = connect_to_rds()

    # Loop over the objects in the JSON array, starting from the given index
    for idx, record in enumerate(data[start_index:], start=start_index):
        player_id = int(record['player_id'])  # Convert to BIGINT
        agent_id = record['agent_id']  # Already a string (VARCHAR)
        matches_played = int(record['matches_played'])  # Convert to SMALLINT
        kda_ratio = float(record['KDA'])  # Convert to DECIMAL(5, 2)

        # Prepare the SQL query
        sql_query = f"""
        INSERT INTO player_agent_mapping (player_id, agent_id, matches_played, KDA_ratio)
        VALUES ({player_id}, "{agent_id}", {matches_played}, {kda_ratio})
        """

        # Execute the SQL query
        try:
            execute_sql(connection, sql_query)
        except Exception as e:
            print(f"Error inserting player_id {player_id} and agent_id {agent_id}: {e}")

    # Close the database connection
    connection.close()

def update_player_stats(json_file_path):
    """
    update_player_stats

    Update player stats by inserting some new data

    :param json_file_path: A json file which contains data to be sent to SQL.
    :return: void
    """
    # Read the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Connect to the database
    connection = connect_to_rds()

    # Loop over the objects in the JSON array
    for record in data:
        player_id = int(record['player_id'])  # Convert to BIGINT
        home_team_id = int(record['home_team_id'])  # Convert to BIGINT

        # New values to update
        attack_KDA = float(record.get('attackKDA', 0.0))  # Convert to DECIMAL(5, 2)
        defense_KDA = float(record.get('defenseKDA', 0.0))  # Convert to DECIMAL(5, 2)
        total_kills = int(record.get('totalKills', 0))  # Convert to SMALLINT
        total_deaths = int(record.get('totalDeaths', 0))  # Convert to SMALLINT
        total_assists = int(record.get('totalAssists', 0))  # Convert to SMALLINT
        years_active = record.get('yearsActive', '')  # Convert to VARCHAR(30)

        # Prepare the SQL query
        sql_query = f"""
        UPDATE players
        SET
            attack_KDA = {attack_KDA},
            defense_KDA = {defense_KDA},
            total_kills = {total_kills},
            total_deaths = {total_deaths},
            total_assists = {total_assists},
            years_active = '{years_active}'
        WHERE player_id = {player_id} AND home_team_id = {home_team_id};
        """

        # Execute the SQL query
        try:
            execute_sql(connection, sql_query)
            print (record.get ("inGameName", "") + " has been updated")
        except Exception as e:
            print(f"Error updating player_id {player_id} and home_team_id {home_team_id}: {e}")

    # Close the database connection
    connection.close()

def insert_selected_players(json_file_path, selected_player_ids):
    """
    Inserts only the player-agent mapping data for the specified player_ids into the database.

    Parameters:
    - json_file_path: Path to the JSON file containing the player-agent data.
    - selected_player_ids: A list of player_ids to be inserted into the database.
    """
    # Read the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Connect to the database
    connection = connect_to_rds()

    # Loop over the objects in the JSON array
    for record in data:
        player_id = int(record['player_id'])  # Convert to BIGINT

        # Check if the player_id is in the selected_player_ids list
        if player_id in selected_player_ids:
            agent_id = record['agent_id']  # Already a string (VARCHAR)
            matches_played = int(record['matches_played'])  # Convert to SMALLINT
            kda_ratio = float(record['KDA'])  # Convert to DECIMAL(5, 2)

            # Prepare the SQL query
            sql_query = f"""
            INSERT INTO player_agent_mapping (player_id, agent_id, matches_played, KDA_ratio)
            VALUES ({player_id}, "{agent_id}", {matches_played}, {kda_ratio})
            """

            # Execute the SQL query
            try:
                execute_sql(connection, sql_query)
            except Exception as e:
                print(f"Error inserting player_id {player_id} and agent_id {agent_id}: {e}")

    # Close the database connection
    connection.close()

def update_player_levels_in_db(json_file_path):
    """
    Updates the 'level' field in the players table of the database based on player_id and home_team_id.

    Parameters:
    - json_file_path: Path to the JSON file containing an array of player objects.
    """
    # Read the JSON file
    with open(json_file_path, 'r') as file:
        players_data = json.load(file)

    # Connect to the database
    connection = connect_to_rds()

    # Loop through each player object in the array
    for player in players_data:
        player_id = player.get('player_id')
        home_team_id = player.get('home_team_id')
        level = player.get('level')

        # Prepare the SQL query to update the level
        sql_query = f"""
        UPDATE players
        SET level = '{level}'
        WHERE player_id = {player_id} AND home_team_id = {home_team_id}
        """

        # Execute the SQL query
        try:
            execute_sql(connection, sql_query)
            print (player.get('inGameName') + " changed")
        except Exception as e:
            print(f"Error updating player_id {player_id} and home_team_id {home_team_id}: {e}")

    # Close the database connection
    connection.close()

def update_player_agent_kda(json_file_path, start_index=0):
    """
    Updates the KDA_as_agent column in the player-agent mapping data in the database.

    Parameters:
    - json_file_path: Path to the JSON file containing the player-agent data.
    - start_index: The index in the JSON array from which to start updating data.
    """
    # Read the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Connect to the database
    connection = connect_to_rds()

    # Loop over the objects in the JSON array, starting from the given index
    for idx, record in enumerate(data[start_index:], start=start_index):
        player_id = int(record['player_id'])  # Convert to BIGINT
        agent_id = record['agent_id']  # Already a string (VARCHAR)
        kda_as_agent = float(record['KDA'])  # Convert to DECIMAL(5, 2)

        # Prepare the SQL query for updating only KDA_as_agent
        sql_query = f"""
        UPDATE player_agent_wise_stats
        SET KDA_as_agent = {kda_as_agent}
        WHERE player_id = {player_id} AND agent_id = "{agent_id}"
        """

        # Execute the SQL query
        try:
            execute_sql(connection, sql_query)
        except Exception as e:
            print(f"Error updating KDA for player_id {player_id} and agent_id {agent_id}: {e}")

    # Close the database connection
    connection.close()

