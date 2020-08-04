from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import PointerToConnection
from .server import Server
from mafia.game.player import Player, Mafia, Villager
import random
from typing import List, Dict, Union

# connect all clients in here
# game server and handling of game in general


class Moderator(ShowBase):
    def __init__(self, _server):
        # everything in the console for now
        ShowBase.__init__(self, windowType='none')
        self.server = _server
        self.players = list()

        # two major ongoing tasks
        # check if start game
        # check if end game

        self.taskMgr.add(self.check_start_game,
                         "See if game can be started", -30)
        self.taskMgr.add(self.check_end_game, "See if game has ended", -31)

    def check_start_game(self, task: Task) -> Task:
        if not self.server.start:
            # keep checking if we can start the game yet
            return Task.cont
        else:
            self.broadcast("Assigning players....")
            self.assign_players(self.server.active_connections)
        return Task.done

    def check_end_game(self, task: Task) -> Task:
        # TODO: Implement this
        return Task.cont

    def randomize_players(self, nbr_players: int) -> List[Union[Villager, Mafia]]:
        mafia_proportion = self.calculate_proportion(nbr_players)
        choices = mafia_proportion * [Mafia] + \
            (nbr_players - mafia_proportion) * [Villager]
        random.shuffle(choices)
        return choices

    def assign_players(self, players: Dict[str, PointerToConnection]) -> None:
        choices = self.randomize_players(len(players))
        for (player_id, address), assignment in zip(players.items(), choices):
            player = assignment(player_id, address)
            description = player.get_description()
            self.players.append(player)
            self.personal_message(description, address)

    def calculate_proportion(self, nbr_players: int) -> int:
        # 3:1 ratio for villagers to mafia
        return nbr_players // 3

    def start_game(self) -> None:
        # TODO: Implement this 
        pass

    def broadcast(self, message: str) -> None:
        self.server.broadcast_message(message)

    def personal_message(self, message: str, person) -> None:
        self.server.send_personal_message(message, person)
