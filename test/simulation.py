
class PlayerEnvironment:
    def __init__(self, aPlayer, aFood, aPastMoves):
        self.thePlayer = aPlayer
        self.theFood = aFood
        self.thePastMoves = aPastMoves

    def reputation(self):
        h = 0
        s = 0
        for c in self.thePastMoves:
            if c == 'h':
                h += 1
            if c == 's':
                s += 1
        return 1. * h / (h + s)

class PlayerGenerator:
    def __init__(self):
        pass

    def generatePlayer(self):
        return Slacker()

class Simulation:
    def __init__(self, aNumPlayers, aPlayerGenerator):
        self.thePlayers = []
        for i in range(aNumPlayers):
            self.thePlayers.append(aPlayerGenerator.generatePlayer())