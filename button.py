from label import Label
import pygame
class Button(Label):
    def __init__(self, rect, text):
        super().__init__(rect, text,pygame.Color("red"),pygame.Color("blue"))
        self.bgcolor = pygame.Color("blue")
        # при создании кнопка не нажата
        self.pressed = False

    def render(self, surface):
        surface.fill(self.bgcolor, self.rect)
        self.rendered_rect = pygame.Rect(self.rect[0],self.rect[1],self.rect[2]+1,self.rect[3])
        self.rendered_text = None
        self.text += "!"
        iterates = 0
        while self.rendered_rect[2] > self.rect[2]:
            self.text = self.text[:-1]
            self.text+="..."
            self.rendered_text = self.font.render(self.text, 1, self.font_color)
            self.text = self.text[:-3]
            self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 2, centery=self.rect.centery)
            iterates+=1
        if iterates == 1: self.rendered_text = self.font.render(self.text, 1, self.font_color)
        if not self.pressed:
            color1 = pygame.Color("white")
            color2 = pygame.Color("black")
            self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 5, centery=self.rect.centery)
        else:
            color1 = pygame.Color("black")
            color2 = pygame.Color("white")
            self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 7, centery=self.rect.centery + 2)

        # рисуем границу
        pygame.draw.rect(surface, color1, self.rect, 2)
        pygame.draw.line(surface, color2, (self.rect.right - 1, self.rect.top), (self.rect.right - 1, self.rect.bottom), 2)
        pygame.draw.line(surface, color2, (self.rect.left, self.rect.bottom - 1),
                         (self.rect.right, self.rect.bottom - 1), 2)
        # выводим текст
        surface.blit(self.rendered_text, self.rendered_rect)

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.pressed = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.pressed = False
        elif event.type == pygame.MOUSEMOTION and self.rect.collidepoint(event.pos):
            self.bgcolor = pygame.Color("lightblue")
        elif event.type == pygame.MOUSEMOTION and not self.rect.collidepoint(event.pos):
            self.bgcolor = pygame.Color("blue")