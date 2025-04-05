import pygame # type: ignore
import sys

pygame.init()

# Define window (screen) size and logical drawing surface size.
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600      # Actual window size
LOGICAL_WIDTH, LOGICAL_HEIGHT = 600, 1200     # Your drawing resolution

# Create the main display and a logical drawing surface.
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
logical_surface = pygame.Surface((LOGICAL_WIDTH, LOGICAL_HEIGHT))

running = True
while running:
    # --- Event Handling ---
    events = pygame.event.get()
    if events:
        print(events)
    for event in events:
        if event.type == pygame.QUIT:
            running = False

        # Process mouse clicks
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get mouse position on the actual window
            mouse_x, mouse_y = event.pos

            # Calculate scaling factors
            scale_x = LOGICAL_WIDTH / WINDOW_WIDTH
            scale_y = LOGICAL_HEIGHT / WINDOW_HEIGHT

            # Convert mouse coordinates to logical coordinates
            logical_mouse_x = mouse_x * scale_x
            logical_mouse_y = mouse_y * scale_y

            print(f"Mouse clicked at window: ({mouse_x}, {mouse_y}) -> logical: ({logical_mouse_x:.2f}, {logical_mouse_y:.2f})")

    # --- Drawing on the logical surface ---
    # For example, fill the background
    logical_surface.fill((50, 50, 50))  # dark gray

    # (Draw your game objects on logical_surface here)
    # e.g., draw a circle at a logical position:
    pygame.draw.circle(logical_surface, (255, 0, 0), (300, 600), 50)

    # --- Scaling the logical surface to the window ---
    scaled_surface = pygame.transform.scale(logical_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(scaled_surface, (0, 0))
    pygame.display.flip()

pygame.quit()
sys.exit()