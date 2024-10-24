import os
import gzip
import shutil

def zip_json_files(folder_path):
    """
    zip_json_files

    zips all json files present inside the provided folder

    :param folder_path: A folder path which contains json files to zip
    :return: void
    """
    # Loop through all files in the specified folder
    for filename in os.listdir(folder_path):
        # Check if the file is a .json file
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            gz_file_path = file_path + ".gz"

            # Open the .json file and compress it into a .gz file
            with open(file_path, 'rb') as f_in:
                with gzip.open(gz_file_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

            print(f"Zipped: {filename} to {gz_file_path}")

# Example usage
# zip_json_files("./game-changers/games/2022")