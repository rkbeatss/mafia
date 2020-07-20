# To handle player state itself 

class Player:
    def __init__(self, player_id, num):
        self.id = player_id 
        self.name = name 
    def get_description(self):
        return ("True")
       
class Mafia(Player):
    def __init__(self):
        Player.__init__(self)
    def get_description(self):
        pass
        
class Villager(Player):
    def __init__(self):
        Player.__init__(self)
    def get_description(self):
        pass

