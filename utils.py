import pygame
def get_frame(sheet, frame, width, height, SCALE_FACTOR):
    rect = pygame.Rect(frame * width, 0, width, height)
    image = pygame.Surface(rect.size, pygame.SRCALPHA)
    image.blit(sheet, (0, 0), rect)
    scaled_image = pygame.transform.scale(image, (width * SCALE_FACTOR, height * SCALE_FACTOR))
    return scaled_image

