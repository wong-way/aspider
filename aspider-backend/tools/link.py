class Link(object):

    def __init__(self, source, target, value):
        self.source = source
        self.target = target
        self.value = value

    def __eq__(self, other):
        if isinstance(other, Link):
            return (self.source == other.source) and (self.value == other.value) and (self.target == self.target)
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.source) + hash(self.target) + hash(self.value)
