import pygame
import numpy as np

pygame.init()

#define the screen dimension and add a dampening factor.
width, height = 400, 400
scale = 1  #use this scale factor to improve the performance of the algorithm. it is currently '1'.
dampening = 0.99 #this seems to be the best value. the ripples are moving quickly even when the dampening value is 0.90.

#initiating the pygame mixer.
pygame.mixer.init()
pygame.mixer.music.load("/location.mp3")  #add your music file path.
pygame.mixer.music.play(-1) #this makes the track to play and repeat indefinately.

#creating and adding a title to the screen.
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Can you hear the music?")

#initiating two 2D arrays called current and buffer, which are the size of the screen.
buffer_width, buffer_height = width // scale, height // scale
current = np.zeros((buffer_height, buffer_width), dtype=np.float32)
previous = np.zeros((buffer_height, buffer_width), dtype=np.float32)

#this function consiqutively updates the buffer values.
def update_buffers():
    global current, previous
    current[1:-1, 1:-1] = (previous[:-2, 1:-1] +
                           previous[2:, 1:-1] +
                           previous[1:-1, :-2] +
                           previous[1:-1, 2:]) / 2 - current[1:-1, 1:-1]
    current *= dampening

#the array manipulations are displayed here with a scale factor.
def display_buffer():
    scaled_buffer = np.repeat(np.repeat(current, scale, axis=0), scale, axis=1)
    surface = pygame.surfarray.make_surface(scaled_buffer)
    screen.blit(surface, (0, 0))
    pygame.display.flip()

#this is the main loop.
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            #x, y = pygame.mouse.get_pos() #for some reason this coordinate seeking command makes the simulation run faster.
            buffer_x, buffer_y = x // scale, y // scale
            if 0 <= buffer_x < buffer_width and 0 <= buffer_y < buffer_height:
                previous[buffer_x, buffer_y] = 2500
    update_buffers()
    display_buffer()
    previous, current = current, previous

#quitting functions.
pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()