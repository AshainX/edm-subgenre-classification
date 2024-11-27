'''

file processing only 60 sec 

'''

import os
import numpy as np
import pandas as pd
from pyAudioAnalysis import audioBasicIO, ShortTermFeatures

# Define the root folder containing subfolders of audio files
rootFolder = r"C:\Users\ashut\Desktop\DATASET\TRAIN"

# Define the duration (in seconds) to process
duration_sec = 60

# Prepare a list to hold data for all audio files
all_data = []

# Iterate over each subfolder and file in the root folder
for subfolder, dirs, files in os.walk(rootFolder):
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

            # Truncate the audio to 60 seconds
            num_samples = int(Fs * duration_sec)
            x = x[:num_samples]

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
            all_data.append(feature_means)

# Create a DataFrame from the list of feature data
df = pd.DataFrame(all_data)

# Set display options to avoid scientific notation
pd.set_option('display.float_format', '{:.15f}'.format)

# Save the DataFrame to an Excel file
output_filepath = r"C:\Users\ashut\Desktop\DATASET\TRAIN.xlsx"
df.to_excel(output_filepath, index=False)

print(f"Features for all audio files saved to {output_filepath}")
