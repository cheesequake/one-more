import os

def delete_files_of_type (folder_path, file_type):
    """
    delete_files_of_type

    Deletes all files in the given folder path of the given file type.

    :param folder_path: Folder path where files are to be deleted from
    :param file_type: Type of files to be deleted from this folder
    :return: void
    """
    try:
        files = os.listdir(folder_path)

        for file_name in files:
            file_path = os.path.join(folder_path, file_name)

            if file_name.endswith(file_type):
                os.remove(file_path)
                print(f'Deleted: {file_name}')

        print('All '+ file_type +' files have been deleted.')
    
    except Exception as e:
        print(f'An error occurred: {e}')

# Example usage
# delete_files_of_type('./vct-international/games/2023', '.gz')