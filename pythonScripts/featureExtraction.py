''' 
Procesing for the TEST folder files


'''

import os
import numpy as np
import pandas as pd
from pyAudioAnalysis import audioBasicIO, ShortTermFeatures

# Define the root folder containing subfolders of audio files
folder = r"/Users/ashutosh/Library/CloudStorage/GoogleDrive-ashutosh.2300705008@cukerala.ac.in/My Drive/DATASET /new_data_TRAINTESTSPLIT/TRAIN"

# Prepare a list to hold data for all audio files
dataALL = []

# Iterate over each subfolder and file in the root folder
for subfolder, dirs, files in os.walk(folder):
    genre = os.path.basename(subfolder)  # Use the subfolder name as the genre
    for file in files:
        if file.endswith(".mp3"):  # Only process .mp3 files
            audioFilepath = os.path.join(subfolder, file)
            print(f"Processing file: {audioFilepath}")

            # Read audio file
            [Fs, x] = audioBasicIO.read_audio_file(audioFilepath)
            if x.size == 0:
                print(f"Warning: Skipping empty audio file {audioFilepath}")
                continue

            # Convert stereo to mono
            x = audioBasicIO.stereo_to_mono(x)

            # Extract short-term features
            F, f_name = ShortTermFeatures.feature_extraction(x, Fs, 0.050 * Fs, 0.025 * Fs)

            # Calculate the means of the features
            feature_means = {name: F[i, :].mean() for i, name in enumerate(f_name)}

            # Add genre and file name to the feature dictionary
            feature_means['Genre'] = genre
            feature_means['File Name'] = file

            # Append the data to the list
            dataALL.append(feature_means)

# Create a DataFrame from the list of feature data
df = pd.DataFrame(dataALL)

# Set display options to avoid scientific notation
pd.set_option('display.t_format', '{:.15f}'.format)

# Save the DataFrame to an Excel file
output_filepath = r"/Users/ashutosh/Library/CloudStorage/GoogleDrive-ashutosh.2300705008@cukerala.ac.in/My Drive/DATASET /new_data_TRAINTESTSPLIT.xlsx"
df.to_excel(output_filepath, index=False)

print(f"Features for all audio files saved to {output_filepath}")
