class User:
    def __init__(self, id: int, first_name: str, last_name: str, is_closed: bool=False, kwargs: dict=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.is_closed = is_closed

        if kwargs:
            self.__dict__.update(kwargs)

    def __str__(self):
        return f'{self.id} {self.first_name} {self.last_name}'

    def info(self):

        info = (f'ID: {self.id}\n'
                f'Имя: {self.first_name} {self.last_name}')
        if self.domain:
            info += f'\nНикнейм: {self.domain}'
        if self.status:
            info += f'\nСтатус: {self.status}'
        if self.about:
            info += f'\nО себе: {self.about}'

        info += '\n'
        if self.sex:
            info += f'\nПол: {self.sex}'
        if self.bdate:
            info += f'\nДата рождения: {self.bdate}'
        if self.city:
            info += f'\nГород: {self.city}'
        if self.home_town:
            info += f'\nРодной город: {self.home_town}'

        info += '\n'
        if self.relation:
            info += f'\nСемейное положение: {self.relation.__str__()}'
        if self.relation_partner:
            info += f'\nПартнёр: {self.relation_partner.__str__()}'

        if self.career:
            info += '\n\nМеста работы:'
        for career in self.career:
            info += f'\n    {" ".join([str(item) for item in career if item])}'

        if self.universities:
            info += '\n\nУниверситеты:'
        for university in self.universities:
            info += f'\n    {university}'

        if self.schools:
            info += '\n\nШколы:'
        for school in self.schools:
            info += f'\n    {school}'

        if self.relatives:
            info += '\n\nРодственники:'
        for relative in self.relatives:
            info += f'\n    {relative[0]}: {relative[1]}'

        return info

    def to_dict(self):
        return {
            'N': self.id,
            'ID': self.id,
            'Name': f'{self.first_name} {self.last_name}',
        }

    def __eq__(self, other):
        return isinstance(other, User) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))