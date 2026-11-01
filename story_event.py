import random

from button import Button


class Event:
    '''Display a story event and handle the player's choice.'''
    def __init__(self, data):
        '''Load event data and create buttons for shuffled options.'''

        self.title = data["title"]
        self.background = data["background"]
        self.story = data["story"]

        self.options = data["options"].copy()
        random.shuffle(self.options)
        self.buttons = []

        self.selected_option = None

        y = 330

        for option in self.options:
            button = Button(
                70, y, 660, 90, option["text"]
            )
            self.buttons.append(button)
            y += 95

    def handle_click(self, position):
        '''Record the selected option and prevent further changes.'''
        if self.selected_option is not None:
            return

        for index in range(len(self.buttons)):
            if self.buttons[index].is_clicked(position):
                self.selected_option = self.options[index]
                break

    def draw(self, screen, title_font, font):
        '''Display the story and choices, or the selected outcome.'''
        title_image = title_font.render(
            self.title, True, (255, 255, 255)
        )
        title_rect = title_image.get_rect(center=(400, 100))
        screen.blit(title_image, title_rect)

        if self.selected_option is None:
            lines = self.story
        else:
            lines = self.selected_option["result"]

        y = 180

        for line in lines:
            image = font.render(line, True, (255, 255, 255))
            screen.blit(image, (50, y))
            y += 35

        if self.selected_option is None:
            for button in self.buttons:
                button.draw(screen, font)