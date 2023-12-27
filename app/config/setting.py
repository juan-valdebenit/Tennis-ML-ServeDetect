import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str = "example email"
    root_dir: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    base_dir: str = os.path.join(root_dir, 'app')
    statis_dir: str = os.path.join(root_dir, 'static')
    upload_dir: str = os.path.join(statis_dir, 'uploads')
    thumbnail_dir: str = os.path.join(statis_dir, 'thumbnails')
    lstm_bin_size: int = 24
    frame_inverse_ratio: int = 3
    lstm_threshold: float = 0.5
    # max_frame_process: int = 10000
    sliding_size: int = 5
    serve_distance: int = 5+3  # seconds [padding 3 seconds]
    serve_sequence_length: int = 1
    max_serve_in_sequence: int = 1
    is_clean_local_videos: bool = False

    # AWS
    aws_access_key_id: str = 'your_access_key'
    aws_secret_access_key: str = 'your_secret_key'
    aws_region: str = 'us-east-1'
    aws_s3_bucket_input: str = 'your_bucket_name'
    aws_s3_bucket_output: str = 'your_bucket_name'
    is_upload_to_s3: bool = False

    # Model
    lstm_model_name: str = 'lstm_model_24_s2_v1_15.keras'
    lstm_model_path: str = os.path.join(root_dir, 'models', lstm_model_name)


settings = Settings()
