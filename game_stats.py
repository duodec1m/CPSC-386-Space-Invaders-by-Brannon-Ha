import json

class GameStats():
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_settings):
        """Initialize statistics."""
        self.ai_settings = ai_settings
        self.reset_stats()

        # Start game in an inactive state.
        self.game_active = False

        # Should you go into the High Scores menu
        self.hs_menu = False

        # High score should never be reset.
        self.high_score = 0

        """Read the saved high score from the json file on disk (if it exists)"""
        try:
            with open('high_scores.json', 'r') as file:
                self.high_scores_all = json.load(file)  # Cast to int to verify type
                self.high_scores_all.sort(reverse=True)
                self.high_score = self.high_scores_all[0]
        except (FileNotFoundError, ValueError, EOFError, json.JSONDecodeError, AttributeError, IndexError) as e:
            print(e)
            self.high_scores_all = [0, 0, 0]  # Some issue with the file, going to default
            self.high_score = self.high_scores_all[0]

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def save_hs_to_file(self):
        """Save the high score to a json file on disk"""
        for i in range(len(self.high_scores_all)):
            if self.score >= self.high_scores_all[i]:
                self.high_scores_all[i+1] = self.high_scores_all[i]
                self.high_scores_all[i] = self.score
                break
        with open('high_scores.json', 'w') as file:
            json.dump(self.high_scores_all, file)