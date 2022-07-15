from editor import WHITE,BLACK,RED
from editor import SCREEN_HEIGHT, SCREEN_WIDTH
import pygame
from random import randint

NUMBER_OF_PREDICTIONS = 5
PREDICTIONS_HEIGHT = 45
CELL_WIDTH = SCREEN_WIDTH / NUMBER_OF_PREDICTIONS
RANDOM_WORDS = ["painter", "sector", "reproduction", "seller", "rape", "easy", "build", "eject", "announcement", "digress", "recover", "adviser", "speech", "crackpot", "frown", "sin", "the", "and", "custody", "middle", "combine"]

class Prediction:
    def __init__(self) -> None:
        self.predictions = ["A", "ABCDEFGHIJKLMNOPQRST", "BBBBB", "GGGGG", "ASDASDAS", "GSERYRETYRET"]
        self.font = pygame.font.SysFont("Calibri",22,True,False)


    def render(self, screen):
        pygame.draw.line(screen, RED, [0, 0], [SCREEN_WIDTH,0], 2)
        pygame.draw.line(screen, RED, [0, PREDICTIONS_HEIGHT], [SCREEN_WIDTH,PREDICTIONS_HEIGHT], 2)

        x = CELL_WIDTH

        for i in range(1, NUMBER_OF_PREDICTIONS):
            pygame.draw.line(screen, RED, [x, 0], [x,PREDICTIONS_HEIGHT], 2)
            x += CELL_WIDTH

        # render predicted words
        for i in range(len(self.predictions)):
            prediction = self.predictions[i]
            x = CELL_WIDTH * i + (CELL_WIDTH) / 2

            size = self.font.size("a")
            letter_width = size[0]
            size = self.font.size(prediction)
            width = size[0]
            total_width = width + letter_width
            if total_width > CELL_WIDTH:
                prediction = prediction[ : int(CELL_WIDTH // letter_width) - 6]
                prediction += "..."

            txt = self.font.render(prediction, True, BLACK)
            txt_rect = txt.get_rect(center=(x, PREDICTIONS_HEIGHT/2))
            screen.blit(txt, txt_rect)

        pygame.display.flip()
    
    def fill_predictions(self):
        self.predictions = []
        for i in range(len(RANDOM_WORDS)): 
            self.predictions.append(RANDOM_WORDS[randint(0, len(RANDOM_WORDS) - 1)])
