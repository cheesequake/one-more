import json

def add_igl_field(file_path):
    """
    add_igl_field

    :param file_path: JSON file path which contains player data
    :return: void
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for obj in data:
        obj['IGL'] = False

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def update_igl_field(file_path, target_id):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for obj in data:
        if obj.get('id') == target_id:
            obj['IGL'] = True

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


# update_igl_field ("./allPlayersAllData.json", "112127610985635537")
