class User:
    def __init__(self, id: int, first_name: str, last_name: str):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self):
        return f'{self.id} {self.first_name} {self.last_name}'

    def __eq__(self, other):
        return isinstance(other, User) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))