from business_logic.dwelling_house import DwellingHouse
from business_logic.soldier import Soldier


class MilitaryBase:

    @staticmethod
    def __validation(dwelling_houses: list[DwellingHouse], soldiers: list[Soldier]):

        if dwelling_houses is not None:
            for i in range(len(dwelling_houses)):
                if not isinstance(dwelling_houses[i], DwellingHouse):
                    return False, f'error in hose NO {i} {dwelling_houses[i]}'

        if soldiers is not None:
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
    def __priority_distance(a: Soldier):
        return a.distance

    soldier_priority_algorithms = {
        'distance': __priority_distance
    }

    def __init__(self, name: str, dwelling_houses: list[DwellingHouse] = None, soldiers: list[Soldier] = None):
        is_valid, error = MilitaryBase.__validation(dwelling_houses, soldiers)
        MilitaryBase.__raise_error(is_valid, error)

        self._name = name
        self._dwelling_houses = dwelling_houses or []
        self._soldiers = soldiers or []

        self._assign_details = None
        self._priority_algorithms = None

    @property
    def dwelling_houses(self):
        return self._dwelling_houses

    @property
    def priority_algorithms(self):
        return self._priority_algorithms

    @priority_algorithms.setter
    def priority_algorithms(self, val):
        self._priority_algorithms = MilitaryBase.soldier_priority_algorithms.get(val)

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

    @property
    def assign_details(self):
        return self._assign_details

    def room_allocation(self):

        for soldier in self._soldiers:
            soldier.placement_status = Soldier.PlacementStatus.WAITING
        self._soldiers.sort(key=self._priority_algorithms, reverse=True)

        result = {}

        house_index = 0
        room_index = 0
        soldier_in_room = 0

        capacity = sum([house.number_rooms * house.number_soldiers_in_room
                        for house in self._dwelling_houses])

        for i in range(min(capacity, len(self._soldiers))):

            soldier = self._soldiers[i]
            house = self._dwelling_houses[house_index]

            if soldier_in_room >= house.number_soldiers_in_room:
                soldier_in_room = 0
                room_index += 1

            if room_index >= house.number_rooms:
                house_index += 1
                room_index = 0
                soldier_in_room = 0
                house = self._dwelling_houses[house_index]

            result[soldier.personal_number] = {
                'house': house.name,
                'room_num': room_index
            }

            soldier_in_room += 1

            soldier.placement_status = Soldier.PlacementStatus.ASSIGNED

        self._assign_details = result
        return result

    def house_info(self):
        num_assigns_in_houses = {houses.name: [0 for _ in range(houses.number_rooms)] for
                                 houses in self._dwelling_houses}

        for assign in self.assign_details.values():
            num_assigns_in_houses[assign['house']][assign['room_num']] += 1

        result = {}

        for house in self._dwelling_houses:
            house_name = house.name
            capacity = house.number_soldiers_in_room
            num_rooms = house.number_rooms

            room_assign_counts = num_assigns_in_houses[house_name]

            full_rooms = sum(1 for count in room_assign_counts if count == capacity)
            empty_rooms = sum(1 for count in room_assign_counts if count == 0)

            result[house_name] = {
                'full_rooms': full_rooms,
                'empty_rooms': empty_rooms,
                'partial': num_rooms - full_rooms - empty_rooms
            }

        return result

    def waiting_list(self):
        waiting = [
            soldier for soldier in self._soldiers
            if soldier.personal_number not in self._assign_details
        ]
        waiting.sort(key=self._priority_algorithms, reverse=True)

        return [s.to_dict() for s in waiting]

    def search_by_personal_number(self, personal_number):
        for soldier in self._soldiers:
            if soldier.personal_number == personal_number:
                return {**soldier.to_dict(), **self.assign_details.get(personal_number, {})}


a = DwellingHouse('a', 8, 10)
b = DwellingHouse('b', 8, 10)

seven_harvests = MilitaryBase('The Seven Harvests', [a, b])
