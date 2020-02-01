from Design.CreateProgramDatabase import *
from Design.ProgramDatabase import *


def createDatabaseTest():
    db = CreateProgramDatabase()
    # db.initializeMinors()
    db.listDatabase()


def getProgram():
    db = ProgramDatabase()
    db.getProgramByName("Accounting", "Major")


createDatabaseTest()
