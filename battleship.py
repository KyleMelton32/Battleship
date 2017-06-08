import enum
import numpy as np


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

    def get_random_tuple(self):
        return np.random.randint(0, 10), np.random.randint(0, 10)

    def get_random_direction(self):
        side_or_up = np.random.randint(0, 2)
        x = np.random.randint(0, 2)
        if x == 0:
            x = x - 1
        if side_or_up == 0:
            return x, 0
        else:
            return 0, x

        return get_random_tuple(-1, 1)

    def out_of_bounds(self, tuplevalue):
        return tuplevalue[0] < 0 or tuplevalue[0] > 9 or tuplevalue[1] < 0 or tuplevalue[1] > 9

    def create_ship(self, length):
        current_ship = []
        start_value = self.get_random_tuple()
        if start_value in ship_list:
            return []
        current_ship.append(tuple(start_value))
        current_field = start_value

        direction = self.get_random_direction()
        other_dir_1 = tuple(reversed(direction))
        other_dir_2 = [x * -1 for x in other_dir_1]
        for j in range(length):
            current_field = tuple(map(sum, zip(current_field, direction)))
            next_field = tuple(map(sum, zip(current_field, direction)))
            surrounding_field_1 = tuple(map(sum, zip(current_field, other_dir_1)))
            surrounding_field_2 = tuple(map(sum, zip(current_field, other_dir_2)))
            if self.out_of_bounds(current_field):
                return []
            for sublist in ship_list:
                if (current_field in sublist or next_field in sublist or surrounding_field_1 in sublist
                    or surrounding_field_2 in sublist):
                    return []
            current_ship.append(tuple(current_field))
        return current_ship

        def get_random_ship_positions(self):
            global ship_list
            ship_list = []
            length = 0
            for i in range(4, -1, -1):
                if i == 0:
                    length = 2
                else:
                    length = i
                current_ship = []
                while current_ship == []:
                    current_ship = self.create_ship(length)

                ship_list += [current_ship]
            return ship_list
