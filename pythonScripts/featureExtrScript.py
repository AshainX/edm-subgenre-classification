import os
import numpy as np
import pandas as pd
from pyAudioAnalysis import audioBasicIO, ShortTermFeatures
import librosa

# Define the root folder containing subfolders of audio files
rootFolder = r"C:\Users\ashut\Documents\GitHub\edm-subgenre-classification\test"

# Prepare a list to hold data for all audio files
all_data = []

# Duration to process (in seconds)
durationToProcess = 60

# Define tempos to analyze from 60 to 200 BPM in increments of 10
tempos = np.arange(60, 201, 10)

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

            # Convert stereo to mono
            x = audioBasicIO.stereo_to_mono(x)

            # Trim the audio to the first 60 seconds if it's longer
            numSamplesToProcess = int(durationToProcess * Fs)
            x = x[:numSamplesToProcess] if x.size > numSamplesToProcess else x

            # Extract short-term features
            F, f_name = ShortTermFeatures.feature_extraction(x, Fs, 0.050 * Fs, 0.025 * Fs)

            # Calculate the means of the features
            feature_means = {name: F[i, :].mean() for i, name in enumerate(f_name)}

            # Compute tempogram using librosa
            y, sr = librosa.load(audioFilepath, sr=Fs, mono=True, duration=durationToProcess)
            onset_env = librosa.onset.onset_strength(y=y, sr=sr, aggregate=np.median)
            tempogram = librosa.feature.tempogram(onset_envelope=onset_env, sr=sr)
            
            # Calculate the tempo and BPM
            tempo_mean = np.mean(tempos)
            tempo_std = np.std(tempos)
            tempo_max = np.max(tempos)
            bpm = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)
            
            # Add tempogram-based metrics to feature dictionary
            feature_means.update({
                'Tempo Mean': tempo_mean,
                'Tempo Std': tempo_std,
                'Max Tempo': tempo_max,
                'BPM': bpm[0] if bpm.size > 0 else 0
            })
            
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
output_filepath = r"C:\Users\ashut\Desktop\edm_subgenre_features_all.xlsx"
df.to_excel(output_filepath, index=False)

print(f"Features for all audio files saved to {output_filepath}")
