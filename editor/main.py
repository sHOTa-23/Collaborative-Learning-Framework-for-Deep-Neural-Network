
import pygame
from prediction import Prediction
from editor import Editor

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption("Text Editor")
    done = False
    clock = pygame.time.Clock()
    editor = Editor()
    prediction = Prediction()
    while not done:
        done = editor.process_events(prediction)
        editor.run_logic()
        editor.display_frame(screen)
        prediction.render(screen)
        clock.tick(20)

    pygame.quit()

if __name__ == '__main__':
    main()
