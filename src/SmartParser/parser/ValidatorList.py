from parser.Validator import Validator
from Levenshtein import distance as levenshtein_distance

class ValidatorList(Validator):
    def __init__(self, values):
        self.values = values
        pass

    def tryToFix(self, toBeValidated):
        return None

    def distance(self, toBeValidated):
        distances = []
        for value in self.values:
            distances += [(levenshtein_distance(value, toBeValidated), value)]
            # print(value, toBeValidated, levenshtein_distance(value, toBeValidated))
        distances.sort(key=lambda tup: tup[0])
        
        if distances[0][0] != distances[1][0]:
            return distances[0][1]

        return None


    def validate(self, toBeValidated):
        #print("validate", toBeValidated)
        if toBeValidated in self.values:
            return {"CODE": self.CODE_ACCEPT}
        correct = self.distance(toBeValidated)
        #correct = self.tryToFix(toBeValidated)
        if correct:
            #print("correcting")
            return {"CODE": self.CODE_REPLACE, "NEW_VALUE": correct}

        return {"CODE": self.CODE_REJECT}