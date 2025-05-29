import wave
import math
import struct
import os
import random

# --- Parameters for the Turbo Jet Sound ---
SAMPLE_RATE = 13300  # Hz
DURATION = 0.50      # Seconds (Short burst)

# Volume Control
VOLUME_ADJUSTMENT = 0.9 # Scale from 0.0 (silent) to 1.0 (full programmed amplitude)
                        # This will scale the BASE_MAX_AMPLITUDE

BASE_MAX_AMPLITUDE = 115 # Internal max amplitude before VOLUME_ADJUSTMENT
                         # (0-127 for 8-bit centered at 128)

# Main Thrust Tone (Slightly falling pitch for a quick burst feel)
THRUST_START_FREQ = 450  # Hz - Initial pitch of the roar
THRUST_END_FREQ = 200    # Hz - Pitch at the end of the burst
THRUST_SINE_MIX = 0.5    # Mix for the main thrust sine wave
# Power for frequency sweep progress (e.g., progress**1.5 makes it drop faster initially)
FREQUENCY_SWEEP_POWER = 1.5

# Noise Component (The "jet wash" or "whoosh")
NOISE_MIX = 0.7          # Mix for the noise component (quite high for a jet)
# Optional: Filter noise - for simplicity, we'll use white noise,
# but you could implement a simple low-pass for a deeper rumble.

# Envelope (How the sound's loudness changes over time)
ATTACK_DURATION_RATIO = 0.08 # Percentage of DURATION for fade-in (e.g., 0.08 = 8% -> very quick)
DECAY_RATE = 8.0             # How quickly the sound fades out after the attack phase
                             # Higher value = faster fade for a short burst

OUTPUT_FILENAME = "res/turbo_jet.wav"
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
# Ensure decay_samples is calculated correctly even if attack_samples is num_samples
decay_samples = max(0, num_samples - attack_samples)


# Generate audio data samples
audio_data = bytearray()

print(f"Generating {num_samples} samples for '{OUTPUT_FILENAME}' (Volume: {VOLUME_ADJUSTMENT*100:.0f}%)")

for i in range(num_samples):
    # Calculate time in seconds for this sample
    t = float(i) / SAMPLE_RATE

    # Calculate overall progress through the sound (0.0 to 1.0)
    overall_progress = float(i) / num_samples if num_samples > 0 else 0

    # 1. Calculate Amplitude Envelope (Attack and Decay)
    current_envelope_value = 0.0
    if i < attack_samples:
        # Attack phase: Linear ramp up
        if attack_samples > 0:
            current_envelope_value = float(i) / attack_samples
        else: # Edge case: no attack phase (or DURATION is so short attack_samples is 0)
            current_envelope_value = 1.0
    else:
        # Decay phase: Exponential decay
        # Progress within the decay phase (0.0 to 1.0)
        if decay_samples > 0:
            progress_in_decay = float(i - attack_samples) / decay_samples
            current_envelope_value = math.exp(-DECAY_RATE * progress_in_decay)
        else: # Sound ends immediately after attack if no decay samples
            current_envelope_value = 1.0 # Or 0.0 for immediate cut if that's intended


    current_master_amplitude = effective_max_amplitude * current_envelope_value

    # 2. Generate Main Thrust Tone
    #    Frequency sweep progress can be non-linear
    freq_progress = overall_progress ** FREQUENCY_SWEEP_POWER
    current_thrust_freq = THRUST_START_FREQ + (THRUST_END_FREQ - THRUST_START_FREQ) * freq_progress
    # Ensure frequency doesn't go too low
    current_thrust_freq = max(20.0, current_thrust_freq)
    thrust_sine_value = math.sin(2.0 * math.pi * current_thrust_freq * t) if THRUST_SINE_MIX > 0 else 0.0

    # 3. Generate Noise Component
    noise_value = (random.random() * 2.0 - 1.0) if NOISE_MIX > 0 else 0.0

    # 4. Mix components
    mixed_signal_unscaled = (thrust_sine_value * THRUST_SINE_MIX) + \
                            (noise_value * NOISE_MIX)

    # Normalize if combined mix factors are high (basic safeguard)
    total_mix_contribution = THRUST_SINE_MIX + NOISE_MIX
    if total_mix_contribution > 1.0:
         mixed_signal_unscaled /= total_mix_contribution


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
        wf.setnchannels(1)
        wf.setsampwidth(1)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_data)
    print(f"Successfully generated {OUTPUT_FILENAME}!")
except Exception as e:
    print(f"Error writing WAV file: {e}")