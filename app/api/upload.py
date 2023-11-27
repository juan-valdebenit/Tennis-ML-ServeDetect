import os.path
from uuid import uuid4

from fastapi import APIRouter, File, UploadFile

from app.config.setting import settings
from app.service.file_utils import delete_folder
from app.service.s3_file_uploader import upload_folder_to_s3
from app.service.video_analysis import analysis_video

router = APIRouter()


@router.post("/upload-file/")
async def create_upload_file(file: UploadFile = File(...)):
    # Generate a unique folder name using uuid4
    folder_name = str(uuid4())
    folder_path = os.path.join(settings.upload_dir, folder_name)

    # Create the folder
    os.makedirs(folder_path)

    # Save the uploaded file to the folder
    file_path = os.path.join(folder_path, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    file_list = analysis_video(file_path, folder_path)
    os.remove(file_path)

    s3_file_list=None
    if settings.is_upload_to_s3:
        filename_without_extension, _ = os.path.splitext(os.path.basename(file_path))
        s3_file_list = upload_folder_to_s3(folder_path, settings.aws_s3_bucket, filename_without_extension)


    if settings.is_clean_local_videos:
        delete_folder(folder_path)

    if s3_file_list:
        return {"file_paths": s3_file_list}

    return {"file_paths": file_list}
