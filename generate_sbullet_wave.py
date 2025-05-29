import wave
import math
import struct
import os
import random

# --- Parameters for the Triple-Canon Spread Shot ---
SAMPLE_RATE = 13300  # Hz
NUM_SHOTS = 3        # Number of shots in the burst

# Timing
SHOT_DURATION = 0.12  # Seconds (Duration of a single shot's sound)
DELAY_BETWEEN_SHOTS = 0.04 # Seconds (Time between the start of each shot)

# Volume Control
VOLUME_ADJUSTMENT = 0.9 # Scale from 0.0 (silent) to 1.0 (full programmed amplitude)
BASE_MAX_AMPLITUDE = 100 # Max amplitude for a single shot before volume adjustment.
                         # Overall amplitude can exceed this due to overlapping shots.

# Individual Shot Characteristics
SHOT_START_FREQ = 300   # Hz - Initial "crack" or "zap" of a shot
SHOT_END_FREQ = 60      # Hz - Frequency at the end of the shot's sweep
SHOT_FREQ_SWEEP_POWER = 1.2 # Power for frequency sweep (higher = faster drop initially)

SINE_MIX = 0.6           # Mix for the tonal part of the shot
NOISE_MIX = 0.5          # Mix for the noisy part of the shot (adds "energy")

SHOT_DECAY_RATE = 15.0   # How quickly each individual shot fades (higher = faster)

# Variation between shots (adds to the "spread" feel)
PITCH_VARIATION_HZ = 100 # Max +/- Hz variation for start/end frequencies of each shot

OUTPUT_FILENAME = "res/sbullet.wav"
# ------------------------------------

# Ensure the 'res' directory exists
if not os.path.exists("res"):
    os.makedirs("res")
    print("Created 'res' directory.")

# Calculate total duration based on number of shots and delay
# The last shot starts at (NUM_SHOTS - 1) * DELAY_BETWEEN_SHOTS
# and lasts for SHOT_DURATION
total_duration = ((NUM_SHOTS - 1) * DELAY_BETWEEN_SHOTS) + SHOT_DURATION
num_samples = int(total_duration * SAMPLE_RATE)

# Calculate effective max amplitude for scaling final output
# This is a bit of a heuristic as shots overlap.
# Max possible combined amplitude could be NUM_SHOTS * BASE_MAX_AMPLITUDE,
# but usually it's less due to decay and phase.
# We'll scale the output based on BASE_MAX_AMPLITUDE and VOLUME_ADJUSTMENT.
effective_base_amplitude = int(BASE_MAX_AMPLITUDE * VOLUME_ADJUSTMENT)

audio_data = bytearray()

print(f"Generating {num_samples} samples for '{OUTPUT_FILENAME}' (Volume: {VOLUME_ADJUSTMENT*100:.0f}%)")
print(f"Total duration: {total_duration:.3f}s")

shot_start_times = [s * DELAY_BETWEEN_SHOTS for s in range(NUM_SHOTS)]

# Pre-calculate randomized frequencies for each shot to ensure consistency
shot_params = []
for s_idx in range(NUM_SHOTS):
    freq_offset_start = random.uniform(-PITCH_VARIATION_HZ, PITCH_VARIATION_HZ)
    freq_offset_end = random.uniform(-PITCH_VARIATION_HZ, PITCH_VARIATION_HZ) # Can be different from start offset
    shot_params.append({
        'start_freq': max(20, SHOT_START_FREQ + freq_offset_start), # Ensure freq > 0
        'end_freq': max(20, SHOT_END_FREQ + freq_offset_end)
    })


for i in range(num_samples):
    t_overall = float(i) / SAMPLE_RATE
    current_sample_value_float = 0.0 # Accumulates contributions from all active shots

    for shot_index in range(NUM_SHOTS):
        shot_start_time = shot_start_times[shot_index]
        shot_end_time = shot_start_time + SHOT_DURATION

        # Check if the current sample is within this shot's active time
        if shot_start_time <= t_overall < shot_end_time:
            t_shot = t_overall - shot_start_time # Time relative to this shot's start
            progress_shot = t_shot / SHOT_DURATION

            # 1. Amplitude for this individual shot (exponential decay)
            shot_amplitude = math.exp(-SHOT_DECAY_RATE * progress_shot)

            # 2. Frequency for this individual shot
            current_shot_start_freq = shot_params[shot_index]['start_freq']
            current_shot_end_freq = shot_params[shot_index]['end_freq']

            freq_sweep_progress = progress_shot ** SHOT_FREQ_SWEEP_POWER
            current_freq_shot = current_shot_start_freq + \
                                (current_shot_end_freq - current_shot_start_freq) * freq_sweep_progress
            current_freq_shot = max(20.0, current_freq_shot) # Ensure positive freq

            # 3. Sine wave for this shot
            sine_value_shot = math.sin(2.0 * math.pi * current_freq_shot * t_shot) if SINE_MIX > 0 else 0.0
            # Note: using t_shot for the sine wave ensures phase coherence for each shot's start

            # 4. Noise for this shot
            noise_value_shot = (random.random() * 2.0 - 1.0) if NOISE_MIX > 0 else 0.0

            # 5. Mix sine and noise for this shot, scaled by its individual amplitude
            #    The effective_base_amplitude applies to a single shot's peak.
            #    Overlapping shots will sum.
            mixed_shot_signal = (sine_value_shot * SINE_MIX) + (noise_value_shot * NOISE_MIX)

            # Normalize individual shot signal if sum of mixes > 1
            indiv_total_mix = SINE_MIX + NOISE_MIX
            if indiv_total_mix > 1.0:
                mixed_shot_signal /= indiv_total_mix

            current_sample_value_float += shot_amplitude * mixed_shot_signal
            # We don't apply effective_base_amplitude here yet, as we sum up multiple shots first.

    # Scale the combined signal by the effective_base_amplitude
    # This effective_base_amplitude acts as the target peak for a single hypothetical loudest shot.
    # If shots overlap perfectly in phase, it might exceed this, but it's a good general scaler.
    scaled_value = current_sample_value_float * effective_base_amplitude

    # Shift to 8-bit unsigned range (0-255)
    byte_value_float = 128.0 + scaled_value

    # Clamp the value
    byte_value = int(max(0.0, min(255.0, byte_value_float)))

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