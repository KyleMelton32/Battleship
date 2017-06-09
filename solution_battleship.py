import enum
import random
import numpy as np


def get_random_tuple():
    """
    This method generates a 2-tuple containing values between 0 and 9.
    :return: 2-tuple of ints
    """
    return np.random.randint(0, 10), np.random.randint(0, 10)


def get_random_direction():
    """
    This method randomly generates a direction (vertical or horizontal)
    :return: "horizontal" or "vertical"
    """
    # TODO(8): Create the logic for this method based on the docstring above.
    direction = random.randrange(0, 2)
    return "horizontal" if direction else "vertical"


def point_out_of_bounds(tuplevalue):
    """
    This method checks to make sure the tuple is a valid point on the 10x10 battleship board
    :param tuplevalue: 
    :return: 
    """
    # TODO(7): Create the logic for this method based on the docstring above.
    return tuplevalue[0] < 0 or tuplevalue[0] > 9 or tuplevalue[1] < 0 or tuplevalue[1] > 9

def point_valid(ship_list, tuplevalue):
    """
    This method checks to see if tuplevalue is a valid move on the board. (aka, cannot be the spot of a current ship, 
    or partially off the board) :param ship_list: :param tuplevalue: :return: 
    """
    # TODO(6): Create the logic for this method based on the docstring above.
    for ship in ship_list:
        if tuplevalue in ship:
            return False
    return not point_out_of_bounds(tuplevalue)


def create_ship(length, ship_list):
    """
    This method randomly picks a direct, and starting location for a ship. It generates a list of parameter length 
    coordinates(2-tuples). The list must be a valid ship and of the provided length.
    :param length: 
    :param ship_list: :return: 
    """
    # TODO(2): Create the logic for this method based on the docstring above.
    ship = []
    while True:
        direction = get_random_direction()
        position = get_random_tuple()
        for i in range(length):
            coordinate = (position[0] + i, position[1]) if direction == "horizontal" else (position[0], position[1] - i)
            if not point_valid(ship_list, coordinate):
                break # Not valid point so must be an invalid starting position
            ship.append(coordinate)
        if len(ship) == length:
            return ship
        ship.clear()

def get_random_ship_positions():
    """
    This method generates 5 ships and adds each ship to a list. Use the create_ship method. 
    :return: 
    """
    # TODO(4): Create the logic for this method based on the docstring above.
    ship_list = [create_ship(2, ())]
    ship_list.append(create_ship(3, ship_list))
    ship_list.append(create_ship(3, ship_list))
    ship_list.append(create_ship(4, ship_list))
    ship_list.append(create_ship(5, ship_list))
    return ship_list


class GameState(enum.Enum):
    SETUP = "Setup"
    MIDGAME = "Midgame"


class Opponent:
    def __init__(self):
        self.ships = get_random_ship_positions()
        self.shots = []

    def take_turn(self):
        """
        This recursive method randomly selects a point. If the point has not been fired at, add it to the list of points
        that have been fired at. If the point has been fired at previously, enter a recursive loop until an available 
        coordinate can be fired at.
        :return: the 2 tuple representing the coordinate fired at
        """
        # TODO(8): Create the logic for this method based on the docstring above.
        shot = get_random_tuple()
        if shot in self.shots:
            shot = self.take_turn()
        self.shots.append(shot)
        return shot


class Battleship:
    def __init__(self):
        self.game_state = GameState.SETUP
        self.opponent = Opponent()
        self.opponent_ships = self.opponent.ships
        self.player_ships = []
        self.turn = 1

    def player_fire(self, x, y):
        """
        This method checks if the (x, y) coordinate is a position on a ship, if it is, return "hit" otherwise "miss". 
        When a ship is hit, remove the coordinate from self.opponent_ships. When the list is empty, print "You win! 
        and close the program. :param x: :param y: :return: 
        """
        for ship in self.opponent_ships:
            if (x, y) in ship:
                ship.remove((x, y))
                if (len(ship) == 0):
                    self.opponent_ships.remove(ship)
                    if (len(self.opponent_ships) == 0):
                        print("You win!")
                        exit()
                return "hit"
        return "miss"

    def opponent_fire(self):
        """
        This method calls on the opponent to take a turn and then check if it was a hit or a miss. If it was a hit, 
        return a tuple in the form of (<result>, x, y), where <result> is the shot was a hit/miss, and x/y is the coordinate return from
        self.opponent.take_turn()
        When a ship is hit, remove the coordinate from self.player_ships. When the list is empty, print "You lose! 
        :return: a tuple containing 
        """
        #TODO(1): Create the logic for this method based on the docstring above.
        shot = self.opponent.take_turn()
        for ship in self.player_ships:
            if (shot[0], shot[1]) in ship:
                ship.remove((shot[0], shot[1]))
                if (len(ship) == 0):
                    self.player_ships.remove(ship)
                    if (len(self.player_ships_ships) == 0):
                        print("You lose!")
                        exit()
                return "hit", shot[0], shot[1]
        return "miss", shot[0], shot[1]
