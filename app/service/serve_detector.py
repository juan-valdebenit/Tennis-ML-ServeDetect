import os
from typing import List

import numpy as np
import tensorflow as tf
import cv2

from app.config.setting import settings

# 32 sequence and v3_2 and v3_3 good work. v3_2 is best.
lstm_model_path = os.path.join(settings.root_dir, 'models/lstm_model_32_v3_2.h5')
lstm_model = tf.keras.models.load_model(lstm_model_path)


def get_keypoints(results):
    all_results_nor = []
    for result in results:
        conf = result.keypoints.conf.cpu().numpy()
        xyn = result.keypoints.xyn.cpu().numpy()
        index = 0  # first index is max confidence
        keypoints_nor = np.hstack((xyn[index].reshape(-1, 2), conf[index].reshape(-1, 1))).flatten()
        all_results_nor.append(keypoints_nor)
    all_results_nor = np.array(all_results_nor).reshape(-1, settings.lstm_bin_size, 51)

    return all_results_nor


def get_serve_predict(annotated_frames: List) -> bool:
    normalize_keypoints = get_keypoints(annotated_frames)
    lstm_model_result = lstm_model.predict(normalize_keypoints, verbose=False)
    is_serve = lstm_model_result[0][1] >= settings.lstm_threshold

    return is_serve
