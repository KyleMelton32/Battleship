import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random # REMOVE BEFORE SUBMITTING!!!! (JUST FOR TESTING)

class Battleship:
    def __init__(self):
        print("TODO")

    def fire(self, x, y):
        #TEST:
        print("X: " + str(x) + "   Y: " + str(y))
        return random.randrange(0, 2) == 0





class Interface:
    def __init__(self, game):
        self.game = game
        self.fig = plt.figure(figsize=(8, 13), facecolor="#292929")
        self.opponent_board, self.opponent_polygons = self.load_game_board(211, "Opponent's Battlefield")
        self.player_board, self.player_polygons = self.load_game_board(212, "Your Battlefield")
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        red_patch = mpatches.Patch(color='red', label='Hit')
        white_patch = mpatches.Patch(color='white', label='Miss')
        gray_patch = mpatches.Patch(color='gray', label="Ship")
        blue_patch = mpatches.Patch(label="Water")
        self.fig.legend(handles=[red_patch, white_patch, gray_patch, blue_patch], labels=["Hit", "Miss", "Ship", "Water"])
        plt.show()

    def load_game_board(self, position, title):
        board = self.fig.add_subplot(position,
                             aspect='equal', frameon=True,
                             xlim=(0, 10),
                             ylim=(0, 10))
        board.set_title(title, color="white")
        for axis in (board.xaxis, board.yaxis):  # Turn off the ticks and labels
            axis.set_major_formatter(plt.NullFormatter())
            axis.set_major_locator(plt.NullLocator())
        polygons = {}
        for y in range(10):
            for x in range(10):
                polygon = plt.Polygon([[x, y], [x + 1, y],
                                       [x + 1, y + 1], [x, y + 1], [x, y]])
                polygon.set_edgecolor("black")
                polygons[polygon] = (x, y)
                board.add_patch(polygon)
        return board, polygons

    def on_click(self, click):
        for polygon in self.opponent_polygons:
            if polygon.contains_point((click.x, click.y)):
                if self.game.fire(self.opponent_polygons[polygon][0], self.opponent_polygons[polygon][1]):
                    polygon.set_facecolor("red")
                else:
                    polygon.set_facecolor("white")
                self.fig.canvas.draw()
                return
        for polygon in self.player_polygons:
            if polygon.contains_point((click.x, click.y)):
                polygon.set_facecolor("gray")
                self.fig.canvas.draw()
                #TODO: SET SHIPS


def main():
    b = Battleship()
    i = Interface(b)


if __name__ == "__main__":
    main()

