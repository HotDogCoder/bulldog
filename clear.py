import os
import shutil

def list_pycache_folders(directory):
    pycache_folders = []
    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            if dir == '__pycache__':
                pycache_folders.append(os.path.join(root, dir))
    return pycache_folders

def delete_pycache_folders(directory):
    pycache_folders = list_pycache_folders(directory)
    if not pycache_folders:
        print("No __pycache__ folders found.")
        return

    print("List of __pycache__ folders to be deleted:")
    for folder in pycache_folders:
        print(folder)

    confirmation = input("Do you want to continue and delete these folders? (yes/no): ").lower()
    if confirmation == 'yes':
        for folder in pycache_folders:
            shutil.rmtree(folder)
            print(f"Deleted: {folder}")
    else:
        print("Deletion aborted.")

# Replace 'directory_path' with the path to the root directory where you want to delete __pycache__ folders
directory_path = '.'
delete_pycache_folders(directory_path)
