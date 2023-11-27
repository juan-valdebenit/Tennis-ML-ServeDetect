import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str = "example email"
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    upload_dir: str = os.path.join(base_dir, 'uploads')
    lstm_bin_size: int = 32
    lstm_threshold: float = 0.9
    # max_frame_process: int = 10000
    sliding_size: int = 15
    serve_distance: int = 5  # seconds
    serve_sequence_length: int = 1
    max_serve_in_sequence: int = 1
    is_clean_local_videos: bool = False

    #AWS
    aws_access_key_id : str = 'your_access_key'
    aws_secret_access_key: str = 'your_secret_key'
    aws_region: str = 'us-east-1'
    aws_s3_bucket: str = 'your_bucket_name'
    is_upload_to_s3: bool = True


settings = Settings()
