import os
from typing import List

import numpy as np
import tensorflow as tf
from tensorflow.keras import layers

from app.config.setting import settings


@tf.keras.utils.register_keras_serializable()
class TransformerBlock(layers.Layer):
    def __init__(self, embed_dim, num_heads, ff_dim, rate=0.1):
        super().__init__()
        self.att = layers.MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim)
        self.ffn = tf.keras.Sequential(
            [layers.Dense(ff_dim, activation="relu"), layers.Dense(embed_dim),]
        )
        self.layernorm1 = layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = layers.LayerNormalization(epsilon=1e-6)
        self.dropout1 = layers.Dropout(rate)
        self.dropout2 = layers.Dropout(rate)

    def call(self, inputs, training):
        attn_output = self.att(inputs, inputs)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)


# 32 sequence and v3_2 and v3_3 good work. v3_2 is best.

lstm_model = tf.keras.models.load_model(settings.lstm_model_path)


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
