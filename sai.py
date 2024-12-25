import random
import json
import os

class AdvancedWordGuessGame:
    def __init__(self):
        """Initialize the game with categories, hints, and scores."""
        self.categories = {
            "Animals": [("elephant", "Large mammal with a trunk"), ("tiger", "Striped predator"), ("dolphin", "Smart marine mammal")],
            "Technology": [("python", "Popular programming language"), ("algorithm", "Set of instructions"), ("database", "Stores structured data")],
            "Countries": [("canada", "Maple syrup capital"), ("japan", "Land of the Rising Sun"), ("brazil", "Famous for football and carnival")]
        }
        self.difficulty = "Medium"
        self.max_attempts = 10
        self.score = 0
        self.word = ""
        self.hint = ""
        self.guessed_word = ""
        self.attempts = 0
        self.scoreboard_file = "scoreboard.json"

    def choose_difficulty(self):
        """Allow the user to choose a difficulty level."""
        print("Choose Difficulty: Easy, Medium, Hard")
        while True:
            choice = input("Enter difficulty: ").capitalize()
            if choice in ["Easy", "Medium", "Hard"]:
                self.difficulty = choice
                break
            print("Invalid choice. Please choose Easy, Medium, or Hard.")
        self.max_attempts = {"Easy": 15, "Medium": 10, "Hard": 5}[self.difficulty]

    def choose_category(self):
        """Allow the user to choose a word category."""
        print("\nAvailable Categories:")
        for idx, category in enumerate(self.categories.keys(), 1):
            print(f"{idx}. {category}")
        while True:
            try:
                choice = int(input("Enter category number: ")) - 1
                category = list(self.categories.keys())[choice]
                break
            except (ValueError, IndexError):
                print("Invalid choice. Please select a valid category number.")
        self.word, self.hint = random.choice(self.categories[category])
        self.guessed_word = "_" * len(self.word)

    def display_status(self):
        """Display the current guessed word and attempts left."""
        print(f"\nGuessed Word: {self.guessed_word}")
        print(f"Attempts Left: {self.max_attempts - self.attempts}")
        print(f"Hint: {self.hint}")

    def update_guessed_word(self, letter):
        """Update the guessed word based on player's input."""
        new_guessed_word = list(self.guessed_word)
        for idx, char in enumerate(self.word):
            if char == letter:
                new_guessed_word[idx] = letter
        self.guessed_word = "".join(new_guessed_word)

    def play_turn(self, letter):
        """Process a single turn."""
        if letter in self.word:
            self.update_guessed_word(letter)
            print(f"Good guess! '{letter}' is in the word.")
        else:
            self.attempts += 1
            print(f"Wrong guess. '{letter}' is not in the word.")

    def calculate_score(self):
        """Calculate the score based on attempts and difficulty."""
        base_score = 100
        difficulty_multiplier = {"Easy": 1, "Medium": 2, "Hard": 3}[self.difficulty]
        return max(base_score - (self.attempts * 10), 0) * difficulty_multiplier

    def save_score(self, name):
        """Save the score to the scoreboard."""
        score_data = self.load_scores()
        score_data.append({"name": name, "score": self.score, "difficulty": self.difficulty})
        with open(self.scoreboard_file, "w") as file:
            json.dump(score_data, file, indent=4)

    def load_scores(self):
        """Load the scoreboard data."""
        if os.path.exists(self.scoreboard_file):
            with open(self.scoreboard_file, "r") as file:
                return json.load(file)
        return []

    def display_scoreboard(self):
        """Display the top scores."""
        scores = self.load_scores()
        if scores:
            print("\n--- Scoreboard ---")
            for entry in sorted(scores, key=lambda x: x["score"], reverse=True)[:10]:
                print(f"{entry['name']} - {entry['score']} ({entry['difficulty']})")
        else:
            print("\nNo scores yet.")

    def check_game_over(self):
        """Check if the game is over."""
        if self.guessed_word == self.word:
            self.score = self.calculate_score()
            print(f"\nCongratulations! You've guessed the word: {self.word}")
            print(f"Your Score: {self.score}")
            name = input("Enter your name for the scoreboard: ")
            self.save_score(name)
            return True
        if self.attempts >= self.max_attempts:
            print(f"\nGame Over. The word was: {self.word}")
            return True
        return False

    def start_game(self):
        """Start the advanced word guessing game."""
        self.choose_difficulty()
        self.choose_category()
        print("\nWelcome to the Advanced Word Guessing Game!")
        while not self.check_game_over():
            self.display_status()
            guess = input("Enter a letter: ").lower()
            if len(guess) == 1 and guess.isalpha():
                self.play_turn(guess)
            else:
                print("Invalid input. Please enter a single letter.")
        print("Thanks for playing!")
        self.display_scoreboard()

# Example usage
if __name__ == "__main__":
    game = AdvancedWordGuessGame()
    game.start_game()
