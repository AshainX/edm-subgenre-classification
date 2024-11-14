import os
import numpy as np
import librosa
import matplotlib.pyplot as plt

# Define the root folder containing subfolders of audio files
rootFolder = r"/Users/ashutosh/Library/CloudStorage/GoogleDrive-ashutosh.2300705008@cukerala.ac.in/My Drive/DATASET /new_data_TRAINTESTSPLIT/TEST"

# Define the duration (in seconds) to process
max_duration_sec = 120

# Define the output directory for Mel spectrogram images
outputRootFolder = r"/Users/ashutosh/Documents/GitHub/edm-subgenre-classification/MelImages"
# Create the output root folder if it doesn't exist
os.makedirs(outputRootFolder, exist_ok=True)

# Iterate over each subfolder and file in the root folder
for subfolder, dirs, files in os.walk(rootFolder):
    genre = os.path.basename(subfolder)  # Use the subfolder name as the genre

    # Create an output folder for each genre
    genreOutputFolder = os.path.join(outputRootFolder, genre)
    os.makedirs(genreOutputFolder, exist_ok=True)

    # Initialize a counter for the images
    image_counter = 1

    for file in files:
        if file.endswith(".mp3"):  # Only process .mp3 files
            audioFilepath = os.path.join(subfolder, file)
            print(f"Processing file: {audioFilepath}")

            # Load audio file and limit to 120 seconds if longer
            x, Fs = librosa.load(audioFilepath, sr=None)
            x = x[:int(Fs * max_duration_sec)]

            # Generate Mel spectrogram
            mel_spectrogram = librosa.feature.melspectrogram(y=x, sr=Fs, n_mels=128, fmax=8000)
            mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)

            # Plot the Mel spectrogram image without axes or labels
            plt.figure(figsize=(10, 4))
            plt.axis('off')
            librosa.display.specshow(mel_spectrogram_db, sr=Fs, fmax=8000, cmap='inferno')
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

            # Define image name and save path
            image_name = f"{genre}{image_counter}.png"
            image_path = os.path.join(genreOutputFolder, image_name)
            plt.savefig(image_path, bbox_inches='tight', pad_inches=0)
            plt.close()
            print(f"Saved Mel spectrogram image: {image_path}")

            # Increment the image counter
            image_counter += 1