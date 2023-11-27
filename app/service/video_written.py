import cv2


def write_and_upload_video(
                        video_output_path,
                        frame_width,
                        frame_height,
                        frame_rate,
                        writeable_frames
                    ):
    print(f"Writing video: {video_output_path}...")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_output_path, fourcc, frame_rate, (frame_width, frame_height))

    for frame in writeable_frames:
        out.write(frame)

    out.release()


