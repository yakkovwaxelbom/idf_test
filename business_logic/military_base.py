from business_logic.dwelling_house import DwellingHouse
from business_logic.soldier import Soldier


class MilitaryBase:

    @staticmethod
    def __validation(dwelling_houses: list[DwellingHouse], soldiers: list[Soldier]):

        for i in range(len(dwelling_houses)):
            if not isinstance(dwelling_houses[i], DwellingHouse):
                return False, f'error in hose NO {i} {dwelling_houses[i]}'

        for i in range(len(soldiers)):
            if not isinstance(soldiers[i], Soldier):
                return False, f'error in soldiers NO {i} {soldiers[i]}'

        return True, None

    @staticmethod
    def __raise_error(is_valid, error):
        if not is_valid:
            raise ValueError(error)

    # Soldier priority algorithms

    @staticmethod
    def __priority_distance(a: Soldier, b: Soldier):
        return a.distance >= b.distance

    soldier_priority_algorithms = {
        'distance': __priority_distance
    }

    def __init__(self, dwelling_houses: list[DwellingHouse], soldiers: list[Soldier]):
        is_valid, error = MilitaryBase.__validation(dwelling_houses, soldiers)
        MilitaryBase.__raise_error(is_valid, error)

        self._dwelling_houses = dwelling_houses
        self._soldiers = soldiers

    @property
    def dwelling_houses(self):
        return self._dwelling_houses

    def add_dwelling_houses(self, houses: list[DwellingHouse]):
        is_valid, error = MilitaryBase.__validation(houses, [])
        MilitaryBase.__raise_error(is_valid, error)
        self._dwelling_houses.extend(houses)

    @property
    def soldiers(self):
        return self._soldiers

    def add_soldiers(self, soldiers: list[Soldier]):
        is_valid, error = self.__validation([], soldiers)
        self.__raise_error(is_valid, error)
        self._soldiers.extend(soldiers)

    def room_allocation(self, priority_algorithm):
        self._soldiers.sort(key=priority_algorithm, reverse=True)

        result = []

        house_index = 0
        room_index = 0
        soldier_in_room = 0

        for soldier in self._soldiers:

            house = self._dwelling_houses[house_index]

            if soldier_in_room >= house.number_soldiers_in_room:
                soldier_in_room = 0
                room_index += 1

            if room_index >= house.number_rooms:
                house_index += 1
                room_index = 0
                soldier_in_room = 0
                house = self._dwelling_houses[house_index]

            result.append({
                'personal_number': soldier.personal_number,
                'house': house.name,
                'room_num': room_index
            })

            soldier_in_room += 1

        return result
