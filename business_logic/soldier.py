from enum import Enum


class Soldier:
    class PlacementStatus(Enum):
        ASSIGNED = 0,
        WAITING = 1

    MASK_PERSONAL_NUMBER = 8 * 10 ** 7
    SIZE_PERSONAL_NUMBER = 8

    GENDER = ['male', 'female']

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
        if (personal_number & Soldier.MASK_PERSONAL_NUMBER != Soldier.MASK_PERSONAL_NUMBER) and len(
                str(personal_number)) != Soldier.SIZE_PERSONAL_NUMBER:
            return False, f"personal_number={personal_number}"

        if gender not in Soldier.GENDER:
            return False, f"gender={gender}"

        if not isinstance(distance, (int, float)):
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

    def __str__(self):
        return '\n'.join([f'{k}: {v}' for k, v in self.to_dict().items()])
