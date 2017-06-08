import enum
import random
import numpy as np


def get_random_tuple():
    return np.random.randint(0, 10), np.random.randint(0, 10)


def get_random_direction():
    direction = random.randrange(0, 2)
    return "horizontal" if direction else "vertical"


def point_out_of_bounds(tuplevalue):
    return tuplevalue[0] < 0 or tuplevalue[0] > 9 or tuplevalue[1] < 0 or tuplevalue[1] > 9


def create_ship(length, ship_list):
    current_ship = []
    start_value = get_random_tuple()
    if start_value in ship_list:
        return []
    current_ship.append(tuple(start_value))
    current_field = start_value

    direction = get_random_direction()
    other_dir_1 = tuple(reversed(direction))
    other_dir_2 = [x * -1 for x in other_dir_1]
    for j in range(length):
        current_field = tuple(map(sum, zip(current_field, direction)))
        next_field = tuple(map(sum, zip(current_field, direction)))
        surrounding_field_1 = tuple(map(sum, zip(current_field, other_dir_1)))
        surrounding_field_2 = tuple(map(sum, zip(current_field, other_dir_2)))
        if point_out_of_bounds(current_field):
            return []
        for sublist in ship_list:
            if current_field in sublist or next_field in sublist or surrounding_field_1 in sublist or surrounding_field_2 in sublist:
                return []
        current_ship.append(tuple(current_field))
    return current_ship


def get_random_ship_positions():
    ship_list = []
    length = 0
    for i in range(4, -1, -1):
        if i == 0:
            length = 2
        else:
            length = i
        current_ship = []
        while current_ship == []:
            current_ship = create_ship(length, ship_list)

        ship_list += [current_ship]
    return ship_list


class GameState(enum.Enum):
    SETUP = "Setup"
    MIDGAME = "Midgame"


class Opponent:
    def __init__(self):
        self.ships = get_random_ship_positions()
        self.shots = []

    def take_turn(self):
        shot = get_random_tuple()
        if shot in self.shots:
            return self.take_turn()
        return shot


class Battleship:
    def __init__(self):
        self.game_state = GameState.SETUP
        self.opponent = Opponent()
        self.opponent_ships = self.opponent.ships
        self.player_ships = []
        self.turn = 1

    def player_fire(self, x, y):
        if self.turn != 1:
            return None
        for ships in self.opponent_ships:
            if (x, y) in ships:
                return "hit"
        return "miss"
