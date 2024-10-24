import json
import unidecode

def combine_names(file_path):
    """
    combine_names

    Combine first name and last name to just one real name

    :param file_path: file path with all player data
    :return: void
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Check if the data is a list
    if isinstance(data, list):
        # Loop over each object and combine names
        for obj in data:
            # Safely extract first and last names, defaulting to empty strings
            first_name = obj.get('first_name', '') or ''
            last_name = obj.get('last_name', '') or ''

            # Decode names
            first_name = unidecode.unidecode(first_name)
            last_name = unidecode.unidecode(last_name)

            # Combine names into 'real_name' and handle empty names
            real_name = f"{first_name} {last_name}".strip()  # strip to handle leading/trailing spaces

            # Assign the combined name to 'real_name'
            obj['real_name'] = real_name

            # Remove the original first_name and last_name keys
            obj.pop('first_name', None)
            obj.pop('last_name', None)

    # Write the updated data back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"Updated names and saved to {file_path}")

def calculate_headshot_percentage(file_path):
    """
    calculate_headshot_percentage

    Calculate headshot percentages of players

    :param file_path: file path with all player data
    :return: void
    """
    # Open the file and load the JSON data
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Check if the data is a list
    if isinstance(data, list):
        # Loop over each object to calculate headshot percentage
        for obj in data:
            head_shots = obj.get('headShots', 0)
            total_shots = obj.get('totalShots', 0)

            # Calculate headshot percentage
            if total_shots > 0:
                headshot_percentage = (head_shots * 100) / total_shots
            else:
                headshot_percentage = 0  # Avoid division by zero

            # Assign the headshot percentage to 'headshotPercentage'
            obj['headshotPercentage'] = headshot_percentage

            # Remove the original headShots and totalShots keys
            obj.pop('headShots', None)
            obj.pop('totalShots', None)

    # Write the updated data back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"Updated headshot percentages and saved to {file_path}")

def calculate_average_stats(file_path):
    """
    calculate_average_stats

    Calculate average of the stats

    :param file_path: file path with all player data
    :return: void
    """
    # Open the JSON file and load the data
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Check if the data is a list
    if isinstance(data, list):
        for obj in data:
            matches_played = obj.get('matchesPlayed', 1)  # Avoid division by zero

            if (matches_played == 0):
                matches_played = 1

            # Calculate averages
            average_attack_first_kills = obj.get('attackFirstKills', 0) / matches_played
            average_attack_first_deaths = obj.get('attackFirstDeaths', 0) / matches_played
            average_defense_first_kills = obj.get('defenseFirstKills', 0) / matches_played
            average_defense_first_deaths = obj.get('defenseFirstDeaths', 0) / matches_played

            # Replace original keys with average keys
            obj['averageAttackFirstKills'] = average_attack_first_kills
            obj['averageAttackFirstDeaths'] = average_attack_first_deaths
            obj['averageDefenseFirstKills'] = average_defense_first_kills
            obj['averageDefenseFirstDeaths'] = average_defense_first_deaths

            # Remove the original keys
            obj.pop('attackFirstKills', None)
            obj.pop('attackFirstDeaths', None)
            obj.pop('defenseFirstKills', None)
            obj.pop('defenseFirstDeaths', None)

    # Write the updated data back to the same JSON file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"Updated averages and saved to {file_path}")

def adjust_acs(file_path):
    """
    adjust_acs

    Calculate average of the ACS

    :param file_path: file path with all player data
    :return: void
    """
    # Open the JSON file and load the data
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Check if the data is a list
    if isinstance(data, list):
        for obj in data:
            matches_played = obj.get('matchesPlayed', 1)  # Avoid division by zero
            acs = obj.get('ACS', 0)

            if matches_played == 0:
                matches_played = 1

            # Calculate new ACS value
            new_acs = acs / matches_played

            # Replace the ACS value with the new value
            obj['ACS'] = new_acs

    # Write the updated data back to the same JSON file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"Updated ACS values and saved to {file_path}")

def calculate_correct_kda(file_path):
    """
    calculate_correct_kda

    Calculate average of the totalled KDA

    :param file_path: file path with all player data
    :return: void
    """
    # Open the JSON file and load the data
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Check if the data is a list
    if isinstance(data, list):
        for player in data:
            # List of agents to process
            agents = [
                "Jett", "Reyna", "Raze", "Yoru", "Phoenix", "Neon",
                "Breach", "Skye", "Sova", "Kayo", "Killjoy", "Cypher",
                "Sage", "Chamber", "Omen", "Brimstone", "Astra",
                "Viper", "Fade", "Harbor", "Gekko", "Deadlock", "Iso", "Clove", "Vyse"
            ]

            for agent in agents:
                matches_key = f"matchesAs{agent}"
                kda_key = f"{agent}KDA"

                matches_played = player.get(matches_key, 0)
                if matches_played > 0:
                    # Calculate the correct KDA
                    correct_kda = player.get(kda_key, 0) / matches_played
                    # Replace the existing KDA with the new calculated KDA
                    player[kda_key] = correct_kda
                else:
                    # If no matches played, set KDA to 0
                    player[kda_key] = 0

    # Write the updated data back to the same JSON file
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"Updated KDA values and saved to {file_path}")


def aggregate_player_stats(input_file_path, output_file_path):
    """
    aggregate_player_stats

    Count match data and agent wise stats

    :param agent_file_path: contains agent data
    :param player_file_path: contains all player data
    :param output_file_path: contains agent wise player data
    :return: void
    """
    # List of agents
    agents = [
        "Jett", "Reyna", "Raze", "Yoru", "Phoenix", "Neon",
        "Breach", "Skye", "Sova", "Kayo", "Killjoy", "Cypher",
        "Sage", "Chamber", "Omen", "Brimstone", "Astra",
        "Viper", "Fade", "Harbor", "Gekko", "Deadlock", "Iso", "Clove", "Vyse"
    ]

    # Load data from the input JSON file
    with open(input_file_path, 'r') as infile:
        players_data = json.load(infile)

    # Dictionary to hold aggregated stats for each player_id
    aggregated_data = {}

    # Iterate over each player object in the data
    for player in players_data:
        player_id = player['player_id']

        # Initialize player stats if this player_id hasn't been encountered
        if player_id not in aggregated_data:
            aggregated_data[player_id] = {'player_id': player_id}
            for agent in agents:
                aggregated_data[player_id]['matchesAs' + agent] = 0
                aggregated_data[player_id]['{}KDA'.format(agent)] = 0.0

        # Aggregate stats for each agent
        for agent in agents:
            matches_key = 'matchesAs' + agent
            kda_key = '{}KDA'.format(agent)

            # Add the matches and KDA values from the player entry
            aggregated_data[player_id][matches_key] += player[matches_key]
            aggregated_data[player_id][kda_key] += player[kda_key]

    # Prepare final aggregated results
    final_results = []
    for player_id, stats in aggregated_data.items():
        for agent in agents:
            matches_key = 'matchesAs' + agent
            kda_key = '{}KDA'.format(agent)

            # Calculate the average KDA if matches are greater than 0
            if stats[matches_key] > 0:
                stats[kda_key] /= stats[matches_key]
            else:
                stats[kda_key] = 0.0  # Set KDA to 0 if no matches

        # Append the formatted player data to final results
        player_stats = {'player_id': stats['player_id']}
        for agent in agents:
            player_stats['matchesAs' + agent] = stats['matchesAs' + agent]
            player_stats[agent + 'KDA'] = stats[agent + 'KDA']

        final_results.append(player_stats)

    # Write the aggregated data to the output JSON file
    with open(output_file_path, 'w') as outfile:
        json.dump(final_results, outfile, indent=4)

def create_agent_player_mapping(agent_file_path, player_file_path, output_file_path):
    """
    create_agent_player_mapping

    Create a mapping file and extract agent-wise data

    :param agent_file_path: contains agent mapping and data
    :param player_file_path: contains player data
    :param output_file_path: file where the mapping has to be saved
    :return: void
    """
    # Load the agent mapping from the first input file
    with open(agent_file_path, 'r') as agent_file:
        agents = json.load(agent_file)

    # Load the player data from the second input file
    with open(player_file_path, 'r') as player_file:
        players = json.load(player_file)

    # Create a mapping of agent_name to agent_id for quick lookup
    agent_name_to_id = {agent["agent_name"]: agent["agent_id"] for agent in agents}

    # Initialize the output list that will store the mappings
    output_data = []

    # Process each player
    for player in players:
        player_id = player["player_id"]

        # For each agent in the mapping file, process the player's stats
        for agent_name, agent_id in agent_name_to_id.items():
            matches_key = f"matchesAs{agent_name}"
            kda_key = f"{agent_name}KDA"

            # Get the matches played and KDA; default to 0 if not available
            matches_played = player.get(matches_key, 0)
            kda = player.get(kda_key, 0)

            # Add this data to the output list
            output_data.append({
                "player_id": player_id,
                "agent_id": agent_id,
                "matches_played": matches_played,
                "KDA": kda
            })

    # Write the output data to the output JSON file
    with open(output_file_path, 'w') as output_file:
        json.dump(output_data, output_file, indent=4)

def process_player_data(input_file_path, output_file_path):
    """
    process_player_data

    Process player data and modify some key value pairs

    :param input_file_path: JSON file with all data
    :param output_file_path: JSON file with processed data
    :return: void
    """
    # Load the input JSON file
    with open(input_file_path, 'r') as input_file:
        player_data = json.load(input_file)

    # Define the list of keys to keep
    keys_to_keep = [
        "player_id", "real_name", "inGameName", "status", "home_team_id",
        "attackKills2022", "attackKills2023", "attackKills2024",
        "defenseKills2022", "defenseKills2023", "defenseKills2024",
        "attackDeaths2022", "attackDeaths2023", "attackDeaths2024",
        "defenseDeaths2022", "defenseDeaths2023", "defenseDeaths2024",
        "attackAssists2022", "attackAssists2023", "attackAssists2024",
        "defenseAssists2022", "defenseAssists2023", "defenseAssists2024",
        "aces", "fourKills", "operatorKills", "ACS", "pistolKills",
        "matchesPlayed", "level", "IGL", "headshotPercentage", "averageAttackFirstKills", "averageAttackFirstDeaths", "averageDefenseFirstKills", "averageDefenseFirstDeaths"
    ]

    # Initialize the output data list
    output_data = []

    # Process each player object
    for player in player_data:
        # Create a new player dictionary with only the specified keys
        processed_player = {key: player[key] for key in keys_to_keep if key in player}

        # Add the "gender" key based on the "level"
        level = processed_player.get("level")
        if level == "Professional" or level == "Semi-Professional":
            processed_player["gender"] = "male"
        elif level == "Game-Changer":
            processed_player["gender"] = "female/others"
        else:
            processed_player["gender"] = "unknown"

        # Append the processed player object to the output data list
        output_data.append(processed_player)

    # Write the output data to the output JSON file
    with open(output_file_path, 'w') as output_file:
        json.dump(output_data, output_file, indent=4)

def merge_player_data(input_file):
    """
    merge_player_data

    Merge year wise stats into one for smaller size

    :param input_file: contains the file with all player data
    :return: void
    """
    # Open and read the input JSON file
    with open(input_file, 'r') as f:
        players_data = json.load(f)

    for player in players_data:
        # Initialize the values for the new fields
        total_attack_kills = 0
        total_defense_kills = 0
        total_attack_deaths = 0
        total_defense_deaths = 0
        total_attack_assists = 0
        total_defense_assists = 0
        years_active = []

        # Loop through years 2022, 2023, and 2024 to aggregate KDA and gather years active
        for year in ["2022", "2023", "2024"]:
            attack_kills = player[f"attackKills{year}"]
            defense_kills = player[f"defenseKills{year}"]
            attack_deaths = player[f"attackDeaths{year}"]
            defense_deaths = player[f"defenseDeaths{year}"]
            attack_assists = player[f"attackAssists{year}"]
            defense_assists = player[f"defenseAssists{year}"]

            # Sum total kills, deaths, assists
            total_attack_kills += attack_kills
            total_defense_kills += defense_kills
            total_attack_deaths += attack_deaths
            total_defense_deaths += defense_deaths
            total_attack_assists += attack_assists
            total_defense_assists += defense_assists

            # Check if any value for the year is greater than 0 and add to years_active
            if (attack_kills + defense_kills + attack_deaths + defense_deaths + attack_assists + defense_assists) > 0:
                years_active.append(year)

        # Calculate KDA ratios for attack and defense
        attack_kda_ratio = (total_attack_kills + total_attack_assists) / total_attack_deaths if total_attack_deaths > 0 else total_attack_kills + total_attack_assists
        defense_kda_ratio = (total_defense_kills + total_defense_assists) / total_defense_deaths if total_defense_deaths > 0 else total_defense_kills + total_defense_assists

        # Create new KDA and aggregated stats
        player["attackKDA"] = round(attack_kda_ratio, 2)
        player["defenseKDA"] = round(defense_kda_ratio, 2)

        # Total Kills, Deaths, Assists
        player["totalKills"] = total_attack_kills + total_defense_kills
        player["totalDeaths"] = total_attack_deaths + total_defense_deaths
        player["totalAssists"] = total_attack_assists + total_defense_assists

        # Combine years active into a comma-separated string
        player["yearsActive"] = ",".join(years_active)

        # Remove old year-specific keys
        for year in ["2022", "2023", "2024"]:
            del player[f"attackKills{year}"]
            del player[f"defenseKills{year}"]
            del player[f"attackDeaths{year}"]
            del player[f"defenseDeaths{year}"]
            del player[f"attackAssists{year}"]
            del player[f"defenseAssists{year}"]

    # Write the modified data back to the output file
    with open(input_file, 'w') as f:
        json.dump(players_data, f, indent=4)

def update_player_levels(json_file_path):
    """
    Updates the 'level' key in each object of a JSON array based on specified criteria.

    Parameters:
    - json_file_path: Path to the JSON file containing an array of player objects.
    """
    # Read the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Loop through each object in the array
    for player in data:
        # Update the 'level' key based on the criteria
        if player.get('level') == "Professional":
            player['level'] = "VCT International"
        elif player.get('level') == "Semi-Professional":
            player['level'] = "VCT Challengers"
        elif player.get('level') == "Game-Changer":
            player['level'] = "VCT Game Changers"

    # Write the updated data back to the JSON file
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)










