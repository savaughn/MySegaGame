import wave
import math
import struct
import os
import random

# --- Parameters for the Shield Ready Sound ---
SAMPLE_RATE = 13300  # Hz
DURATION = 0.5       # Seconds (Relatively short, clear notification)

# Volume Control
VOLUME_ADJUSTMENT = 0.9 # Scale from 0.0 (silent) to 1.0 (full programmed amplitude)
                        # This will scale the BASE_MAX_AMPLITUDE

BASE_MAX_AMPLITUDE = 110 # Internal max amplitude before VOLUME_ADJUSTMENT
                         # (0-127 for 8-bit centered at 128)

# Main Tone (Rising Pitch)
MAIN_START_FREQ = 300    # Hz - Start of the rising tone
MAIN_END_FREQ = 600     # Hz - End of the rising tone (e.g., an octave higher)
MAIN_SINE_MIX = 0.7      # Mix for the main rising sine wave

# Shimmer/Harmony Tone (Adds richness)
# This could be a fixed frequency or slightly detuned/slower rising one
SHIMMER_FREQ_OFFSET = 5  # Hz - Offset from the main frequency for a slight chorus/shimmer
                         # If 0, it will be in unison, can make it negative too.
# Or, for a fixed harmony:
# SHIMMER_FIXED_FREQ = 900 # Hz (e.g. a fifth above the start, or just a pleasant tone)
SHIMMER_SINE_MIX = 0.4   # Mix for the shimmer/harmony sine wave

# Subtle Noise (Optional, for a bit of "energy" or "sparkle")
NOISE_MIX = 0.05         # Very subtle noise, if any (0.0 to 1.0)

# Envelope (How the sound's loudness changes over time)
ATTACK_DURATION_RATIO = 0.1 # Percentage of DURATION for fade-in (e.g., 0.1 = 10%)
DECAY_RATE = 4.0            # How quickly the sound fades out after the attack phase
                            # Lower value = slower fade

OUTPUT_FILENAME = "res/shield_ready.wav"
# ------------------------------------

# Ensure the 'res' directory exists
if not os.path.exists("res"):
    os.makedirs("res")
    print("Created 'res' directory.")

# Calculate effective max amplitude
effective_max_amplitude = int(BASE_MAX_AMPLITUDE * VOLUME_ADJUSTMENT)
if not (0 <= effective_max_amplitude <= 127):
    print(f"Warning: Effective MAX_AMPLITUDE ({effective_max_amplitude}) is outside the ideal 0-127 range. Clamping might occur.")
    effective_max_amplitude = max(0, min(127, effective_max_amplitude))


# Calculate total number of samples
num_samples = int(DURATION * SAMPLE_RATE)
attack_samples = int(num_samples * ATTACK_DURATION_RATIO)
decay_samples = num_samples - attack_samples

# Generate audio data samples
audio_data = bytearray()

print(f"Generating {num_samples} samples for '{OUTPUT_FILENAME}' (Volume: {VOLUME_ADJUSTMENT*100:.0f}%)")

for i in range(num_samples):
    # Calculate time in seconds for this sample
    t = float(i) / SAMPLE_RATE

    # Calculate overall progress through the sound (0.0 to 1.0)
    overall_progress = float(i) / num_samples

    # 1. Calculate Amplitude Envelope (Attack and Decay)
    current_envelope_value = 0.0
    if i < attack_samples:
        # Attack phase: Linear ramp up
        if attack_samples > 0:
            current_envelope_value = float(i) / attack_samples
        else: # Edge case: no attack phase
            current_envelope_value = 1.0
    else:
        # Decay phase: Exponential decay
        # Progress within the decay phase (0.0 to 1.0)
        if decay_samples > 0:
            progress_in_decay = float(i - attack_samples) / decay_samples
            current_envelope_value = math.exp(-DECAY_RATE * progress_in_decay)
        else: # Edge case: no decay phase (sound ends abruptly after attack)
            current_envelope_value = 1.0 # Or 0.0 if you want instant cut-off

    current_master_amplitude = effective_max_amplitude * current_envelope_value

    # 2. Generate Main Rising Tone
    #    Linear sweep for frequency
    main_current_freq = MAIN_START_FREQ + (MAIN_END_FREQ - MAIN_START_FREQ) * overall_progress
    main_sine_value = math.sin(2.0 * math.pi * main_current_freq * t)

    # 3. Generate Shimmer/Harmony Tone
    # Option 1: Shimmer based on main frequency + offset
    shimmer_current_freq = main_current_freq + SHIMMER_FREQ_OFFSET
    # Option 2: Fixed frequency (uncomment SHIMMER_FIXED_FREQ and use it here)
    # shimmer_current_freq = SHIMMER_FIXED_FREQ
    shimmer_sine_value = math.sin(2.0 * math.pi * shimmer_current_freq * t)


    # 4. Generate Noise Component (Optional)
    noise_value = (random.random() * 2.0 - 1.0) if NOISE_MIX > 0 else 0.0

    # 5. Mix components
    #    The individual mix factors should ideally sum to <= 1.0 if no further normalization is done.
    #    Or, ensure that the combined signal * current_master_amplitude stays within byte range.
    mixed_signal_unscaled = (main_sine_value * MAIN_SINE_MIX) + \
                            (shimmer_sine_value * SHIMMER_SINE_MIX) + \
                            (noise_value * NOISE_MIX)

    # Ensure mixed_signal_unscaled is roughly within -1 to 1 before applying master amplitude
    # This step is a simple safeguard, more robust normalization might be needed for complex mixes.
    # A simple way to handle potential overdrive from mixing:
    total_mix_contribution = MAIN_SINE_MIX + SHIMMER_SINE_MIX + NOISE_MIX
    if total_mix_contribution > 1.0: # Only normalize if sum of mixes is > 1
         mixed_signal_unscaled /= total_mix_contribution


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