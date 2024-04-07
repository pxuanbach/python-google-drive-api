import io
import os
from datetime import datetime
from mimetypes import MimeTypes


def read_file_content(file_path: str):
    with open(file_path, 'rb') as file:
        content = file.read()
    return io.BytesIO(content)


def get_local_file_metadata(file_path: str):
    file_name = os.path.basename(file_path)

    mime = MimeTypes()
    mime_type, _ = mime.guess_type(file_path)

    file_size = os.path.getsize(file_path)

    created_time = os.path.getctime(file_path)
    modified_time = os.path.getmtime(file_path)
    created_time_str = datetime.fromtimestamp(created_time).isoformat() + 'Z'
    modified_time_str = datetime.fromtimestamp(modified_time).isoformat() + 'Z'

    metadata = {
        'name': file_name,
        'mimeType': mime_type,
        'size': file_size,
        'createdTime': created_time_str,
        'modifiedTime': modified_time_str
    }
    return metadata