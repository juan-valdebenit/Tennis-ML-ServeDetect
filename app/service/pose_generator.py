import os.path
from typing import List

from ultralytics import YOLO
import numpy as np
import tensorflow as tf
import cv2

from app.config.setting import settings

pose_model = YOLO('yolov8n-pose.pt')


def get_modified_frame(frame):
    # 720*1080
    resized_image = cv2.resize(frame, (1280, 720))
    ## (0,0) top left
    # h*w*c
    crop_frame = resized_image[200:-50, 250:-250, :]
    resized_image = cv2.resize(crop_frame, (640, 640))
    return resized_image


def get_poses_batch(frames: List[np.ndarray]) -> List:
    results = []
    for frame in frames:
        modified_frame = get_modified_frame(frame)
        result = pose_model.predict(modified_frame, verbose=False)
        results.append(result[0])

    return results


def get_poses(frame: np.ndarray):
    modified_frame = get_modified_frame(frame)
    result = pose_model.predict(modified_frame, verbose=False)[0]

    found_pose = True
    if result.boxes.shape[0] == 0:
        found_pose = False

    return result, found_pose
