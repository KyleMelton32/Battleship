import argparse
import socket

class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.turn = 0


class Server:
    def __init__(self, server_port_number=54332, max_players=-1):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_port_number = server_port_number
        self.max_players = max_players
        self.waiting_players = []
        self.player_games = {}
        self.start_socket()

    def start_socket(self):
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('0.0.0.0', self.server_port_number))
        self.server_socket.listen(5)
        while True:
            connection = self.server_socket.accept()
            message = connection.recv(100)
            print("Server received: %s" % message)
            if connection in self.player_games.keys():
                connection.send("What is a game!")
            elif connection in self.waiting_players:
                connection.send("be patient!")
            elif "new_player" in message:
                self.waiting_players.append(connection)
                connection.send("looking_for_other_players")
                if len(self.waiting_players) % 2 == 0:
                    game = Game(self.waiting_players.pop(), self.waiting_players.pop())
                    self.player_games[game.player1] = game
                    self.player_games[game.player2] = game



def main(server_port_number=54332):
    Server(server_port_number, 500)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--server_port_number', help='server port number argument',
                        required=False, default=str(54332))
    args = parser.parse_args()
    server_port_number = int(args.server_port_number)
    main(server_port_number=server_port_number)
