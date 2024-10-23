import os
import re

def renameAudioFiles(folderPath):
    # Regex pattern to match files starting with numbers followed by a period and a space
    pattern = r"^\d+\.\s+"

    # Traverse through all the subdirectories and files in the folder
    for dirpath, dirnames, filenames in os.walk(folderPath):
        for filename in filenames:
            # Check if the filename starts with numbers followed by a period and space
            if re.match(pattern, filename):
                newFilename = re.sub(pattern, '', filename)  # Remove the number part
                # Construct the full path for the current and new filenames
                oldFilePath = os.path.join(dirpath, filename)
                newFilePath = os.path.join(dirpath, newFilename)
                # Rename the file
                os.rename(oldFilePath, newFilePath)
                print(f"Renamed: {oldFilePath} -> {newFilePath}")

# Define the paths for TRAIN and TEST folders
trainFolderPath = r"C:\Users\ashut\Desktop\edm subgenre\TRAIN"
testFolderPath = r"C:\Users\ashut\Desktop\edm subgenre\TEST"

renameAudioFiles(trainFolderPath)
renameAudioFiles(testFolderPath)
