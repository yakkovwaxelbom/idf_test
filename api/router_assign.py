from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status

from services.assign_service import process_assign_from_csv, get_space, get_waiting, search_by_id
# from sqlmodel import Session

from services.file_service import process_file

router = APIRouter(prefix="/assign", tags=["Assign"])


@router.post('/uploadCsv')
# def upload_users_file(file: UploadFile, has_header: bool = True, session: Session = Depends(get_session)):
def upload_users_file(file: UploadFile):
    file_details, error = process_assign_from_csv(file, 'distance')

    if not file_details:
        raise error

    return file_details


@router.get('/space')
def space():
    return get_space()


@router.get('/waitingList')
def waiting_list():
    return get_waiting()

@router.get("/search/{personal_number}")
def search(personal_number: str):
    result = search_by_id(personal_number)

    return result
