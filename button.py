import pygame


class Button:
    """Represent a clickable image button with a text label."""

    def __init__(self, x, y, width, height, text):
        """Load the button image and set its size and label."""
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = (92, 74, 170)

        image = pygame.image.load(
            "images/button_normal.png"
        ).convert_alpha()

        # Remove transparent margins around the button.
        visible_area = image.get_bounding_rect()
        image = image.subsurface(visible_area).copy()

        self.image = pygame.transform.smoothscale(
            image, (width, height)
        )

        # Create a brighter image for mouse hover.
        self.hover_image = self.image.copy()
        self.hover_image.fill(
            (25, 25, 25),
            special_flags=pygame.BLEND_RGB_ADD
        )

    def draw(self, screen, font):
        """Draw the image, hover effect, status outline, and label."""
        mouse_position = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_position):
            screen.blit(self.hover_image, self.rect)
        else:
            screen.blit(self.image, self.rect)

        # Preserve color feedback for ticket success and failure.
        if self.color != (92, 74, 170):
            pygame.draw.rect(
                screen,
                self.color,
                self.rect,
                width=3,
                border_radius=14
            )

        text_image = font.render(
            self.text, True, (255, 255, 255)
        )
        text_rect = text_image.get_rect(
            center=self.rect.center
        )

        screen.blit(text_image, text_rect)

    def is_clicked(self, position):
        """Return whether the position is inside the button."""
        return self.rect.collidepoint(position)