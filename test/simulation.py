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
reverseThresholdFile = import_path("../strategies/ReverseThreshold.py")
helperFile = import_path("../strategies/Helper.py")

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
        i = random.randint(0,6)
        if (i == 0):
            return slackerFile.Slacker()
        if (i == 1):
            return hunterFile.Hunter()
        if (i == 2):
            return randomFile.RandomPlayer(.7 + .3 * random.random())
        if (i == 3):
            setting = (random.randint(0,1) == 0)
            val = random.random()
            return thresholdFile.ThresholdPlayer(.7 + .3 * val, setting, .2 + .3 * val)
        if (i == 4):
            setting = (random.randint(0,1) == 0)
            val = random.random()
            return chaoticFile.ChaoticThresholdPlayer(.7 + .3 * val, .05, setting, .2 + .3 * val)
        if (i == 5):
            setting = (random.randint(0,1) == 0)
            val = random.random()
            return reverseThresholdFile.ReverseThreshold(.7 + .3 * val, setting, .2 + .3 * val)
        if (i == 6):
            return helperFile.Helper()

class Simulation:
    def __init__(self, aNumPlayers, aPlayerGenerator):
        self.theRoundNumber = 0
        self.thePlayerEnvironments = []
        amtFood = 300 * (aNumPlayers - 1)
        # always initialize user player to be index 0
        for i in range(0, aNumPlayers):
            myPlayer = aPlayerGenerator.generatePlayer(i)
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
        if len(self.thePlayerEnvironments) == 1:
            print "Game is over: One player remaining."
            print "Game ended on round:", self.theRoundNumber
            self.thePlayerEnvironments[0].thePlayer.printInfo()
            return True
        if len(self.thePlayerEnvironments) == 0:
            print "No victor in the Hunger Games :(."
            print "Game ended on round:", self.theRoundNumber
            return True
        if self.theRoundNumber > 10000 and random.randint(0,100) > 90:
            print "Game is over: Large of number of rounds reached."
            print "Game ended on round:", self.theRoundNumber
            max = self.thePlayerEnvironments[0].theFood
            maxIdx = 0
            for i in range(1,len(self.thePlayerEnvironments)):
                if self.thePlayerEnvironments[i].theFood > max:
                    max = self.thePlayerEnvironments[i].theFood
                    maxIdx = i
            self.thePlayerEnvironments[maxIdx].thePlayer.printInfo()
            return True
        return False

    def cleanUpAfterRound(self):
        i = 0
        while(i < len(self.thePlayerEnvironments)):
            myPlayerEnvironment = self.thePlayerEnvironments[i]
            if (myPlayerEnvironment.theFood <= 0):
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
            print self.thePlayerEnvironments[i].theFood

if __name__ == "__main__":
    pg = PlayerGenerator()
    sizeSim = 30
    sim = Simulation(sizeSim, pg)

    for i in range(100):
        while not sim.isGameOver():
            sim.simulateRound()
            sim.cleanUpAfterRound()
            #print "Round:",sim.theRoundNumber
            #sim.printPlayers()
        #print sim.theRoundNumber
        sim = Simulation(sizeSim, pg)
    # sim.printPlayers()


