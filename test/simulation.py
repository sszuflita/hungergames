import os, sys, random

def import_path(fullpath):
    """ 
    Import a file with full path specification. Allows one to
    import from anywhere, something __import__ does not do. 
    """
    path, filename = os.path.split(fullpath)
    filename, ext = os.path.splitext(filename)
    sys.path.append(path)
    module = __import__(filename)
    reload(module) # Might be out of date
    del sys.path[-1]
    return module

slackerFile = import_path("../strategies/Slacker.py")

class PlayerEnvironment:
    def __init__(self, aPlayer, aFood, aPastMoves):
        self.thePlayer = aPlayer
        self.theFood = aFood
        self.thePastMoves = aPastMoves

    def reputation(self):
        if len(self.thePastMoves) == 0:
            return 0
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
        return slackerFile.Slacker()


class Simulation:
    def __init__(self, aNumPlayers, aPlayerGenerator):
        self.theRoundNumber = 0
        self.thePlayerEnvironments = []
        for i in range(aNumPlayers):
            myPlayer = aPlayerGenerator.generatePlayer()
            amtFood = 300 * (aNumPlayers - 1)
            myEnvironment = PlayerEnvironment(myPlayer, amtFood, "")
            self.thePlayerEnvironments.append(myEnvironment)

    def simulateRound(self):
        self.theRoundNumber += 1
        p = len(self.thePlayerEnvironments)
        m = random.randint(1, p * (p - 1) - 1)
        myReputations = []
        for playerEnvironment in self.thePlayerEnvironments:
            myReputations.append(playerEnvironment.reputation())
        allDecisions = []
        for i in range(p):
            playerEnvironment = self.thePlayerEnvironments[i]
            otherHuntDecisions = playerEnvironment.thePlayer.hunt_choices(self.theRoundNumber,
                playerEnvironment.theFood,
                myReputations[i],
                m,
                myReputations[:i] + myReputations[i+1:])
            huntDecisions = otherHuntDecisions[:i] + ["X"] + otherHuntDecisions[i:]
            allDecisions.append(huntDecisions)
        print allDecisions

if __name__ == "__main__":
    pg = PlayerGenerator()
    sim = Simulation(10, pg)
    sim.simulateRound()



