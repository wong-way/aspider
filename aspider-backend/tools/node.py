class Node(object):

    def __init__(self, value, name):
        self.name = name
        self.value = value

    def __eq__(self, other):
        if isinstance(other, Node):
            return (self.name == other.name) and (self.value == other.value)
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name) + hash(self.value)
