from Design.Requirement import *


def addReqTest():
    name = "University Tier I Writing"
    RString = """Foreign Language: 1. Foreign Language: 4 courses from in a sequence of at least four courses in a foreign language.
Business: 2. Business: 5 courses from ACC230, EC210, FI320, GBL323, MKT327
Cognate: 5 courses
At least 3 courses from An area other than the College of Engineering approved by academic advisor. At least 6 credits must be at the 300 level or higher. The cognate should enhance the student's ability to apply analytic procedures in a specific subject area.
At least 2 courses from courses numbered at the 300 and 400 levels in an area other the College of Engineering."""
    requirement = Requirement(name, RString)


addReqTest()