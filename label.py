import pygame
class Label:
    def __init__(self, rect, text,text_color,background_color):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.bgcolor = background_color
        self.font_color = text_color
        # Рассчитываем размер шрифта в зависимости от высоты
        self.font = pygame.font.Font(None, self.rect.height - 4)
        self.rendered_text = None
        self.rendered_rect = None


    def render(self, surface):
        if self.bgcolor!=-1: surface.fill(self.bgcolor, self.rect)
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 2, centery=self.rect.centery)
        surface.blit(self.rendered_text, self.rendered_rect)