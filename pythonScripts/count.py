# import os

# def count_files_in_directory(directory):
#     folder_file_count = {}
    
#     for root, dirs, files in os.walk(directory):
#         folder_file_count[root] = len(files)

#     return folder_file_count

# # Specify the path to your folder
# TEST = r'C:\Users\ashut\Desktop\TRAIN'
# file_counts = count_files_in_directory(TEST)

# # Print the results
# for folder, count in file_counts.items():
#     print(f'Folder: {folder} - Number of files: {count}')


import os

def countFilesInDirectory(directory):
    folderFileCount = {}
    
    for root, dirs, files in os.walk(directory):
        folderFileCount[root] = len(files)
        
        # Ensure to include subdirectories even if they have no files
        for dir in dirs:
            subfolderPath = os.path.join(root, dir)
            if subfolderPath not in folderFileCount:
                folderFileCount[subfolderPath] = 0

    return folderFileCount
#for checking empty folders
# def printEmptyFolders(fileCounts):
#     print("\nFolders with 0 files:")
#     for folder, count in sorted(fileCounts.items()):
#         if count == 0:
#             print(f'Empty Folder: {folder}')

def printFileCounts(fileCounts):
    print("\nFolder and File Count:")
    for folder, count in sorted(fileCounts.items()):
        print(f'Folder: {folder} - Number of files: {count}')

# Specify the path to your folder
TRAIN = r'C:\Users\ashut\Desktop\TRAIN'
TEST = r'C:\Users\ashut\Desktop\TEST'

fileCountTEST = countFilesInDirectory(TEST)
fileCountTRAIN = countFilesInDirectory(TRAIN)

# printing the results
print("TEST Directory Files:")
printFileCounts(fileCountTEST)
# printEmptyFolders(fileCountTEST)

print("\nTRAIN Directory Files:")
printFileCounts(fileCountTRAIN)
# printEmptyFolders(fileCountTRAIN)
