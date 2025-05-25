import wave
import math
import struct
import os
import random

# --- Parameters for the Weak Enemy Attack Sound ---
SAMPLE_RATE = 16000  # Hz
DURATION = 0.2       # Seconds (Short for a weak attack)

# Pop characteristics (at the very beginning)
POP_DURATION_RATIO = 0.15 # How much of the DURATION is the "pop" (e.g., 0.15 = 15%)
POP_START_FREQ = 2200     # Hz - Start high for the pop
# The pop will sweep down to the TAIL_START_FREQ

# Tail characteristics (the main part of the sound after the pop)
TAIL_START_FREQ = 1000    # Hz - Frequency after the initial pop
TAIL_END_FREQ = 600       # Hz - End frequency for a slight downward pitch

# Mixing
SINE_MIX = 0.9            # How much of the sine wave component (0.0 to 1.0)
NOISE_MIX = 0.2           # How much of the noise component (0.0 to 1.0) - keep low for weak sound

MAX_AMPLITUDE = 90       # Amplitude (0-127). Lower for a weaker sound.
DECAY_RATE = 10.0         # How quickly the sound fades (higher = faster fade)
# To make the pop more distinct and the decay faster initially:
AMPLITUDE_DECAY_SHAPE_POW = 1.5 # Power for progress in decay (e.g., progress**1.5 makes it decay faster at start)

OUTPUT_FILENAME = "res/elaser.wav"
# ------------------------------------

# Ensure the 'res' directory exists
if not os.path.exists("res"):
    os.makedirs("res")
    print("Created 'res' directory.")

# Calculate total number of samples
num_samples = int(DURATION * SAMPLE_RATE)
pop_num_samples = int(num_samples * POP_DURATION_RATIO)

# Generate audio data samples
audio_data = bytearray()

print(f"Generating {num_samples} samples for '{OUTPUT_FILENAME}'...")

for i in range(num_samples):
    # Calculate time in seconds for this sample
    t = float(i) / SAMPLE_RATE

    # Calculate overall progress through the sound (0.0 to 1.0)
    progress = float(i) / num_samples

    # 1. Calculate Master Amplitude Envelope
    #    Using a power on progress makes the decay faster at the beginning
    amplitude_decay_progress = progress ** AMPLITUDE_DECAY_SHAPE_POW
    current_master_amplitude = MAX_AMPLITUDE * math.exp(-DECAY_RATE * amplitude_decay_progress)

    # 2. Calculate Frequency (Two-phase: Pop then Tail)
    current_freq = 0
    if i < pop_num_samples:
        # Pop phase: Sweep from POP_START_FREQ down to TAIL_START_FREQ
        pop_progress = float(i) / pop_num_samples # Progress within the pop phase (0.0 to 1.0)
        current_freq = POP_START_FREQ + (TAIL_START_FREQ - POP_START_FREQ) * pop_progress
    else:
        # Tail phase: Sweep from TAIL_START_FREQ down to TAIL_END_FREQ
        # Ensure tail_num_samples is not zero to avoid division by zero
        tail_total_samples = num_samples - pop_num_samples
        if tail_total_samples > 0:
            tail_progress = float(i - pop_num_samples) / tail_total_samples # Progress within the tail phase
            current_freq = TAIL_START_FREQ + (TAIL_END_FREQ - TAIL_START_FREQ) * tail_progress
        else: # Should not happen if DURATION and POP_DURATION_RATIO are sensible
            current_freq = TAIL_END_FREQ


    # 3. Generate Sine Wave value for the current frequency
    sine_value = math.sin(2.0 * math.pi * current_freq * t)

    # 4. Generate Noise Component (White Noise)
    noise_value = (random.random() * 2.0 - 1.0)

    # 5. Mix Sine and Noise
    mixed_signal_unscaled = (sine_value * SINE_MIX) + (noise_value * NOISE_MIX)
    # Optional: Normalize if combined mix factors are high
    # total_mix_factor = SINE_MIX + NOISE_MIX
    # if total_mix_factor > 1.0:
    #     mixed_signal_unscaled /= total_mix_factor


    # 6. Scale mixed signal by master amplitude and shift to 8-bit unsigned range (0-255)
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
        wf.setnchannels(1)
        wf.setsampwidth(1)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_data)
    print(f"Successfully generated {OUTPUT_FILENAME}!")
except Exception as e:
    print(f"Error writing WAV file: {e}")