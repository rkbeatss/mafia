from direct.showbase.ShowBase import ShowBase

# connect all clients in here 
# game server and handling of game in general
class GameHandler(ShowBase):
    ShowBase.__init__(self, windowType='none') # everything in the console for now
    self.players = dict()
    
    # initialize general room
    # initialize personal room
    # assign roles
    
