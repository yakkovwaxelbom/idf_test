from enum import Enum


class Soldier:
    class PlacementStatus(Enum):
        ASSIGNED = 0,
        WAITING = 1

    GENDER = ['male', 'female', 'זכר', 'נקבה']

    def __init__(self, personal_number: int, first_name: str, last_name: str, gender: str, city: str

                 , distance: float, placement_status: PlacementStatus = PlacementStatus.WAITING):
        is_valid, error = Soldier.__validation(personal_number, gender, distance)

        if not is_valid:
            raise ValueError(error)

        self._personal_number = personal_number
        self._first_name = first_name
        self._last_name = last_name
        self._gender = gender
        self._city = city
        self._distance = distance
        self._placement_status = placement_status

    @classmethod
    def __validation(cls, personal_number, gender, distance):
        if personal_number[0] != '8':
            return False, f"personal_number={personal_number}"

        if gender not in Soldier.GENDER:
            return False, f"gender={gender}"

        if not distance.isdigit():
            return False, f"distance={distance}"
        return True, None

    def to_dict(self):
        return {
            'personal_number': self._personal_number,
            'first_name': self._first_name,
            'last_name': self._last_name,
            'gender': self._gender,
            'city': self._city,
            'distance': self._distance,
            'placement_status': self._placement_status.name.lower()
        }

    @property
    def personal_number(self):
        return self._personal_number


    @property
    def distance(self):
        return self._distance

    @property
    def placement_status(self):
        return self._placement_status

    @placement_status.setter
    def placement_status(self, val):
        if isinstance(val, Soldier.PlacementStatus):
            self._placement_status = val

    def __str__(self):
        return '\n'.join([f'{k}: {v}' for k, v in self.to_dict().items()])
