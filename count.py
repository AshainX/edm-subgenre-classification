# import os

# def count_files_in_directory(directory):
#     folder_file_count = {}
    
#     for root, dirs, files in os.walk(directory):
#         folder_file_count[root] = len(files)

#     return folder_file_count

# # Specify the path to your folder
# folder_path = r'C:\Users\ashut\Desktop\TRAIN'
# file_counts = count_files_in_directory(folder_path)

# # Print the results
# for folder, count in file_counts.items():
#     print(f'Folder: {folder} - Number of files: {count}')


import os

def count_files_in_directory(directory):
    folder_file_count = {}
    
    for root, dirs, files in os.walk(directory):
        folder_file_count[root] = len(files)
        
        # Ensure to include subdirectories even if they have no files
        for dir in dirs:
            subfolder_path = os.path.join(root, dir)
            if subfolder_path not in folder_file_count:
                folder_file_count[subfolder_path] = 0

    return folder_file_count

# Specify the path to your folder
folder_path = r'C:\Users\ashut\Desktop\TRAIN'
file_counts = count_files_in_directory(folder_path)

# Print the results
for folder, count in sorted(file_counts.items()):
    print(f'Folder: {folder} - Number of files: {count}')
