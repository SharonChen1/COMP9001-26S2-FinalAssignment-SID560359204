import pygame
from button import Button
from ticket_game import TicketGame
from story_event import Event
from story_data import boss_event, transport_event, help_event, ticket_swap_event, merch_event, no_merch_event
from lucky_wheel import LuckyWheel
from save_data import ENDING_TITLES, load_endings, save_endings, load_best_time, save_best_time
from train_game import TrainGame

class Game:
    '''Coordinate game screens, story events, mini-games, and saved progress.'''
    def __init__(self):
        '''Initialize Pygame, load backgrounds, and create game components.'''
        pygame.init()

        self.screen = pygame.display.set_mode((800, 600))

        self.backgrounds = {}

        image_names = [
            "menu",
            "ticket",
            "boss",
            "transport",
            "help",
            "ticket_swap",
            "merch",
            "ending_boss",
            "ending_help",
            "ending_concert",
            "failed"
        ]

        for name in image_names:
            image = pygame.image.load(
                f"images/{name}.png"
            ).convert()

            image = pygame.transform.scale(
                image, (800, 600)
            )

            self.backgrounds[name] = image

        # Darken backgrounds so white text remains readable.
        self.background_shade = pygame.Surface((800, 600))
        self.background_shade.fill((0, 0, 0))
        self.background_shade.set_alpha(140)

        pygame.display.set_caption("Can You Make It to the Concert?")

        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "menu"

        self.title_font = pygame.font.Font(None, 42)
        self.button_font = pygame.font.Font(None, 30)

        self.start_button = Button(
            250, 280, 300, 70, "Start Game"
        )
        self.collection_button = Button(
            250, 360, 300, 70, "Good Endings"
        )
        self.quit_button = Button(
            250, 440, 300, 70, "Quit"
        )

        self.ticket_game = TicketGame()
        self.train_game = TrainGame()

        self.retry_button = Button(
            80, 470, 280, 60, "Try Again"
        )
        self.back_button = Button(
            440, 470, 280, 60, "Back to Menu"
        )   

        self.continue_button = Button(
            80, 470, 280, 60, "Continue"
        )

        self.current_event = None 

        self.can_buy_merch = True

        self.bought_merch = False

        self.lucky_wheel = LuckyWheel()

        self.unlocked_endings = load_endings()

        self.best_time = load_best_time()
        self.record_checked = False

    def run(self):
        '''Run the main loop to process input, update challenges, and draw screens.'''
        while self.running:
            self.handle_events()

            if self.state == "ticket":
                self.ticket_game.update()
                self.check_ticket_record()

            elif self.state == "train":
                self.train_game.update()

            elif self.state == "wheel":
                self.lucky_wheel.update()

            self.draw()
            self.clock.tick(60)

        pygame.quit()

    def handle_events(self):
        '''Handle player input and transitions between game states.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if self.state == "ticket":
                    self.ticket_game.handle_key(event)

                elif self.state == "train":
                    self.train_game.handle_key(event)

            elif event.type == pygame.KEYUP:
                if self.state == "train":
                    self.train_game.handle_key(event)

            elif event.type == pygame.WINDOWFOCUSLOST:
                self.train_game.space_down = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.state == "menu":
                        if self.start_button.is_clicked(event.pos):
                            self.can_buy_merch = True
                            self.bought_merch = False
                            self.ticket_game.reset()
                            self.record_checked = False
                            self.state = "ticket"

                        elif self.collection_button.is_clicked(event.pos):
                            self.state = "collection"

                        elif self.quit_button.is_clicked(event.pos):
                            self.running = False

                    elif self.state == "ticket":
                        status = self.ticket_game.status

                        if status == "success":
                            if self.continue_button.is_clicked(event.pos):
                                self.current_event = Event(boss_event)
                                self.state = "story"

                            elif self.back_button.is_clicked(event.pos):
                                self.state = "menu"

                        elif status == "failed":
                            if self.retry_button.is_clicked(event.pos):
                                self.ticket_game.reset()
                                self.record_checked = False

                            elif self.back_button.is_clicked(event.pos):
                                self.state = "menu"

                        else:
                            self.ticket_game.handle_click(event.pos)

                    # Story events
                    elif self.state == "story":
                        selected = self.current_event.selected_option

                        if selected is None:
                            self.current_event.handle_click(event.pos)

                            chosen = self.current_event.selected_option

                            if chosen is not None:
                                if "spend_merch_budget" in chosen:
                                    if chosen["spend_merch_budget"]:
                                        self.can_buy_merch = False

                                if "buy_merch" in chosen:
                                    if chosen["buy_merch"]:
                                        self.bought_merch = True
                                        self.can_buy_merch = False

                                ending = chosen["next"]

                                if ending in ENDING_TITLES:
                                    if ending not in self.unlocked_endings:
                                        self.unlocked_endings.append(ending)

                                        saved = save_endings(
                                            self.unlocked_endings
                                        )

                                        if not saved:
                                            print(
                                                "This ending is unlocked "
                                                "for this session, but "
                                                "could not be saved."
                                            )

                        else:
                            if self.back_button.is_clicked(event.pos):
                                self.state = "menu"

                            elif self.continue_button.is_clicked(event.pos):
                                if selected["next"] == "transport":
                                    self.current_event = Event(
                                        transport_event
                                    )

                                elif selected["next"] == "train":
                                    self.train_game.reset()
                                    self.state = "train"

                                elif selected["next"] == "lucky_wheel":
                                    self.lucky_wheel.reset()
                                    self.state = "wheel"

                                elif selected["next"] == "help":
                                    self.current_event = Event(
                                        help_event
                                    )

                                elif selected["next"] == "ticket_swap":
                                    self.current_event = Event(
                                        ticket_swap_event
                                    )

                                elif selected["next"] == "merch":
                                    if self.can_buy_merch:
                                        self.current_event = Event(
                                            merch_event
                                        )
                                    else:
                                        self.current_event = Event(
                                            no_merch_event
                                        )                

                    # High-speed rail
                    elif self.state == "train":
                        status = self.train_game.status

                        if status in ("success", "failed"):
                            if self.back_button.is_clicked(event.pos):
                                self.state = "menu"

                            elif status == "success":
                                if self.continue_button.is_clicked(event.pos):
                                    self.current_event = Event(
                                        help_event
                                    )
                                    self.state = "story"

                        else:
                            self.train_game.handle_click(event.pos)

                    # Lucky wheel
                    elif self.state == "wheel":
                        if self.lucky_wheel.status == "finished":
                            if self.back_button.is_clicked(event.pos):
                                self.state = "menu"

                            elif self.lucky_wheel.lucky:
                                if self.continue_button.is_clicked(event.pos):
                                    self.current_event = Event(
                                        help_event
                                    )
                                    self.state = "story"

                        else:
                            self.lucky_wheel.handle_click(event.pos)

                    elif self.state == "collection":
                        if self.back_button.is_clicked(event.pos):
                            self.state = "menu"

    def draw(self):
        '''Draw the current game screen and its available buttons.'''
        self.draw_background()

        if self.state == "menu":

            title = self.title_font.render(
                "Can You Make It to the Concert?",
                True,
                (255, 255, 255)
            )
            title_rect = title.get_rect(center=(400, 170))
            self.screen.blit(title, title_rect)

            self.start_button.draw(self.screen, self.button_font)
            self.collection_button.draw(
                self.screen, self.button_font
            )
            self.quit_button.draw(self.screen, self.button_font)

        elif self.state == "ticket":
            title = self.title_font.render(
                "The Ticket Battle",
                True,
                (255, 255, 255)
            )
            title_rect = title.get_rect(center=(400, 140))
            self.screen.blit(title, title_rect)

            self.ticket_game.draw(self.screen, self.button_font)
            if self.best_time is None:
                record_text = "Personal best: No record yet"
            else:
                record_text = (
                    f"Personal best: {self.best_time:.3f} seconds"
                )

            record_image = self.button_font.render(
                record_text, True, (185, 190, 210)
            )
            record_rect = record_image.get_rect(
                center=(400, 430)
            )
            self.screen.blit(record_image, record_rect)

            status = self.ticket_game.status

            if status == "success":
                self.continue_button.draw(
                    self.screen, self.button_font
                )
                self.back_button.draw(
                    self.screen, self.button_font
                )

            elif status == "failed":
                self.retry_button.draw(
                    self.screen, self.button_font
                )
                self.back_button.draw(
                    self.screen, self.button_font
                )

        elif self.state == "story":
            self.current_event.draw(
                self.screen,
                self.title_font,
                self.button_font
            )

            if self.bought_merch:
                budget_text = "Merch: Purchased!"

            elif self.can_buy_merch:
                budget_text = "Merch budget: Available"

            else:
                budget_text = "Merch budget: Spent on transport"

            budget_image = self.button_font.render(
                budget_text, True, (185, 190, 210)
            )
            self.screen.blit(budget_image, (50, 30))            

            selected = self.current_event.selected_option

            if selected is not None:
                self.back_button.draw(
                    self.screen, self.button_font
                )

                if selected["next"] in [
                    "transport",
                    "train",
                    "lucky_wheel",
                    "help",
                    "ticket_swap",
                    "merch"
                ]:
                    self.continue_button.draw(
                        self.screen, self.button_font
                    )

        elif self.state == "train":
            self.train_game.draw(
                self.screen,
                self.title_font,
                self.button_font
            )

            if self.train_game.status in ("success", "failed"):
                self.back_button.draw(
                    self.screen, self.button_font
                )

                if self.train_game.status == "success":
                    self.continue_button.draw(
                        self.screen, self.button_font
                    )

        # Lucky wheel
        elif self.state == "wheel":
            title = self.title_font.render(
                "Lucky Test",
                True,
                (255, 255, 255)
            )
            title_rect = title.get_rect(center=(400, 90))
            self.screen.blit(title, title_rect)

            self.lucky_wheel.draw(self.screen)

            if self.lucky_wheel.status == "finished":
                self.back_button.draw(
                    self.screen, self.button_font
                )

                if self.lucky_wheel.lucky:
                    self.continue_button.draw(
                        self.screen, self.button_font
                    )

        elif self.state == "collection":
            title = self.title_font.render(
                "Good Ending Collection",
                True,
                (255, 255, 255)
            )
            title_rect = title.get_rect(center=(400, 100))
            self.screen.blit(title, title_rect)

            count = len(self.unlocked_endings)

            progress = self.button_font.render(
                f"Collected: {count} / 3",
                True,
                (185, 190, 210)
            )
            progress_rect = progress.get_rect(center=(400, 165))
            self.screen.blit(progress, progress_rect)

            y = 250

            for ending in ENDING_TITLES:
                if ending in self.unlocked_endings:
                    text = ENDING_TITLES[ending]
                    color = (130, 230, 170)
                else:
                    text = "???"
                    color = (185, 190, 210)

                image = self.button_font.render(
                    text, True, color
                )
                image_rect = image.get_rect(center=(400, y))
                self.screen.blit(image, image_rect)

                y += 65

            self.back_button.draw(
                self.screen, self.button_font
            )

        pygame.display.flip()

    def check_ticket_record(self):
        '''Check each successful ticket attempt once and save a new personal best.'''
        if self.record_checked:
            return

        if self.ticket_game.status != "success":
            return

        self.record_checked = True
        reaction_time = self.ticket_game.reaction_time

        if self.best_time is None or reaction_time < self.best_time:
            self.best_time = reaction_time

            saved = save_best_time(self.best_time)

            if not saved:
                print(
                    "The new record is available for this session, "
                    "but could not be saved."
                )

    def draw_background(self):
        '''Select the background for the current state and apply a dark overlay.'''
        background = "menu"

        if self.state == "ticket":
            background = "ticket"

            if self.ticket_game.status == "failed":
                background = "failed"

        elif self.state == "story":
            background = self.current_event.background
            selected = self.current_event.selected_option

            if selected is not None:
                next_step = selected["next"]

                if next_step == "boss_ending":
                    background = "ending_boss"

                elif next_step == "help_ending":
                    background = "ending_help"

                elif next_step == "concert_ending":
                    background = "ending_concert"

                elif next_step == "failed":
                    background = "failed"

        elif self.state == "train":
            background = "transport"

            if self.train_game.status == "failed":
                background = "failed"

        elif self.state == "wheel":
            background = "transport"

            if self.lucky_wheel.status == "finished":
                if not self.lucky_wheel.lucky:
                    background = "failed"

        self.screen.blit(
            self.backgrounds[background], (0, 0)
        )

        self.screen.blit(
            self.background_shade, (0, 0)
        )

if __name__ == "__main__":
    game = Game()
    game.run()