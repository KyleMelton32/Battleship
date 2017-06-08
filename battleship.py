import enum


class GameState(enum.Enum):
    SETUP = "Setup"


class Battleship:
    def __init__(self):
        self.game_state = GameState.SETUP
        self.opponent_ships = []
        self.player_ships = []

    def fire(self, x, y):
        """
        for ships in ship_list:
                if (x, y) in ships:
                    return True"""
        return False
