import pygame

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
MARGIN_TOP = 50
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)

class Editor(object):
    def __init__(self):
        self.text = ""
        self.font = pygame.font.SysFont("Calibri",25,True,False) 
        self.text_list = []
        

    def process_events(self):
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    print("AAAAAAAA")
                    if len(self.text) > 1:
                        self.text = self.text[:len(self.text)-1]
                    else:
                        self.text = ""
                elif event.key == pygame.K_RETURN:
                    self.add_new_line()
                else:
                    self.text += event.unicode
                

        return False

    def add_new_line(self):
        self.text_list.append(self.text)
        self.text = ""

    def run_logic(self):
        size = self.font.size("a")
        letter_width = size[0]
        size = self.font.size(self.text)
        width = size[0]
        total_width = width + letter_width
        if total_width > SCREEN_WIDTH:
            self.add_new_line()

    def display_frame(self,screen):
        screen.fill(WHITE)
        size = self.font.size("abc")
        height = size[1] + 2
        for index, item in enumerate(self.text_list):
            label = self.font.render(item,True,BLACK)
            screen.blit(label,(0, MARGIN_TOP + height * index))

        t_h = len(self.text_list) * height
        new_line = self.font.render(self.text,True,BLACK)
        screen.blit(new_line,(0,MARGIN_TOP + t_h))
        width = new_line.get_width()
        pygame.draw.line(screen, RED, [width,MARGIN_TOP + t_h], [width,MARGIN_TOP + t_h + height], 3)
        
        pygame.display.flip()
