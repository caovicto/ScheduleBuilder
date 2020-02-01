from Design.CoursePlanner import *
from Design.Student import *
from Design.ProgramDatabase import *


coursedb = CourseDatabase()
programdb = ProgramDatabase()

pastCourses = {"WRA101", "MTHWAIV2", "IAH201", "MTH134", "ISS210", "designated score on Mathematics Placement test", "Designated score on Mathematics Placement test", "Completion of Tier I Writing Requirement", "completion of Tier I writing requirement", "designated score on English Placement test"}
suj = Student("../PreviousCourses/Victoria.txt")

cp = CoursePlanner(suj)



