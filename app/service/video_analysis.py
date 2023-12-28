import os

import cv2

from app.config.setting import settings
from app.service.pose_generator import get_poses
from app.service.serve_detector import get_serve_predict
from app.service.video_written import write_and_upload_video


def analysis_video(video_path: str, output_path: str):
    filename_without_extension, _ = os.path.splitext(os.path.basename(video_path))
    print(f"Processing file: {filename_without_extension}")

    cap = cv2.VideoCapture(video_path)
    # Get the original video's frame width and height
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    frame_rate = int(cap.get(5))

    # Initialize storage and tracker
    output_file_list = []
    raw_frame = []
    batch_annotated_frame = []
    serve_list = []
    total_serve = 0
    serve_count = 0
    last_serve_frame = 0
    total_frame = -1

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        raw_frame.append(frame)
        total_frame += 1

        if total_frame % 1000 == 0:
            print(f"Frame proces: {total_frame}")

        if total_frame % settings.frame_inverse_ratio != 0:
            continue

        # annotate frame
        annotation, is_pose_found = get_poses(frame)
        if is_pose_found: batch_annotated_frame.append(annotation)

        if len(batch_annotated_frame) < settings.lstm_bin_size:
            continue

        # predict sequence of frame.
        is_serve = get_serve_predict(batch_annotated_frame)
        # prepare for next slide.
        batch_annotated_frame = batch_annotated_frame[settings.sliding_size:]

        if is_serve or len(serve_list) > 0: serve_list.append(is_serve)

        if len(serve_list) < settings.serve_sequence_length:
            # continue for gathering more data
            continue

        is_actual_serve = sum(serve_list) >= settings.max_serve_in_sequence
        serve_list = []  # clean serve list for next

        if is_actual_serve and (((total_frame - last_serve_frame) > (settings.serve_distance * frame_rate)) or total_serve <= 0):
            print(f"Total frame: {total_frame} || Last serve frame : {last_serve_frame} || Distance : {settings.serve_distance * frame_rate} ||"
                  f"Actual distance: {(total_frame - last_serve_frame)}")
            # if is_actual_serve:
            serve_count += 1
            total_serve += 1
            print(f"Current serve count: {total_serve}")

            if serve_count == 1:
                last_serve_frame = max(0, total_frame - int(frame_rate * 1.5))
                end_frame = len(raw_frame) - int(frame_rate * 3)
            else:
                end_frame = len(raw_frame) - int(frame_rate * 3)
                writeable_frames = raw_frame[:end_frame]

                # Reset serve counter...
                serve_count = 1
                last_serve_frame = total_frame - int(frame_rate * 3)

                video_output_path = os.path.join(output_path,
                                                 f"{filename_without_extension}_{total_serve - 1}.mp4")
                write_and_upload_video(
                    video_output_path,
                    frame_width,
                    frame_height,
                    frame_rate,
                    writeable_frames
                )
                output_file_list.append(video_output_path)

            raw_frame = raw_frame[end_frame:]

    cap.release()
    return output_file_list
