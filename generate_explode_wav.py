import wave
import math
import struct
import os
import random # For generating noise

# --- Parameters for the Explosion/Decompression Sound ---
SAMPLE_RATE = 16000  # Hz (CD quality is 44100, lower saves space)
DURATION = 0.5       # Seconds (Longer for an explosion/decompression)

# Rumble component (sweeping sine wave for the "boom" and pressure release)
RUMBLE_START_FREQ = 800 # Hz - Initial impact/crack sound
RUMBLE_END_FREQ = 35    # Hz - Lingering low rumble
RUMBLE_MIX = 0.6        # How much of the rumble component is present (0.0 to 1.0)

# Noise component (for the chaotic/hissing part)
NOISE_MIX = 0.7         # How much of the noise component is present (0.0 to 1.0)
                        # Note: Rumble_MIX + Noise_MIX can conceptually exceed 1.0,
                        # the final signal is scaled by MAX_AMPLITUDE.

MAX_AMPLITUDE = 105 # Amplitude (0-127 for 8-bit centered at 128).
                    # Keep it a bit lower due to mixing noise, which can have high peaks.
DECAY_RATE = 3.5    # How quickly the sound fades (higher value = faster fade)
                    # For a more "explosive" feel, you might want a sharper initial decay.
                    # e.g., by using progress**0.5 in the decay calculation.

OUTPUT_FILENAME = "res/explosion_decompression.wav"
# ------------------------------------

# Ensure the 'res' directory exists
if not os.path.exists("res"):
    os.makedirs("res")
    print("Created 'res' directory.")

# Calculate total number of samples
num_samples = int(DURATION * SAMPLE_RATE)

# Generate audio data samples
audio_data = bytearray()

print(f"Generating {num_samples} samples for '{OUTPUT_FILENAME}'...")

for i in range(num_samples):
    # Calculate time in seconds for this sample
    t = float(i) / SAMPLE_RATE

    # Calculate progress through the sound (0.0 to 1.0)
    progress = float(i) / num_samples

    # 1. Calculate Master Amplitude Envelope (Exponential decay for the overall sound)
    # To make the initial part of the explosion sharper, you could use:
    # envelope_progress = progress**0.5 # Makes decay faster at the start
    envelope_progress = progress
    current_master_amplitude = MAX_AMPLITUDE * math.exp(-DECAY_RATE * envelope_progress)

    # 2. Generate Rumble Component (Sweeping Sine Wave)
    #    Using progress**2 or progress**3 makes the frequency drop faster initially,
    #    which can sound more like an impact.
    rumble_freq_sweep_progress = progress**2.0
    current_rumble_freq = RUMBLE_START_FREQ + \
                          (RUMBLE_END_FREQ - RUMBLE_START_FREQ) * rumble_freq_sweep_progress
    # Ensure frequency doesn't go below a practical minimum (e.g., 20 Hz)
    current_rumble_freq = max(20.0, current_rumble_freq)
    # Calculate sine wave for rumble, unscaled by its mix factor yet
    rumble_sine_value = math.sin(2.0 * math.pi * current_rumble_freq * t)

    # 3. Generate Noise Component (White Noise)
    #    Random value between -1.0 and 1.0
    noise_value = (random.random() * 2.0 - 1.0)

    # 4. Mix Rumble and Noise, applying their respective mix factors
    #    The combined signal should ideally stay within -1.0 to 1.0 before master amplitude scaling
    #    A simple weighted sum:
    mixed_signal_unscaled = (rumble_sine_value * RUMBLE_MIX) + (noise_value * NOISE_MIX)

    # Optional: Normalize if combined mix factors are high to prevent excessive internal clipping
    # total_mix_factor = RUMBLE_MIX + NOISE_MIX
    # if total_mix_factor > 1.0: # Only normalize if combined sources could exceed 1.0
    # mixed_signal_unscaled /= total_mix_factor

    # 5. Scale mixed signal by master amplitude and shift to 8-bit unsigned range (0-255)
    byte_value_float = 128.0 + (current_master_amplitude * mixed_signal_unscaled)

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
    print(f"Successfully generated {OUTPUT_FILENAME}!")
except Exception as e:
    print(f"Error writing WAV file: {e}")