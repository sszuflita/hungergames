import math, random

class ReverseThreshold:
    def __init__(self, threshold, decayFlag, endPoint):
        self.hunted = 0
        self.slacked = 0
        self.threshold = threshold
        self.initialThreshold = threshold
        self.decayFlag = decayFlag
        self.endPoint = endPoint
        self.startNumPlayers = 0
        self.currentNumPlayers = 0
        
    def refresh_threshold(self):
        if self.decayFlag and self.endPoint < self.initialThreshold:
            self.threshold = self.endPoint + float(self.currentNumPlayers)/self.startNumPlayers*(self.initialThreshold-self.endPoint)

    def hunt_choices(self, round_number, current_food, current_reputation, m,
                     player_reputations):
        if round_number == 1:
            self.startNumPlayers = len(player_reputations)
        self.currentNumPlayers = len(player_reputations)
        self.refresh_threshold()
        if len(player_reputations) == 1:
            return ['s']
        hunt_decisions = []
        if (round_number < 10):
            hunt_decisions = ['h' for player in player_reputations]
        n = len(player_reputations)
        timesToHunt = min(int(math.ceil(self.threshold * (self.hunted + self.slacked + n) - self.hunted)), n)
        for i in range(timesToHunt):
            hunt_decisions.append('h')
            self.hunted += 1
        for i in range(n - timesToHunt):
            hunt_decisions.append('s')
            self.slacked += 1
        hunt_decisions = self.shuffle(hunt_decisions)
        return hunt_decisions

    def hunt_outcomes(self, food_earnings):
        pass

    def round_end(self, award, m, number_hunters):
        pass

    def shuffle(self, hunt_decisions):
        n = len(hunt_decisions)
        for i in range(n):
            j = random.randint(i, n - 1)
            tmp = hunt_decisions[j]
            hunt_decisions[j] = hunt_decisions[i]
            hunt_decisions[i] = tmp
        return hunt_decisions

    def printInfo(self):
        print "ReverseThreshold with threshold " + str(self.threshold)
        if self.decayFlag:
            print "Decay setting on, Initial Threshold:", self.initialThreshold, "EndPoint:", self.endPoint
        else:
            print "Decay setting off"
        
