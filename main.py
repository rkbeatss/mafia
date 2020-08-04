from network.server import Server
from network.moderator import Moderator

if __name__ == "__main__":
    server = Server()  
    game = Moderator(server)
    game.run()
