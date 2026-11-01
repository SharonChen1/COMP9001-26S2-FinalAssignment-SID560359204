import math
import random
import pygame

from button import Button


class LuckyWheel:
    '''Manage a spinning wheel that decides the taxi journey's outcome.'''
    def __init__(self):
        '''Create the spin button and draw alternating lucky and unlucky sectors.'''
        self.font = pygame.font.Font(None, 30)

        self.spin_button = Button(
            250, 490, 300, 60, "Spin the Wheel"
        )

        self.sector_count = 12
        self.sector_angle = 360 / self.sector_count

        self.wheel_image = pygame.Surface(
            (260, 260), pygame.SRCALPHA
        )

        # Draw alternating lucky and unlucky sectors.
        for sector in range(self.sector_count):
            if sector % 2 == 0:
                color = (40, 150, 90)
            else:
                color = (170, 60, 70)

            start_angle = sector * self.sector_angle
            end_angle = start_angle + self.sector_angle

            points = [(130, 130)]

            for degree in range(
                int(start_angle), int(end_angle) + 1
            ):
                radians = math.radians(degree)

                x = 130 + 125 * math.cos(radians)
                y = 130 + 125 * math.sin(radians)

                points.append((x, y))

            pygame.draw.polygon(
                self.wheel_image, color, points
            )

            pygame.draw.lines(
                self.wheel_image,
                (255, 255, 255),
                True,
                points,
                2
            )

        pygame.draw.circle(
            self.wheel_image,
            (255, 255, 255),
            (130, 130),
            125,
            3
        )

        pygame.draw.circle(
            self.wheel_image,
            (255, 220, 90),
            (130, 130),
            12
        )

        self.reset()

    def reset(self):
        '''Reset the wheel's rotation, timer, outcome, and message.'''
        self.status = "ready"
        self.angle = 0
        self.start_time = 0
        self.duration = 3000
        self.total_rotation = 0
        self.lucky = None
        self.message = "Will the traffic clear in time?"

    def handle_click(self, position):
        '''Start spinning toward a randomly selected sector.'''
        if self.status != "ready":
            return

        if self.spin_button.is_clicked(position):
            self.status = "spinning"
            self.start_time = pygame.time.get_ticks()

            # Choose a sector, then stop safely inside it.
            target_sector = random.randrange(self.sector_count)

            target_angle = (
                target_sector * self.sector_angle
                + random.uniform(5, self.sector_angle - 5)
            )

            # Convert the target position to a rotation angle.
            final_angle = (target_angle - 270) % 360

            self.total_rotation = 1080 + final_angle
            self.message = "Good luck..."

    def update(self):
        '''Gradually slow the wheel and determine the outcome when it stops.'''
        if self.status != "spinning":
            return

        elapsed = pygame.time.get_ticks() - self.start_time
        progress = min(elapsed / self.duration, 1)

        # Gradually slow the wheel down.
        movement = 1 - (1 - progress) ** 3
        self.angle = self.total_rotation * movement

        if progress == 1:
            self.status = "finished"

            # Find the sector under the top pointer.
            pointer_angle = (270 + self.angle) % 360
            sector = int(pointer_angle / self.sector_angle)

            self.lucky = sector % 2 == 0

            if self.lucky:
                self.message = "Lucky! Traffic clears. You arrive on time!"
            else:
                self.message = "Unlucky! You miss the concert."

    def draw(self, screen):
        '''Display the rotating wheel, fixed pointer, legend, and message.'''
        message_image = self.font.render(
            self.message, True, (255, 255, 255)
        )
        message_rect = message_image.get_rect(
            center=(400, 155)
        )
        screen.blit(message_image, message_rect)

        rotated_image = pygame.transform.rotate(
            self.wheel_image, self.angle
        )
        wheel_rect = rotated_image.get_rect(
            center=(400, 335)
        )
        screen.blit(rotated_image, wheel_rect)

        # Fixed pointer at the top.
        pygame.draw.polygon(
            screen,
            (255, 220, 90),
            [(387, 193), (413, 193), (400, 215)]
        )

        legend = self.font.render(
            "Green: Lucky     Red: Unlucky",
            True,
            (255, 255, 255)
        )
        legend_rect = legend.get_rect(center=(400, 465))
        screen.blit(legend, legend_rect)

        if self.status == "ready":
            self.spin_button.draw(screen, self.font)