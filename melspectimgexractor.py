'''

Components of a Mel Spectrogram:

	•	X-axis (Time): Represents the progression of time.
	•	Y-axis (Frequency in Mel scale): Represents the different frequencies in Mel scale, from low to high.
	•	Color Intensity: Represents the amplitude or energy at each frequency band at a given time. Brighter or darker regions indicate stronger or weaker amplitudes.

'''


import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

def save_mel_spectrogram(audio_path, output_image_path):
    # Load the audio file
    y, sr = librosa.load(audio_path, sr=None)

    # Generate the Mel Spectrogram
    mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)

    # Convert power (amplitude squared) to decibel (log scale)
    mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)

    # Plot the Mel Spectrogram
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(mel_spectrogram_db, sr=sr, x_axis='time', y_axis='mel', fmax=8000)

    # Add a color bar to indicate decibel levels
    plt.colorbar(format='%+2.0f dB')

    # Add labels for the axes
    plt.title('Mel Spectrogram')
    plt.tight_layout()

    # Save the plot as an image
    plt.savefig(output_image_path)
    plt.close()

# Example usage
audio_path = '/Users/ashutosh/Documents/GitHub/edm-subgenre-classification/audioTest/Mr Afro Deep - AfricanTool - Coming Through (Main Mix).mp3'  # Replace with the path to your audio file
output_image_path = 'mel_spectrogram_image.png'  # Output image file name
save_mel_spectrogram(audio_path, output_image_path)