# Optional format of the constructor for the OOP approach
class ThresholdPlayer:
    def __init__(self, aThreshold, decayFlag, endPoint):
        self.food = 0
        self.reputation = 0
        self.threshold = aThreshold
        self.initialThreshold = aThreshold
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
        hunt_decisions = []
        for rep in player_reputations:
            if rep < self.threshold and round_number != 1:
                hunt_decisions.append('s')
            else:
                hunt_decisions.append('h')
        return hunt_decisions

    def hunt_outcomes(self, food_earnings):
        pass # do nothing

    def round_end(self, award, m, number_hunters):
        pass # do nothing

    def printInfo(self):
        print "ThresholdPlayer with threshold " + str(self.threshold)
        if self.decayFlag:
            print "Decay setting on, Initial Threshold:", self.initialThreshold, "EndPoint:", self.endPoint
        else:
            print "Decay setting off"
