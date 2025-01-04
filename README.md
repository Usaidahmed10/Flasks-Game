# Magical Flask Game

## Overview
The **Magical Flask Game** is a Python-based terminal game where players sort chemicals into their respective flasks. The game is built to challenge your logic and speed while showcasing the practical implementation of fundamental data structures like **Bounded Stack** and **Bounded Queue**.

## Features
- **Levels of Increasing Difficulty:** Three chemical files (`chemicals1.txt`, `chemicals2.txt`, `chemicals3.txt`) represent different game levels.
- **Data Structures:**
  - **Bounded Stack:** Used to manage the chemicals in flasks.
  - **Bounded Queue:** Used to enqueue chemicals before filling flasks.
- **Time Tracking:** Tracks the time taken to complete each level.
- **Progressive Gameplay:** Option to move to the next level after completing the current one.

## How to Play
1. Start the game by running the `flasks.py` file.
2. A welcome message will display the objective and rules.
3. You will see a visual representation of flasks and chemicals.
4. Use the terminal to input:
   - The source flask number.
   - The destination flask number.
5. Your goal is to sort all chemicals such that each flask contains only one type of chemical.
6. Complete the level as quickly as possible to beat the timer!
7. After completing a level, you can choose to move to the next level or exit the game.

## Files
- **bqueue.py:** Implements the `BoundedQueue` data structure.
- **bstack.py:** Implements the `BoundedStack` data structure.
- **flasks.py:** The main game logic.
- **chemicals1.txt, chemicals2.txt, chemicals3.txt:** Input files for the game levels.

## Screenshot
![Screenshot 2025-01-02 235643](https://github.com/user-attachments/assets/fdfdf516-8a45-4057-982e-15f3b3f8d6af)

## Cloning the Repository
To get started with this project, clone the repository to your local machine:

```bash
git clone <repository_url>
```
Replace `<repository_url>` with the URL of this repository. For example:

```bash
git clone https://github.com/your-username/magical-flask-game.git
```

Navigate into the project directory:

```bash
cd magical-flask-game
```

## Running the Game
Run the following command to start the game:

```bash
python flasks.py
```

## Contributing
Feel free to develop more levels by creating additional chemical files and pushing them to this repository. Contributions to improve the game logic, UI, or features are welcome!

## License
This project is open-source and available under the MIT License.

