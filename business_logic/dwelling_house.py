NUMBER_ROOMS = 10
NUMBER_SOLDIERS_IN_ROOM = 8


class DwellingHouse:
    def __init__(self, name: str, number_rooms: int = NUMBER_ROOMS,
                 number_soldiers_in_room: int = NUMBER_SOLDIERS_IN_ROOM
                 ):
        self._name = name
        self._number_rooms = number_rooms
        self._number_soldiers_in_room = number_soldiers_in_room

    @property
    def name(self):
        return self._name

    @property
    def number_rooms(self):
        return self._number_rooms

    @property
    def number_soldiers_in_room(self):
        return self._number_soldiers_in_room

    def to_dict(self):
        return {
            'name': self._name,
            'number_rooms': self._number_rooms,
            'number_soldiers_in_room': self._number_soldiers_in_room
        }

    def __str__(self):
        return '\n'.join([f'{k}: {v}' for k, v in self.to_dict().items()])
