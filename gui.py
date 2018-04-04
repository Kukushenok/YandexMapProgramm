from textbox import TextBox
import pygame
class GUI:
    def __init__(self):
        self.elements = []
        self.text_boxes = []
        self.curr = -1

    def add_element(self, element):
        self.elements.append(element)
        if isinstance(element,TextBox):
            self.curr +=1
            self.text_boxes.append(element)

    def render(self, surface):
        for element in self.elements:
            render = getattr(element, "render", None)
            if callable(render):
                element.render(surface)

    def update(self):
        for element in self.elements:
            update = getattr(element, "update", None)
            if callable(update):
                element.update()
        if self.curr != -1 and self.text_boxes[self.curr].active == False:
            self.curr = -1
        for tb in range(len(self.text_boxes)):
            if self.curr == -1 and self.text_boxes[tb].active == True:
                self.curr = tb
            if self.text_boxes[tb].active == True and tb != self.curr:
                self.text_boxes[tb].active = False


    def get_event(self, event):
        for element in self.elements:
            get_event = getattr(element, "get_event", None)
            if callable(get_event):
                element.get_event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            self.curr +=1
            self.curr = self.curr%len(self.text_boxes)
            self.text_boxes[self.curr].active = True


