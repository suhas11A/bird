import math, random

def smooth_step(t):
    return t*t*(3 - 2*t)     ################################

def value_noise_1d(t, seed=0):
    i0 = math.floor(t)     ################################
    i1 = i0 + 1     ################################
    r0 = random.Random(seed + i0).uniform(-1, 1)     ################################
    r1 = random.Random(seed + i1).uniform(-1, 1)     ################################
    f = t - i0     ################################
    return r0 + (r1 - r0) * smooth_step(f)     ################################

def fractal_noise_1d(t, seed=0, octaves=4, lacunarity=2.0, gain=0.5):
    total = 0.0     ################################
    amplitude = 1.0     ################################
    frequency = 1.0     ################################
    for _ in range(octaves):     ################################
        total += value_noise_1d(t * frequency, seed) * amplitude     ################################
        amplitude *= gain     ################################
        frequency *= lacunarity     ################################
    norm = (1 - gain**octaves) / (1 - gain)     ################################
    return total / norm     ################################