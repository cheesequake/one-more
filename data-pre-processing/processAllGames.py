import os
import json
from processGameEvents import process_game_events

def process_mapping_data(mapping_data_file, match_folder_path, output_json_path):
    """
    process_mapping_data

    Process mapping data for all games in the folder

    :param mapping_data_file: mapping_json (and v2) file from public data
    :param match_folder_path: folder path which contains all games
    :param output_json_path: a file which contains player data (initialised, not populated)
    """
    print("Starting processing of mapping data...")

    with open(mapping_data_file, 'r', encoding='utf-8') as mapping_file:
        mapping_data = json.load(mapping_file)

    with open(output_json_path, 'r', encoding='utf-8') as f:
        player_data = json.load(f)

    for match in mapping_data:
        platform_game_id = match["platformGameId"].replace(":", "_")  # Replace colon with underscore
        match_file_path = os.path.join(match_folder_path, f"{platform_game_id}.json")

        # Check if the match file exists
        if not os.path.exists(match_file_path):
            print(f"Match file {match_file_path} not found, skipping...")
            continue

        # Print that file processing has started
        print(f"Processing match file {match_file_path}...")

        # Check for a corrupted or invalid JSON file
        try:
            game_stats = process_game_events(match_file_path)
            if (game_stats == None):
                continue
        except (json.JSONDecodeError, OSError, ValueError) as e:
            print(f"Error processing match file {match_file_path}: {e}, skipping...")
            continue

        # Year from folder name
        folder_year = match_folder_path[-4:]

        # Map participant stats from the game to the correct player in player_data
        for participant, player_id in match["participantMapping"].items():
            player_id = str(player_id)
            team_ids = [int(key) for key in match['teamMapping'].keys()]
            higher_team_id = max(team_ids)
            lower_team_id = min(team_ids)
            higher_team_match_id = match['teamMapping'][str(higher_team_id)]
            lower_team_match_id = match['teamMapping'][str(lower_team_id)]
            team_id = higher_team_match_id if 1 <= int(participant) <= 5 else lower_team_match_id

            # Skip if player not initialized in player_data
            player_entry = next((p for p in player_data if p['id'] == player_id and p['home_team_id'] == team_id), None)
            if not player_entry:
                print ("Skipped cause no player entry: "+player_id+ " team:"+team_id)
                continue
            # Convert participant (string) to an integer when accessing game_stats
            participant_int = int(participant)
            agent = game_stats[participant_int].get("selectedAgent", "")

            player_entry[f"attackKills{folder_year}"] += game_stats[participant_int].get("attackKills", 0)
            player_entry[f"defenseKills{folder_year}"] += game_stats[participant_int].get("defenseKills", 0)
            player_entry[f"attackDeaths{folder_year}"] += game_stats[participant_int].get("attackDeaths", 0)
            player_entry[f"defenseDeaths{folder_year}"] += game_stats[participant_int].get("defenseDeaths", 0)
            player_entry[f"attackAssists{folder_year}"] += game_stats[participant_int].get("attackAssists", 0)
            player_entry[f"defenseAssists{folder_year}"] += game_stats[participant_int].get("defenseAssists", 0)
            player_entry["attackFirstKills"] += game_stats[participant_int].get("attackFirstKills", 0)
            player_entry["attackFirstDeaths"] += game_stats[participant_int].get("attackFirstDeaths", 0)
            player_entry["defenseFirstKills"] += game_stats[participant_int].get("defenseFirstKills", 0)
            player_entry["defenseFirstDeaths"] += game_stats[participant_int].get("defenseFirstDeaths", 0)
            player_entry["aces"] += game_stats[participant_int].get("aces", 0)
            player_entry["fourKills"] += game_stats[participant_int].get("fourKills", 0)
            player_entry["headShots"] += game_stats[participant_int].get("headShots", 0)
            player_entry["totalShots"] += game_stats[participant_int].get("totalShots", 0)
            player_entry["operatorKills"] += game_stats[participant_int].get("operatorKills", 0)
            player_entry["ACS"] += game_stats[participant_int].get("ACS", 0)
            player_entry["pistolKills"] += game_stats[participant_int].get("pistolKills", 0)
            player_entry["matchesPlayed"] += 1
            player_entry[f"matchesAs{agent}"] += 1
            player_entry[f"{agent}KDA"] += game_stats[participant_int].get("selectedAgentKDA", 0)

    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(player_data, f, indent=4)

    print("Finished processing of mapping data.")


# process_mapping_data ("./vct-international/esports-data/mapping_data_v2.json", "./vct-international/games/2022", "./allPlayersAllData.json")
# process_mapping_data ("./vct-international/esports-data/mapping_data_v2.json", "./vct-international/games/2023", "./allPlayersAllData.json")
# process_mapping_data ("./vct-international/esports-data/mapping_data_v2.json", "./vct-international/games/2024", "./allPlayersAllData.json")