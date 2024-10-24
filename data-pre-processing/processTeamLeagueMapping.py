import json
from sqlExecutor import connect_to_rds, execute_sql

def insert_team_league_mapping(connection, team_id, league_id):
    """
    insert_team_league_mapping

    :param connection: a JSON file path which contains data about team league mappings
    :return: void
    """
    sql_query = f"""
    INSERT INTO team_league_mapping (team_id, league_id)
    VALUES ({team_id}, {league_id});
    """
    execute_sql(connection, sql_query)

def process_json_and_insert_mapping(file_path):
    """
    process_json_and_insert_mapping

    :param file_path: a JSON file path which contains data about team league mappings
    :return: void
    """
    connection = connect_to_rds()
    if not connection:
        print("Failed to connect to the database")
        return

    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

            for record in data:
                team_id = record.get('team_id')
                home_league_id = record.get('home_league_id')

                if team_id and home_league_id:
                    insert_team_league_mapping(connection, team_id, home_league_id)
                else:
                    print(f"Missing data in record: {record}")

        print("Data insertion complete")

    except json.JSONDecodeError as e:
        print(f"Error reading JSON file: {e}")

    finally:
        if connection.is_connected():
            connection.close()
            print("Database connection closed.")

# Run the process with the JSON file path directly in the code
# json_file_path = './vct-international/esports-data/team_league_mapping.json'
# process_json_and_insert_mapping(json_file_path)
