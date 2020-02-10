from Design.Student import *
from Design.CoursePlanner import *

import glob


print("""   _____ ____  _    _ _____   _____ ______   _____  _               _   _ _   _ ______ _____  
  / ____/ __ \| |  | |  __ \ / ____|  ____| |  __ \| |        /\   | \ | | \ | |  ____|  __ \ 
 | |   | |  | | |  | | |__) | (___ | |__    | |__) | |       /  \  |  \| |  \| | |__  | |__) |
 | |   | |  | | |  | |  _  / \___ \|  __|   |  ___/| |      / /\ \ | . ` | . ` |  __| |  _  / 
 | |___| |__| | |__| | | \ \ ____) | |____  | |    | |____ / ____ \| |\  | |\  | |____| | \ \ 
  \_____\____/ \____/|_|  \_\_____/|______| |_|    |______/_/    \_\_| \_|_| \_|______|_|  \_\
                                                                                              
                                                                                              """)
name = input("Name: ")
file = ""

path = "PreviousCourses/"+name+"*"
for filename in glob.glob(path):
    file = filename

if file != "":
    mock = Student(name, file)
    cp = CoursePlanner(mock)

else:
    print("Name not found, initializing with no previous courses.")
    file = "PreviousCourses/empty.txt"
    mock = Student(name, file)
    cp = CoursePlanner(mock)
