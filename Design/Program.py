import re
from Design.Requirement import *


class Program:
    def __init__(self, number, name, reqString):
        self.number = number
        self.name = name
        self.credits = 0
        self.requirements = []

        parsedWords = re.findall(r"\nRequired Credits: \d*", reqString)
        self.credits = int(parsedWords[0].split()[2])

        ignore = ["University Residency", "College Distribution", "Distribution"]
        for line in reqString.split("\nRequirement"):
            newRequirement = Requirement(line)
            if newRequirement.isValid() and not any(s in newRequirement.name for s in ignore):
                # print(newRequirement)
                self.requirements.append(newRequirement)
        # self.requirements = Requirement(reqString)


    def __str__(self):
        s = self.name + ": " + str(self.credits) + " credits\n"
        for ele in self.requirements:
            s += str(ele)


    def getRequirements(self):
        return self.requirements


