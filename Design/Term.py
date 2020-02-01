class Term:
    def __init__(self, term):
        self.term = term

    def __str__(self):
        return self.term

    def __eq__(self, other):
        return self.term == other.term
