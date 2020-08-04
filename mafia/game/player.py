# To handle player state itself 

class Player:
    def __init__(self, player_id, address):
        self.id = player_id
        self.address = address

    def get_description(self):
        return ("You are a player in this game.")


class Mafia(Player):
    def __init__(self, player_id, address):
        Player.__init__(self, player_id, address)

    def get_description(self):
        return ("You are a Mafia. Your goal is to collaborate with other Mafias and eliminate as many villagers without getting exposed.")


class Villager(Player):
    def __init__(self, player_id, address):
        Player.__init__(self, player_id, address)

    def get_description(self):
        return ("You are a Villager. You have a big responsibility to catch the Mafias and save the innocent.")