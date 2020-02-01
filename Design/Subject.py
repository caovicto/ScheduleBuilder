class Subject:
    def __init__(self, code):
        """

        :param code: string Subject code
        """
        self.code = code
        self.name = ""
        self.getName()


    def __eq__(self, other):
        return self.code == other.subject

    def __str__(self):
        return self.code + ": " + self.name

    def getName(self):
        file = open("/home/victoria/Projects/ScheduleBuilder/Files/Subject.txt", "r")
        for line in file:
            if line.find(self.code) == 0:
                splitLine = line.split()
                self.name = ' '.join(splitLine[1:])

