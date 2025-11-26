import csv
import io
import json
from fastapi import UploadFile
from typing import Dict


def process_file(file: UploadFile, has_header: bool = True) -> Dict:
    content_type = file.content_type
    filename = file.filename

    content_bytes = file.file.read()

    status = 200
    header = None

    # CSV
    if content_type == "text/csv" or filename.endswith(".csv"):

        content_str = content_bytes.decode("utf-8")
        reader = csv.reader(io.StringIO(content_str))

        header = next(reader) if has_header else None
        data = list(reader)

    # JSON
    elif content_type == "application/json" or filename.endswith(".json"):

        content_str = content_bytes.decode("utf-8")
        data = json.loads(content_str)

    else:
        data = None
        status = 404

    return {
        "filename": filename,
        "content_type": content_type,
        "header": header,
        "data": data,
        "status": status
    }
