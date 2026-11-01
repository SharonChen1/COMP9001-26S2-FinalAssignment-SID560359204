import random
import pygame

from button import Button

class TicketGame:
    '''Manage the ticket reaction challenge and code verification.'''
    def __init__(self):
        '''Create the ticket button and prepare the challenge.'''
        self.ticket_button = Button(
            250, 280, 300, 70, "Not on Sale Yet"
        )
        self.reset()

    def reset(self):
        '''Reset the timers, verification input, and button appearance.'''
        self.status = "waiting"
        self.message = "Wait for ticket sales to open..."
        self.reaction_time = None

        self.wait_time = random.randint(2000, 5000)
        self.start_time = pygame.time.get_ticks()
        self.sale_time = self.start_time + self.wait_time
        self.time_limit = 1000

        self.verification_code = ""
        self.player_input = ""
        self.verification_start = 0
        self.verification_limit = 8000

        self.ticket_button.text = "Not on Sale Yet"
        self.ticket_button.color = (92, 74, 170)

    def update(self):
        '''Open ticket sales and check purchase and verification deadlines.'''
        current_time = pygame.time.get_ticks()

        if self.status == "waiting":
            if current_time >= self.sale_time:
                self.status = "open"
                self.message = "Tickets are on sale! Click now!"
                self.ticket_button.text = "Buy Ticket!"
                self.ticket_button.color = (40, 150, 90)

        if self.status == "open":
            if current_time - self.sale_time > self.time_limit:
                self.status = "failed"
                self.message = "Sold out! You were too late."
                self.ticket_button.text = "Sold Out"
                self.ticket_button.color = (170, 60, 70)

        elif self.status == "verification":
            elapsed = current_time - self.verification_start

            if elapsed >= self.verification_limit:
                self.status = "failed"
                self.message = "Verification timed out! Your ticket was released."
                self.ticket_button.text = "Time Up"
                self.ticket_button.color = (170, 60, 70)

    def handle_click(self, position):
        '''Check purchase timing and start verification after a valid click.'''
        self.update()

        if not self.ticket_button.is_clicked(position):
            return

        if self.status == "waiting":
            self.status = "failed"
            self.message = "Too early! Your account was temporarily blocked."
            self.ticket_button.text = "Blocked"
            self.ticket_button.color = (170, 60, 70)

        elif self.status == "open":
            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.sale_time

            if elapsed > self.time_limit:
                self.status = "failed"
                self.message = "Sold out! You were too late."
                self.ticket_button.text = "Sold Out"
                self.ticket_button.color = (170, 60, 70)

            else:
                self.reaction_time = elapsed / 1000
                self.status = "verification"
                self.message = "A ticket is held for you. Complete verification!"

                self.verification_code = str(
                    random.randint(1000, 9999)
                )
                self.player_input = ""
                self.verification_start = current_time

    def handle_key(self, event):
        '''Handle verification digits, deletion, and code submission.'''
        # Check the timer before accepting keyboard input.
        self.update()

        if self.status != "verification":
            return

        if event.key == pygame.K_BACKSPACE:
            self.player_input = self.player_input[:-1]

        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            if self.player_input == self.verification_code:
                self.status = "success"
                self.message = "Verification passed! You got a ticket!"
                self.ticket_button.text = "Success!"
                self.ticket_button.color = (40, 150, 90)

            else:
                self.message = "Incorrect code! Try again before time runs out."
                self.player_input = ""

        elif event.unicode in "0123456789" and event.unicode != "":
            if len(self.player_input) < 4:
                self.player_input += event.unicode

    def draw_text(self, screen, font, text, y, color):
        '''Draw horizontally centered text at the given vertical position.'''
        image = font.render(text, True, color)
        position = image.get_rect(center=(400, y))
        screen.blit(image, position)

    def draw(self, screen, font):
        '''Display the challenge status, verification input, and timing.'''
        self.draw_text(
            screen,
            font,
            self.message,
            220,
            (255, 255, 255)
        )

        if self.status == "verification":
            self.draw_text(
                screen,
                font,
                f"Verification code: {self.verification_code}",
                280,
                (255, 220, 90)
            )

            # Display empty slots for digits not yet entered.
            input_display = self.player_input

            while len(input_display) < 4:
                input_display += "_"

            self.draw_text(
                screen,
                font,
                f"Your input: {input_display}",
                325,
                (255, 255, 255)
            )

            self.draw_text(
                screen,
                font,
                "Type 4 digits. Press Enter. Backspace deletes.",
                365,
                (185, 190, 210)
            )

            elapsed = (
                pygame.time.get_ticks() - self.verification_start
            )
            remaining = max(
                0,
                (self.verification_limit - elapsed) / 1000
            )

            self.draw_text(
                screen,
                font,
                f"Time left: {remaining:.1f} seconds",
                395,
                (255, 220, 90)
            )

        else:
            self.ticket_button.draw(screen, font)

            if self.status == "success":
                self.draw_text(
                    screen,
                    font,
                    f"Reaction time: {self.reaction_time:.3f} seconds",
                    390,
                    (255, 255, 255)
                )