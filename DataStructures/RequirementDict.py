
class RequirementDict:
    def __init__(self):
        self.reqdict = {}
        self.credits = 0

    def __str__(self):
        s = "Credits: " + str(self.credits) + '\n'
        for req in self.reqdict.values():
            s += str(req) + '\n'
        return s

    def add_req(self, req):
        """
        name: (string) name of requirement
        req: (Requirement) requirement object
        """
        if self.reqdict.get(req.name) is None:
            self.reqdict[req.name] = req

    def remove(self, name):
        if self.reqdict.get(name):
            del self.reqdict[name]

    def get_reqs(self):
        return self.reqdict.values()


    def set_credit(self, credit):
        self.credits = credit

    def find(self, name):
        """
        returns requirement object with given name from dictionary
        """
        return self.reqdict.get(name)

    def match(self, name):
        for key in self.reqdict.keys():
            if name in key:
                return key

    def merge(self, other):
        """
        Add all requirements of other req dictionary
        """
        if len(self.get_reqs()) == 0:
            self.reqdict = other.reqdict
            self.credits = other.credits
        else:
            for other_req in other.get_reqs():
                added = False
                # check for intersecting requirements within current dict
                for this_req in self.get_reqs():
                    if "University" not in this_req.name:
                        sub = this_req.subset(other_req)
                        if sub == other_req:
                            self.remove(this_req.name)
                            break
                        elif sub == this_req:
                            added = True
                            break
                if not added:
                    self.add_req(other_req)


    def create_options(self):
        single = []
        multiple = []
        for req in self.get_reqs():
            req.clean()
            if len(req.options) > 1:
                multiple.append(req)
            elif len(req.options) == 1:
                single.append(req)


        return single, multiple



class Requirement:
    def __init__(self, name):
        """
        self.options: (list<Option>)
        """
        self.name = name
        self.options = []


    def __str__(self):
        s = self.name + '\n'
        for ele in self.options:
            s += str(ele) + '\n'

        return s

    def add(self, option):
        self.options.append(option)

    def subset(self, other):
        """

        """
        for other_opt in other.options:
            for this_opt in self.options:
                intersection = set(this_opt.courses).intersection(set(other_opt.courses))

                # if common courses types are equal
                if intersection and (len(intersection) >= other_opt.number or len(intersection) >= this_opt.number) and this_opt.type == other_opt.type:
                    # other requirement is superset of this requirement
                    if this_opt.number <= other_opt.number:
                        if len(intersection) > other_opt.number:
                            new_option = Option(other_opt.number, other_opt.type, intersection)
                            other.options = [new_option]
                        else:
                            for same_course in intersection:
                                other_opt.courses[other_opt.courses.index(same_course)] = same_course+"*"
                        return other

                    # this requirement is superset of other requirement
                    elif this_opt.number >= other_opt.number:
                        if len(intersection) > this_opt.number:
                            new_option = Option(this_opt.number, this_opt.type, intersection)
                            self.options = [new_option]
                        else:
                            for same_course in intersection:
                                this_opt.courses[this_opt.courses.index(same_course)] = same_course+"*"
                        return self

    def clean(self):
        if len(self.options) > 1:
            new_options = [self.options.pop()]

            for other in self.options:
                add = True
                for this in new_options:
                    intersection = set(this.courses).intersection(set(other.courses))
                    greater = len(this.courses) if len(this.courses) > len(other.courses) else len(other.courses)
                    if len(intersection)/float(greater) > 0.8:
                        add = False
                if add:
                    new_options.append(other)

            self.options = new_options


class Option:
    def __init__(self, num, type, courses):
        """
        self.number: number of credits/courses
        self.type: credit or course
        self.courses: available courses to take
        """
        self.number = num
        self.type = type
        self.courses = courses


    def __str__(self):
        return str(self.number) + ' ' + self.type + ' ' + ','.join(self.courses)


    def check(self, other):
        intersection = set(self.courses).intersection(set(other.courses))
        if intersection and self.number == other.number and self.type == other.type:
            return self if len(self.courses) < len(other.courses) else other



