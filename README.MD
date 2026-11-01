This game uses Pygame and must be run locally rather than in the Ed environment.
And the document size is greater than 2MB (the Ed limit) so the external files are on my github

GitHub Repository
https://github.com/SharonChen1/COMP9001-26S2-FinalAssignment-SID560359204

Requirements

- Python 3.12
- Pygame 2.6.1

Install Pygame by running:

    py -3.12 -m pip install pygame==2.6.1

Project Files

This project contains 8 Python files and one images folder:

- game.py: Main entry point; manages game screens and transitions.
- button.py: Defines reusable buttons.
- story_data.py: Stores story events, choices, and outcomes.
- story_event.py: Displays story events and handles choices.
- ticket_game.py: Manages ticket purchasing and code verification.
- train_game.py: Manages the high-speed train challenge.
- lucky_wheel.py: Manages the lucky wheel mini-game.
- save_data.py: Loads and saves endings and reaction records.

The images folder contains 12 images for the required background and button images.

How to Run

1. Keep all Python files and the images folder together.
2. Open a terminal in the project folder.
3. Run the following command:

    py -3.12 game.py

Controls

- Mouse: Click buttons and select story choices.

- Ticket verification: Type the four-digit code, press Enter to submit, and use Backspace to delete.

- High-speed train challenge: Press and release SPACE repeatedly. Holding it down does not count.

Saved Progress

Unlocked endings and the best successful ticket reaction time are saved automatically in endings.txt and best_time.txt in the project folder. These files do not need to exist before the first run.