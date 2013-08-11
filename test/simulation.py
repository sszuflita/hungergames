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
hunterFile = import_path("../strategies/Hunter.py")
randomFile = import_path("../strategies/RandomPlayer.py")
thresholdFile = import_path("../strategies/ThresholdPlayer.py")
strategyFile = import_path("../strategies/Strategy.py")
chaoticFile = import_path("../strategies/ChaoticThresholdPlayer.py")

class PlayerEnvironment:
    def __init__(self, aPlayer, aFood):
        self.thePlayer = aPlayer
        self.theFood = aFood
        self.timesHunted = 0
        self.timesSlacked = 0

    def reputation(self):
        if self.timesHunted == 0 and self.timesSlacked == 0:
            return 0
        else:
            return float(self.timesHunted) / (self.timesHunted + self.timesSlacked)

class PlayerGenerator:
    def __init__(self):
        pass

    def generatePlayer(self, id):
        if id == 0:
            return chaoticFile.ChaoticThresholdPlayer(.97, .03)
        else:
            #return slackerFile.Slacker()
            #return hunterFile.Hunter()
            return thresholdFile.ThresholdPlayer(.95)


class Simulation:
    def __init__(self, aNumPlayers, aPlayerGenerator):
        self.playerDied = False
        self.theRoundNumber = 0
        self.thePlayerEnvironments = []
        amtFood = 300 * (aNumPlayers - 1)
        # always initialize user player to be index 0
        myPlayer = aPlayerGenerator.generatePlayer(0)
        myEnvironment = PlayerEnvironment(myPlayer, amtFood)
        self.thePlayerEnvironments.append(myEnvironment)
        for i in range(1,aNumPlayers):
            myPlayer = aPlayerGenerator.generatePlayer(1)
            myEnvironment = PlayerEnvironment(myPlayer, amtFood)
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
        foodEarnings = [0 for x in range(p)]
        for i in range(p):
            for j in range(i,p):
                (outcome1, outcome2) = self.huntOutcome(allDecisions[i][j],allDecisions[j][i])
                foodEarnings[i] += outcome1
                foodEarnings[j] += outcome2
        for i in range(p):
            playerEnvironment = self.thePlayerEnvironments[i]
            playerEnvironment.thePlayer.hunt_outcomes(foodEarnings[i])
            playerEnvironment.theFood += foodEarnings[i]
        count = 0
        for i in range(p):
            playerEnvironment = self.thePlayerEnvironments[i]
            for j in range(p):
                if allDecisions[i][j] == 'h':
                    playerEnvironment.timesHunted += 1
                    count += 1
                elif allDecisions[i][j] == 's':
                    playerEnvironment.timesSlacked += 1
                    
        if count >= m:
            award = 2*(p-1)
        else:
            award = 0
        for i in range(p):
            playerEnvironment = self.thePlayerEnvironments[i]
            playerEnvironment.thePlayer.round_end(award, m, p)
            playerEnvironment.theFood += award

    def isGameOver(self):
        if self.playerDied:
            print "Game is over: User Player died :("
            return True
        if len(self.thePlayerEnvironments) == 1:
            print "Game is over: User Player won!!!! :)"
            return True
        if self.theRoundNumber > 10000 and random.randint(0,100) > 90:
            print "Game is over: Large of number of rounds reached"
            max = self.thePlayerEnvironments[0].theFood
            maxIdx = 0
            for i in range(1,len(self.thePlayerEnvironments)):
                if self.thePlayerEnvironments[i].theFood > max:
                    max = self.thePlayerEnvironments[i].theFood
                    maxIdx = i
            if maxIdx == 0:
                print "User Player won still!"
            else:
                print "User Player lost :(. Player ", maxIdx, " won instead."
            return True
        return False

    def cleanUpAfterRound(self):
        i = 0
        while(i < len(self.thePlayerEnvironments)):
            myPlayerEnvironment = self.thePlayerEnvironments[i]
            if (myPlayerEnvironment.theFood <= 0):
                # the first time this happens means that our played died
                if i == 0:
                    self.playerDied = True
                del self.thePlayerEnvironments[i]
            else:
                i += 1
                
    def huntOutcome(self, decision1, decision2):
        if (decision1, decision2) == ('h', 'h'):
            return (0,0)
        if (decision1, decision2) == ('h', 's'):
            return (-3,1)
        if (decision1, decision2) == ('s', 'h'):
            return (1,-3)
        if (decision1, decision2) == ('s', 's'):
            return (-2,-2)
        return (0,0)

    def printPlayers(self):
        for i in range(len(self.thePlayerEnvironments)):
            if i == 0 and not self.playerDied:
                print "User Player: ", self.thePlayerEnvironments[i].theFood
            else:
                print self.thePlayerEnvironments[i].theFood

if __name__ == "__main__":
    pg = PlayerGenerator()
    sim = Simulation(10, pg)

    while not sim.isGameOver():
        sim.simulateRound()
        sim.cleanUpAfterRound()
        print "Round " + str(sim.theRoundNumber)
        sim.printPlayers()
    sim.printPlayers()


