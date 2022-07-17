import pygame
from prediction import Prediction
import sys
sys.path.insert(0,"..")
from Client.app_clients import AppClient
from dataset import Dataset
from editor import Editor
from model import Model
import torch.nn as nn

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

def main():
    loss = nn.MSELoss()
    app = AppClient('conf.yml',loss)
    app.run()
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption("Text Editor")
    done = False
    clock = pygame.time.Clock()
    dataset = Dataset('a.txt',3)
    model = Model('bla.pt',dataset)
    editor = Editor(model,dataset)
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
