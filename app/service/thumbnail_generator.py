import os.path

import ffmpeg
import sys

def generate_thumbnail(in_filename, out_filename):
    probe = ffmpeg.probe(in_filename)
    time = float(probe['streams'][0]['duration']) // 2
    width = probe['streams'][0]['width']
    try:
        (
            ffmpeg
            .input(in_filename, ss=time)
            .filter('scale', width, -1)
            .output(out_filename, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        print(e.stderr.decode(), file=sys.stderr)


def get_thumbnails_path(video_clip_file_list, thumbnail_path):
    thumbnail_image_list = []
    try:
        for file_name in video_clip_file_list:
            filename_without_extension, _ = os.path.splitext(os.path.basename(file_name))
            file_base_name = f'{filename_without_extension}.jpg'
            outfile = os.path.join(thumbnail_path, file_base_name)
            generate_thumbnail(file_name, outfile)

            static_path = os.path.join('static', outfile.split(f'static{os.sep}')[-1])
            thumbnail_image_list.append(static_path)

    except Exception as err:
        print(err)

    return thumbnail_image_list
