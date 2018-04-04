from label import Label
import pygame
class TextBox(Label):
    def __init__(self, rect, text,max_len=None):
        super().__init__(rect, text,pygame.Color("white"),pygame.Color("gray"))
        self.active = True
        self.blink = True
        self.blink_timer = 0
        self.delta = 0
        self.max_len = max_len
        self.executed = False

    def execute(self):
        self.executed = True

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and self.active:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.execute()
            elif event.key == pygame.K_BACKSPACE:
                if len(self.text) > 0:
                    c = self.delta + len(self.text)
                    a =  self.text[:c-1]
                    b = self.text[c:]
                    self.text = a + b
            elif event.key == pygame.K_TAB:pass
            elif event.key == pygame.K_LEFT:
                if self.delta < len(self.text):
                    self.delta -= 1
            elif event.key == pygame.K_RIGHT:
                if self.delta < 0:
                    self.delta +=1
                print(self.delta)
            else:
                c = self.delta + len(self.text)
                a = self.text[:c]+event.unicode
                b = self.text[c:]
                self.text = a + b
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)
            was = None
            id = 0
            if self.active and self.text:
                for i in range(len(self.text)+1):
                    self.rendered_text = self.font.render(self.text[:i], 1, self.font_color)
                    d = self.rendered_text.get_rect(x=self.rect.x + 2, centery=self.rect.centery)
                    if not was or abs(d.width+d.x - event.pos[0]) < abs(was.width+was.x-event.pos[0]): was,id = d,i
                self.delta = -(len(self.text)-id)

    def update(self):
        if pygame.time.get_ticks() - self.blink_timer > 200:
            self.blink = not self.blink
            self.blink_timer = pygame.time.get_ticks()

    def render(self, surface):
        surface.fill(self.bgcolor, self.rect)
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 2, centery=self.rect.centery)

        while (self.rect.width <= self.rendered_rect.width) if not self.max_len else (len(self.text) > self.max_len):
            self.text = self.text[:-1]
            self.rendered_text = self.font.render(self.text, 1, self.font_color)
            self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 2, centery=self.rect.centery)
        if self.blink and self.active:
            self.rer_text = self.font.render(self.text[:self.delta] if self.delta != 0 else self.text, 1,
                                             self.font_color)
            self.p_rect = self.rer_text.get_rect(x=self.rect.x + 2, centery=self.rect.centery)
            pygame.draw.line(surface, pygame.Color("black"),
                             (self.p_rect.right, self.p_rect.top + 2),
                             (self.p_rect.right, self.p_rect.bottom - 2))
        surface.blit(self.rendered_text, self.rendered_rect)

