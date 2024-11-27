import os
import numpy as np
import pandas as pd
import librosa
from pyAudioAnalysis import audioBasicIO, ShortTermFeatures

# Define the root folder containing subfolders of audio files
folder = r"C:\Users\ashut\Desktop\DATASET\TRAIN"

# Prepare a list to hold data for all audio files
dataALL = []

# Duration to process (in seconds)
durationToProcess = 120  # Change this to the desired duration (in seconds)

# Iterate over each subfolder and file in the root folder
for subfolder, dirs, files in os.walk(folder):
    genre = os.path.basename(subfolder)  # Use the subfolder name as the genre
    for file in files:
        if file.endswith(".mp3"):  # Only process .mp3 files
            audioFilepath = os.path.join(subfolder, file)
            print(f"Processing file: {audioFilepath}")

            # Load the audio file using librosa
            try:
                x, Fs = librosa.load(audioFilepath, sr=None, mono=True, duration=durationToProcess)
            except Exception as e:
                print(f"Error reading {audioFilepath}: {e}")
                continue

            if x.size == 0:
                print(f"Warning: Skipping empty audio file {audioFilepath}")
                continue

            # Extract short-term features using pyAudioAnalysis
            F, f_name = ShortTermFeatures.feature_extraction(x, Fs, 0.050 * Fs, 0.025 * Fs)

            # Calculate the means of the features
            feature_means = {name: F[i, :].mean() for i, name in enumerate(f_name)}

            # Additional features using librosa
            try:
                # Onset detection
                onset_env = librosa.onset.onset_strength(y=x, sr=Fs)
                onsets = len(librosa.onset.onset_detect(y=x, sr=Fs))
                feature_means['Onsets'] = onsets

                # Harmonic and percussive components
                harmonic, percussive = librosa.effects.hpss(x)
                feature_means['Harmonic Mean'] = np.mean(harmonic)
                feature_means['Percussive Mean'] = np.mean(percussive)

                # CQT (Constant-Q Transform)
                cqt = librosa.cqt(x, sr=Fs)
                feature_means['CQT Mean'] = np.mean(np.abs(cqt))

                # Beat Synchronization
                mfcc = librosa.feature.mfcc(y=x, sr=Fs)
                tempo, beat_frames = librosa.beat.beat_track(y=x, sr=Fs)
                beat_mfcc = librosa.util.sync(mfcc, beat_frames, aggregate=np.mean)
                feature_means['Beat Sync MFCC Mean'] = np.mean(beat_mfcc)

                # Rhythm Complexity
                fourier_tempogram = librosa.feature.fourier_tempogram(y=x, sr=Fs)
                rhythm_complexity = np.mean(fourier_tempogram)
                feature_means['Rhythm Complexity'] = rhythm_complexity

            except Exception as e:
                print(f"Error extracting additional features for {audioFilepath}: {e}")
                feature_means['Onsets'] = 0
                feature_means['Harmonic Mean'] = 0
                feature_means['Percussive Mean'] = 0
                feature_means['CQT Mean'] = 0
                feature_means['Beat Sync MFCC Mean'] = 0
                feature_means['Rhythm Complexity'] = 0

            # Extract tempogram and compute tempo
            try:
                tempo = librosa.feature.rhythm.tempo(onset_envelope=onset_env, sr=Fs)[0]  # Updated method
                feature_means['Tempo'] = tempo

                # Extract Tempogram
                tempogram = librosa.feature.tempogram(y=x, sr=Fs)
                feature_means['Tempogram Mean'] = np.mean(tempogram)

            except Exception as e:
                print(f"Error extracting tempo/tempogram for {audioFilepath}: {e}")
                feature_means['Tempo'] = 0
                feature_means['Tempogram Mean'] = 0

            # Add genre and file name to the feature dictionary
            feature_means['Genre'] = genre
            feature_means['File Name'] = file

            # Append the data to the list
            dataALL.append(feature_means)

# Create a DataFrame from the list of feature data
df = pd.DataFrame(dataALL)

# Set display options to avoid scientific notation
pd.set_option('display.float_format', '{:.15f}'.format)

# Save the DataFrame to an Excel file
output_filepath = r"C:\Users\ashut\Desktop\DATASET\TRAINFINAL8FEATURESEXTRA.xlsx"
df.to_excel(output_filepath, index=False)

print(f"Features for all audio files saved to {output_filepath}")
