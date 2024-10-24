import os
import gzip
import shutil

def extract_gz_files(folder_path):
    """
    extract_gz_files

    Extracts all .gz files inside the given folder.

    :param folder_path: a path to a folder which contains all .gz files
    :return: void
    """
    try:
        files = os.listdir(folder_path)

        gz_files = [file for file in files if file.endswith('.gz')]

        if len(gz_files) == 0:
            print('No .gz files found in the folder.')
            return

        for gz_file in gz_files:
            gz_file_path = os.path.join(folder_path, gz_file)
            json_file_path = gz_file_path.replace('.gz', '')

            if os.path.exists(json_file_path):
                print(f"Skipping {gz_file}, already extracted.")
                continue

            print(f"Processing file: {gz_file}")

            with gzip.open(gz_file_path, 'rb') as f_in:
                with open(json_file_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

            print(f"Successfully extracted to {json_file_path}")

        print("Done")

    except Exception as e:
        print(f"Error: {e}")
        return

# Example usage
# extract_gz_files('./vct-international/games/2023')
