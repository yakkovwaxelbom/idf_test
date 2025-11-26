from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status

from services.assign_service import process_assign_from_csv
# from sqlmodel import Session

from services.file_service import process_file

router = APIRouter(prefix="/assign", tags=["Assign"])


@router.post("/uploadCsv")
# def upload_users_file(file: UploadFile, has_header: bool = True, session: Session = Depends(get_session)):
def upload_users_file(file: UploadFile):
    file_details, error = process_assign_from_csv(file, 'distance')

    if not file_details:
        raise error

    return file_details
