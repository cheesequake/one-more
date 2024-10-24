import json
import sqlExecutor

def insert_agents_data(json_file_path):
    """
    insert_agents_data

    :param json_file_path: A JSON File path which contains agent data
    :return: void
    """
    with open(json_file_path, 'r', encoding='utf-8') as file:
        agents_data = json.load(file)

    connection = sqlExecutor.connect_to_rds()

    for agent in agents_data:
        agent_name = agent['agent_name']
        agent_id = agent['agent_id']
        role = agent['role']

        sql_query = f"""
        INSERT INTO agents (agent_name, agent_id, role)
        VALUES ('{agent_name}', '{agent_id}', '{role}');
        """

        try:
            sqlExecutor.execute_sql(connection, sql_query)
            print(f"Inserted agent: {agent_name}")
        except Exception as e:
            print(f"Error inserting agent {agent_name}: {e}")

    connection.close()

    print("Finished inserting agent data.")

# Example usage:
# insert_agents_data('./agent_mapping.json')
