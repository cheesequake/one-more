import json
from sqlExecutor import connect_to_rds, execute_sql

def process_json_and_insert(json_file_path):
    """
    process_json_and_insert

    Process JSON for teams, and insert in the database.

    :param json_file_path: A JSON File path in which teams data is present
    :return: void
    """
    try:
        with open(json_file_path, 'r') as file:
            teams = json.load(file)

        connection = connect_to_rds()

        if connection:
            for team in teams:
                team_id = team.get('id')
                team_acronym = team.get('acronym')
                team_name = team.get('name')
                # Use light_logo_url if available, otherwise use dark_logo_url
                team_logo_url = team.get('light_logo_url') or team.get('dark_logo_url')

                sql_query = """
                INSERT INTO teams (team_id, team_acronym, team_logo_url, team_name) 
                VALUES ({}, "{}", "{}", "{}")
                ON DUPLICATE KEY UPDATE
                    team_acronym = "{}",
                    team_logo_url = "{}",
                    team_name = "{}"
                """.format(team_id, team_acronym, team_logo_url, team_name, team_acronym, team_logo_url, team_name)

                execute_sql(connection, sql_query)

            connection.close()
    except Exception as e:
        print(f"Error processing JSON file: {e}")

# # Usage example
# if __name__ == "__main__":
#     json_file_path = './vct-international/esports-data/teams.json'
#     process_json_and_insert(json_file_path)
