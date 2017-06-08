import solution_battleship

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def turn_of_ticks_and_labels(plot):
    """
    This method turns off the ticks and axis labels for the provided plot.
    :param plot: 
    :return: None
    """
    # TODO(5): Create the logic for this method based on the docstring above.
    for axis in (plot.xaxis, plot.yaxis):  # Turn off the ticks and labels
        axis.set_major_formatter(plt.NullFormatter())
        axis.set_major_locator(plt.NullLocator())


def create_ship_menu(figure, location, title, horizontal, vertical, carrier, battleship, cruiser, submarine,
                     destroyer):
    """
    This method creates the subplot that creates the ship_selector menu. 
    :param figure: the figure that the subplot will sit against
    :param location: the spacing arguement found in matplotlib.pyplot.add_subplot().
    :param title: 
    :param horizontal: 
    :param vertical: 
    :param carrier: 
    :param battleship: 
    :param cruiser: 
    :param submarine: 
    :param destroyer: 
    :return: 
    """
    menu = figure.add_subplot(location,
                              aspect="1", frameon=False,
                              xlim=(0, 10),
                              ylim=(0, 10))
    menu.set_title(title, color="white") #titles visible on a dark background

    menu.set_facecolor("#292929") #Dark background
    ships = {}
    if carrier:
        if horizontal:
            horizontal_carrier = plt.Rectangle(xy=(0, 9), width=5, height=1, color='gray')
            menu.annotate("Carrier", xy=(2.5, 9.5), va="center", ha="center")
            ships[horizontal_carrier] = (5, "horizontal", "carrier")
        if vertical:
            vertical_carrier = plt.Rectangle(xy=(6, 10), width=1, height=-5, color='gray')
            menu.annotate("Carrier", xy=(6.5, 7.5), va="center", ha="center", rotation=270)
            ships[vertical_carrier] = (5, "vertical", "carrier")
    #TODO(3): Continue on the logic provided for the carrier for each of the other ships. This must look similar to
    # gui.png posted on the write up.
    #  (battleship(length 4), cruiser(length 3), submarine(length 3), destroyer(length 2)
    if battleship:
        if horizontal:
            horizontal_battleship = plt.Rectangle(xy=(0, 7), width=4, height=1, color='gray')
            menu.annotate("Battleship", xy=(2, 7.5), va="center", ha="center")
            ships[horizontal_battleship] = (4, "horizontal", "battleship")
        if vertical:
            vertical_battleship = plt.Rectangle(xy=(8, 10), width=1, height=-4, color='gray')
            menu.annotate("Battleship", xy=(8.5, 8), va="center", ha="center", rotation=270)
            ships[vertical_battleship] = (4, "vertical", "battleship")
    if cruiser:
        if horizontal:
            horizontal_cruiser = plt.Rectangle(xy=(0, 5), width=3, height=1, color='gray')
            menu.annotate("Cruiser", xy=(1.5, 5.5), va="center", ha="center")
            ships[horizontal_cruiser] = (3, "horizontal", "cruiser")
        if vertical:
            vertical_cruiser = plt.Rectangle(xy=(6, 4), width=1, height=-3, color='gray')
            menu.annotate("Cruiser", xy=(6.5, 2.5), va="center", ha="center", rotation=270)
            ships[vertical_cruiser] = (3, "vertical", "cruiser")
    if submarine:
        if horizontal:
            horizontal_submarine = plt.Rectangle(xy=(0, 3), width=3, height=1, color='gray')
            menu.annotate("Submarine", xy=(1.5, 3.5), va="center", ha="center")
            ships[horizontal_submarine] = (3, "horizontal", "submarine")
        if vertical:
            vertical_submarine = plt.Rectangle(xy=(8, 4), width=1, height=-3, color='gray')
            menu.annotate("Submarine", xy=(8.5, 2.5), va="center", ha="center", rotation=270)
            ships[vertical_submarine] = (3, "vertical", "submarine")
    if destroyer:
        if horizontal:
            horizontal_destroyer = plt.Rectangle(xy=(0, 1), width=2, height=1, color='gray')
            menu.annotate("Destroyer", xy=(1, 1.5), va="center", ha="center", size=8)
            ships[horizontal_destroyer] = (2, "horizontal", "destroyer")
        if vertical:
            vertical_destroyer = plt.Rectangle(xy=(4, 3), width=1, height=-2, color='gray')
            menu.annotate("Destroyer", xy=(4.5, 2), va="center", ha="center", size=8, rotation=270)
            ships[vertical_destroyer] = (2, "vertical", "destroyer")

    for ship in ships.keys():
        menu.add_patch(ship)

    turn_of_ticks_and_labels(menu)

    figure.canvas.draw()
    return menu, ships


class ShipSelector:
    def __init__(self, figure):
        self.figure = figure
        self.ship_selection_menu, self.ship_buttons = \
            create_ship_menu(self.figure, 224, "Place your ships", True, True, True, True, True, True, True)
        self.selected_boat = None
        self.points = []
        self.setup_boats = {"carrier": False, "battleship": False, "cruiser": False, "submarine": False,
                            "destroyer": False}

    def select_location(self, x, y):
        boat = self.ship_buttons[self.selected_boat]
        points = []
        for i in range(boat[0]):
            location = (x, y)
            if boat[1] == "horizontal":
                location = (x + i, y)
            else:
                location = (x, y - i)
            if not solution_battleship.point_valid(points, location):
                print("Out of bounds!")
                return
            points.append(location)
        self.points.append(points)
        self.selected_boat = None
        self.figure.delaxes(self.ship_selection_menu)
        # redraw the menu without the boat that was selected
        self.setup_boats[boat[2]] = True
        self.ship_selection_menu, self.ship_buttons = \
            create_ship_menu(self.figure, 224, "Place your ships", True, True,
                             (not self.setup_boats["carrier"]), (not self.setup_boats["battleship"]),
                             (not self.setup_boats["cruiser"]),
                             not self.setup_boats["submarine"], (not self.setup_boats["destroyer"]))
        return points

    def finished(self):
        for ship in self.setup_boats:
            if not self.setup_boats[ship]:
                return False
        return True


class Interface:
    def __init__(self, game):
        self.game = game
        self.fig = plt.figure(figsize=(9, 8), facecolor="#292929")
        self.opponent_board, self.opponent_polygons = self.load_game_board(221, "Opponent's Battlefield")
        self.player_board, self.player_polygons = self.load_game_board(223, "Your Battlefield")
        self.ship_selector = ShipSelector(self.fig)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        red_patch = mpatches.Patch(color='red', label='Hit')
        white_patch = mpatches.Patch(color='white', label='Miss')
        gray_patch = mpatches.Patch(color='gray', label="Ship")
        blue_patch = mpatches.Patch(label="Water")
        self.fig.legend(handles=[red_patch, white_patch, gray_patch, blue_patch],
                        labels=["Hit", "Miss", "Ship", "Water"])
        plt.show()

    def load_game_board(self, position, title):
        """
        This method generates a new gameboard grid and fills it with usable boxes. It also turns off the axis labels and ticks.
        :param position:  the spacing arguement found in matplotlib.pyplot.add_subplot().
        :param title: name of the grid
        :return: 
        """
        board = self.fig.add_subplot(position,
                                     aspect='equal', frameon=True,
                                     xlim=(0, 10),
                                     ylim=(0, 10))
        board.set_title(title, color="white")
        turn_of_ticks_and_labels(board)
        grid = {}
        for y in range(10):
            for x in range(10):
                polygon = plt.Polygon([[x, y], [x + 1, y],
                                       [x + 1, y + 1], [x, y + 1], [x, y]])
                polygon.set_edgecolor("black")
                grid[polygon] = (x, y)
                board.add_patch(polygon)
        return board, grid

    def on_click(self, click):
        if self.game.game_state is solution_battleship.GameState.SETUP:
            for button in self.ship_selector.ship_buttons:
                if button.contains_point((click.x, click.y)):
                    self.ship_selector.selected_boat = button
                    return
            if self.ship_selector.selected_boat is not None:
                for polygon in self.player_polygons:
                    if polygon.contains_point((click.x, click.y)):
                        ship_points = self.ship_selector.select_location(self.player_polygons[polygon][0],
                                                                         self.player_polygons[polygon][1])
                        if ship_points is None:
                            return
                        for ship_point in self.player_polygons:
                            if self.player_polygons[ship_point] in ship_points:
                                ship_point.set_facecolor("gray")
                        if self.ship_selector.finished():
                            solution_battleship.player_ships = self.ship_selector.points
                            self.game.game_state = solution_battleship.GameState.MIDGAME
                        self.fig.canvas.draw()
                        return
        if self.game.game_state is solution_battleship.GameState.MIDGAME:
            for polygon in self.opponent_polygons:
                if polygon.contains_point((click.x, click.y)):
                    if self.game.player_fire(self.opponent_polygons[polygon][0], self.opponent_polygons[polygon][1]) == "hit":
                        polygon.set_facecolor("red")
                    else:
                        polygon.set_facecolor("white")
                    opponent_turn = self.game.opponent_fire()
                    if opponent_turn[0] == "hit":
                        self.change_square_color_on_player_board(opponent_turn[1], opponent_turn[2], "red")
                    else:
                        self.change_square_color_on_player_board(opponent_turn[1], opponent_turn[2], "white")
                    self.fig.canvas.draw()
                    return

    def change_square_color_on_player_board(self, x, y, color):
        for square in self.player_polygons:
            if self.player_polygons[square] == (x, y):
                square.set_facecolor(color)


def main():
    game = solution_battleship.Battleship()
    Interface(game)


if __name__ == "__main__":
    main()
