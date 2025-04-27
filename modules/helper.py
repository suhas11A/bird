import math, random
import pygame # type: ignore

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

def draw_rounded_image_with_border(screen, image, rect, border_color=(255, 0, 0), border_thickness=6, radius=25):
    # Step 1: Prepare sizes
    width, height = rect.size
    border_rect = pygame.Rect(0, 0, width, height)

    # Step 2: Create transparent surface with alpha
    final_surf = pygame.Surface((width, height), pygame.SRCALPHA)

    # Step 3: Draw border (filled rounded rect)
    pygame.draw.rect(final_surf, border_color, border_rect, border_radius=radius)

    # Step 4: Create masked image (with transparency outside corners)
    mask = pygame.Surface((width - 2 * border_thickness, height - 2 * border_thickness), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=radius - border_thickness)

    # Step 5: Prepare scaled image and apply mask
    image = pygame.transform.smoothscale(image, mask.get_size()).convert_alpha()
    image.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    # Step 6: Blit masked image onto border surface, offset by border_thickness
    final_surf.blit(image, (border_thickness, border_thickness))

    # Step 7: Blit to screen
    screen.blit(final_surf, rect.topleft)