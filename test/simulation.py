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

    def generatePlayer(self):
        #return slackerFile.Slacker()
        #return hunterFile.Hunter()
        return randomFile.RandomPlayer()


class Simulation:
    def __init__(self, aNumPlayers, aPlayerGenerator):
        self.theRoundNumber = 0
        self.thePlayerEnvironments = []
        for i in range(aNumPlayers):
            myPlayer = aPlayerGenerator.generatePlayer()
            amtFood = 300 * (aNumPlayers - 1)
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
        print allDecisions
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
        print foodEarnings
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
            print playerEnvironment.theFood
            print playerEnvironment.reputation()
        print award

                
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

if __name__ == "__main__":
    pg = PlayerGenerator()
    sim = Simulation(10, pg)
    sim.simulateRound()



