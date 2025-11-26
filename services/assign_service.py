from fastapi import UploadFile, HTTPException, status

from services.file_service import process_file
from business_logic.military_base import seven_harvests, MilitaryBase
from business_logic.soldier import Soldier

fields = ['personal_number', 'first_name', 'last_name', 'gender', 'city', 'distance']
hebrew_fields = {'מספר אישי': 'personal_number', 'שם פרטי': 'first_name', 'שם משפחה': 'last_name', 'מין': 'gender',
                 'עיר מגורים': 'city', 'מרחק מהבסיס': 'distance'}


def validate_headers(header, hebrew_fields, fields):
    if set(header) == set(hebrew_fields.keys()):
        header = [hebrew_fields[h] for h in header]

    if header != fields:
        return None, HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="headers not valid"
        )

    return header, None


def validate_algorithm(algorithm, priority_algorithms):
    algorithm_func = priority_algorithms.get(algorithm)
    if not algorithm_func:
        return False, HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="algorithm not valid"
        )

    seven_harvests.priority_algorithms = algorithm

    return False, None


def parse_soldiers(records):
    soldiers = []
    for record in records:
        try:
            soldier = Soldier(**record)
            soldiers.append(soldier)
        except Exception as e:
            print("Soldier parsing failed:", e, record)
            continue
    return soldiers


def create_assign_result(military_base, assign_details):
    settlements_num = len(assign_details.keys())

    soldiers_details = []
    for soldier in military_base.soldiers:

        soldier_info = soldier.to_dict()

        if soldier.placement_status == Soldier.PlacementStatus.ASSIGNED:
            soldier_info = {**soldier_info, **assign_details[soldier.personal_number]}

        soldiers_details.append(soldier_info)

    return {
        "Number of settlements": settlements_num,
        "Number of soldiers waiting": len(military_base.soldiers) - settlements_num,
        "soldiers_details": soldiers_details
    }


def process_assign_from_csv(file: UploadFile, algorithm):
    file_details = process_file(file)

    header, error = validate_headers(
        file_details["header"],
        hebrew_fields,
        fields
    )
    if error:
        return None, error

    res, error = validate_algorithm(
        algorithm,
        MilitaryBase.soldier_priority_algorithms
    )
    if error:
        return None, error

    file_details["data"] = [dict(zip(header, row)) for row in file_details["data"]]

    soldiers = parse_soldiers(file_details["data"])

    seven_harvests.add_soldiers(soldiers)
    assign_details = seven_harvests.room_allocation()

    res = create_assign_result(seven_harvests, assign_details)

    return res, error


def get_space():
    return seven_harvests.house_info()


def get_waiting():
    return seven_harvests.waiting_list()


def search_by_id(id):
    return seven_harvests.search_by_personal_number(id)
