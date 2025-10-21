import numpy as np
from matplotlib import pyplot as plt
from scipy.fft import fft, fftfreq
import scipy.io.wavfile as wav
import json

# Embedded note frequency map
NOTES_MAP = json.load(open("notes_map.json", "r"))


# Load WAV file
WAVE_LOCATION = "./secret_tunes.wav"
SAMPLE_RATE, data = wav.read(WAVE_LOCATION)

# Convert stereo to mono if needed
if len(data.shape) == 2:
    data = data.mean(axis=1)

# Normalize audio
data = data / np.max(np.abs(data))

# Use full duration of audio
samples_to_analyze = len(data)

# Time domain plot
t = np.arange(samples_to_analyze) / SAMPLE_RATE
plt.figure(figsize=(10, 4))
plt.plot(t, data[:samples_to_analyze])
plt.title("Waveform")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.tight_layout()
plt.show()

# Frequency domain plot
yf = fft(data[:samples_to_analyze])
xf = fftfreq(samples_to_analyze, 1 / SAMPLE_RATE)
plt.figure(figsize=(10, 4))
plt.plot(xf[:samples_to_analyze // 2], np.abs(yf[:samples_to_analyze // 2]))
plt.title("Frequency Spectrum")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.xlim([0, 3000])
plt.tight_layout()
plt.show()

# Extract significant frequencies
magnitudes = np.abs(yf[:samples_to_analyze // 2])
frequencies = xf[:samples_to_analyze // 2]
threshold = np.max(magnitudes) * 0.1
significant_freqs = frequencies[magnitudes > threshold]

# Map frequencies to notes
detected_notes = set()
for freq in significant_freqs:
    for note, note_freq in NOTES_MAP.items():
        if abs(freq - note_freq) <= 4:
            detected_notes.add(note)

# Output all detected notes
print("🎵 Detected Notes:", sorted(detected_notes))