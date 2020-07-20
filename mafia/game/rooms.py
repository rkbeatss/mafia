# To handle different room logic

class Room:
    # room for all 
    # broadcast to all 
    pass

class MafiaRoom(Room):
    # room for all mafia 
    # making mafia decisions
    # broadcast to all mafias only 
    pass

class PersonalRoom(Room):
    # getting my role assigned 
    # anything else you can think of 
    # broadcasts to one client only 
    pass