import os.path
from uuid import uuid4

from fastapi import APIRouter, File, UploadFile

from app.config.setting import settings
from app.service.file_utils import delete_folder
from app.service.s3_file_uploader import upload_folder_to_s3, upload_single_file_to_s3
from app.service.thumbnail_generator import get_thumbnails_path
from app.service.video_analysis import analysis_video

router = APIRouter()


@router.post("/upload-file/")
async def create_upload_file(file: UploadFile = File(...)):
    # Generate a unique folder name using uuid4
    folder_name = str(uuid4())
    upload_path = os.path.join(settings.upload_dir, folder_name)
    thumbnail_path = os.path.join(settings.thumbnail_dir, folder_name)

    # Create the folder
    os.makedirs(upload_path, exist_ok=True)
    os.makedirs(thumbnail_path, exist_ok=True)

    # Save the uploaded file to the folder
    file_path = os.path.join(upload_path, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    ## upload main_file in s3
    if settings.is_upload_to_s3:
        upload_single_file_to_s3(file_path, settings.aws_s3_bucket_input)

    video_clip_file_list = analysis_video(file_path, upload_path)
    # Remove main file.
    os.remove(file_path)

    # upload video clip to s3
    s3_file_list = None
    if settings.is_upload_to_s3:
        filename_without_extension, _ = os.path.splitext(os.path.basename(file_path))
        s3_file_list = upload_folder_to_s3(upload_path, settings.aws_s3_bucket_output, filename_without_extension)

    thumbnail_path = get_thumbnails_path(video_clip_file_list, thumbnail_path)

    if settings.is_upload_to_s3 and settings.is_clean_local_videos:
        delete_folder(upload_path)
    video_file_path = []
    if s3_file_list:
        video_file_path = s3_file_list
    else:
        for file_name in video_clip_file_list:
            static_path = os.path.join('static', file_name.split(f'static{os.sep}')[-1])
            video_file_path.append(static_path)

    return {"file_paths": video_file_path, "thumbnail_paths": thumbnail_path}
