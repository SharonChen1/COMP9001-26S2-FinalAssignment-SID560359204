import pygame

from button import Button


class TrainGame:
    '''Manage a timed challenge to squeeze onto a crowded train.'''
    def __init__(self):
        '''Create the start button and set the challenge difficulty.'''
        self.start_button = Button(
            250, 370, 300, 60, "Start Boarding"
        )

        self.time_limit = 10000
        self.push_amount = 5
        self.crowd_resistance = 12

        self.reset()

    def reset(self):
        '''Reset boarding progress, timers, and keyboard state.'''
        self.status = "ready"
        self.progress = 0.0
        self.start_time = None
        self.last_update = None
        self.space_down = False

    def handle_click(self, position):
        '''Start the countdown when the start button is clicked.'''
        if self.status == "ready":
            if self.start_button.is_clicked(position):
                self.status = "playing"
                self.start_time = pygame.time.get_ticks()
                self.last_update = self.start_time

    def update(self):
        '''Reduce progress over time and check the boarding deadline.'''
        if self.status != "playing":
            return

        current_time = pygame.time.get_ticks()

        if current_time - self.start_time >= self.time_limit:
            self.status = "failed"
            return

        elapsed = (current_time - self.last_update) / 1000

        self.progress = max(
            0,
            self.progress - self.crowd_resistance * elapsed
        )

        self.last_update = current_time

    def handle_key(self, event):
        '''Increase progress for each separate Space press.'''
        if event.key != pygame.K_SPACE:
            return

        if event.type == pygame.KEYUP:
            self.space_down = False
            return

        self.update()

        if event.type != pygame.KEYDOWN:
            return

        if self.space_down:
            return

        self.space_down = True

        if self.status == "playing":
            self.progress = min(
                100,
                self.progress + self.push_amount
            )

            if self.progress >= 100:
                self.status = "success"

    def draw_text(self, screen, font, text, y, color):
        '''Draw horizontally centered text at the given vertical position.'''
        image = font.render(text, True, color)
        position = image.get_rect(center=(400, y))
        screen.blit(image, position)

    def draw(self, screen, title_font, font):
        '''Display instructions, the countdown, progress, and the outcome.'''
        white = (255, 255, 255)
        yellow = (255, 220, 90)
        green = (130, 230, 170)
        red = (255, 150, 150)

        self.draw_text(
            screen, title_font,
            "Squeeze onto the High-Speed Train!",
            100, white
        )

        if self.status == "ready":
            self.draw_text(
                screen, font,
                "The platform is packed. The doors are closing soon!",
                185, white
            )
            self.draw_text(
                screen, font,
                "Tap SPACE repeatedly to push through the crowd.",
                225, white
            )
            self.draw_text(
                screen, font,
                "Fill the bar within 10 seconds to get aboard.",
                265, white
            )
            self.draw_text(
                screen, font,
                "Keep tapping! The crowd pushes you back.",
                305, yellow
            )

            self.start_button.draw(screen, font)
            return

        if self.status == "playing":
            elapsed = pygame.time.get_ticks() - self.start_time

            remaining = max(
                0,
                (self.time_limit - elapsed) / 1000
            )

            self.draw_text(
                screen, font,
                f"Doors close in: {remaining:.1f} seconds",
                185, yellow
            )
            self.draw_text(
                screen, font,
                "Tap SPACE! Holding it down does not count.",
                230, white
            )

        elif self.status == "success":
            self.draw_text(
                screen, font,
                "You squeezed aboard just before the doors closed!",
                185, green
            )
            self.draw_text(
                screen, font,
                "Next stop: the concert venue!",
                230, white
            )

        elif self.status == "failed":
            self.draw_text(
                screen, font,
                "The doors closed before you could get aboard.",
                185, red
            )
            self.draw_text(
                screen, font,
                "The next train will arrive after the concert ends.",
                230, white
            )
            self.draw_text(
                screen, font,
                "You missed the concert!",
                400, red
            )

        # Progress bar background.
        bar = pygame.Rect(100, 290, 600, 45)
        pygame.draw.rect(screen, (45, 48, 65), bar)

        # Filled part of the progress bar.
        fill = pygame.Rect(
            bar.x,
            bar.y,
            round(bar.width * self.progress / 100),
            bar.height
        )
        pygame.draw.rect(screen, (65, 190, 135), fill)

        # Progress bar border.
        pygame.draw.rect(screen, white, bar, 2)

        self.draw_text(
            screen, font,
            f"Boarding progress: {self.progress:.0f}%",
            365, white
        )