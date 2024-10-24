import json
from sqlExecutor import connect_to_rds, execute_sql

def process_json_and_insert_leagues (json_file_path):
    """
    process_json_and_insert_leagues

    Given a JSON file, extract league information and send it to the database.

    :param json_file_path: the path to the JSON file which contains league data.
    :return: void
    """
    try:
        with open(json_file_path, 'r') as file:
            leagues = json.load(file)

        connection = connect_to_rds()

        if connection:
            for league in leagues:
                league_id = league.get('league_id')
                league_region = league.get('region')
                league_name = league.get('name')
                # Use light_logo_url if available, otherwise use dark_logo_url
                league_logo_url = league.get('light_logo_url') or league.get('dark_logo_url')

                sql_query = """
                INSERT INTO leagues (league_id, league_region, league_logo_url, league_name) 
                VALUES ({}, "{}", "{}", "{}")
                ON DUPLICATE KEY UPDATE
                    league_region = "{}",
                    league_logo_url = "{}",
                    league_name = "{}"
                """.format(league_id, league_region, league_logo_url, league_name, league_region, league_logo_url, league_name)

                execute_sql(connection, sql_query)

            connection.close()
    except Exception as e:
        print(f"Error processing JSON file: {e}")

# Usage example
# if __name__ == "__main__":
#     json_file_path = './vct-international/esports-data/leagues.json'
#     process_json_and_insert_leagues(json_file_path)
