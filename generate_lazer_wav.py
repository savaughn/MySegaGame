import wave
import math
import struct
import os

# --- Parameters for the Laser Sound ---
SAMPLE_RATE = 16000  # Hz (CD quality is 44100, lower saves space)
DURATION = 0.15     # Seconds (Keep it short)
START_FREQ = 1800   # Starting frequency in Hz
END_FREQ = 300      # Ending frequency in Hz
MAX_AMPLITUDE = 110 # Amplitude (0-127 for 8-bit centered at 128). Lower avoids clipping.
DECAY_RATE = 5.0    # How quickly the sound fades (higher value = faster fade)
OUTPUT_FILENAME = "res/laser.wav"
# ------------------------------------

# Ensure the 'res' directory exists
if not os.path.exists("res"):
    os.makedirs("res")
    print("Created 'res' directory.")

# Calculate total number of samples
num_samples = int(DURATION * SAMPLE_RATE)

# Generate audio data samples
audio_data = bytearray()

print(f"Generating {num_samples} samples...")

for i in range(num_samples):
    # Calculate time in seconds for this sample
    t = float(i) / SAMPLE_RATE

    # Calculate progress through the sound (0.0 to 1.0)
    progress = float(i) / num_samples

    # 1. Calculate Frequency (Linear sweep down)
    current_freq = START_FREQ + (END_FREQ - START_FREQ) * progress

    # 2. Calculate Amplitude (Exponential decay)
    # amplitude = MAX_AMPLITUDE * (1.0 - progress) # Linear decay alternative
    amplitude = MAX_AMPLITUDE * math.exp(-DECAY_RATE * progress)

    # 3. Generate Sine Wave value for the current frequency
    # Value ranges from -1.0 to 1.0
    sine_value = math.sin(2.0 * math.pi * current_freq * t)

    # 4. Scale sine wave by amplitude and shift to 8-bit unsigned range (0-255)
    # The center is 128. We add the scaled sine value.
    byte_value_float = 128.0 + (amplitude * sine_value)

    # Clamp the value to ensure it's within the 0-255 range
    byte_value = int(max(0.0, min(255.0, byte_value_float)))

    # Pack the integer value as an unsigned byte ('B')
    packed_value = struct.pack('B', byte_value)
    audio_data.extend(packed_value)

# Write the audio data to a WAV file
print(f"Writing WAV file: {OUTPUT_FILENAME}")
try:
    with wave.open(OUTPUT_FILENAME, 'wb') as wf:
        # Set WAV file parameters
        wf.setnchannels(1)         # Mono
        wf.setsampwidth(1)         # 1 byte = 8 bits (for 8-bit unsigned)
        wf.setframerate(SAMPLE_RATE) # Sample rate
        # Write the packed byte data
        wf.writeframes(audio_data)
    print("Successfully generated laser.wav!")
except Exception as e:
    print(f"Error writing WAV file: {e}")