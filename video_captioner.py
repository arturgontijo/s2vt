import os
import logging
from pytube import YouTube

from utils.extract_features import extractor
from utils.s2vt_captioner import get_captions
from utils.video_tools import get_video_frames

logging.basicConfig(level=10, format="%(asctime)s - [%(levelname)8s] - %(name)s - %(message)s")
log = logging.getLogger("video_cap_service")


def download_yt_video(url, video_folder, video_name):
    try:
        video_path = YouTube(url).streams.filter(
            progressive=True,
            file_extension='mp4').order_by('resolution').desc().first().download(
            output_path=video_folder,
            filename=video_name)
        log.debug("Video stored at: {}".format(video_path))
        return True, video_path
    except Exception as e:
        print(e)
        return False, 'Fail!'


def main(url='https://www.youtube.com/watch?v=GwowU444Ky8',
         video_name='civic',
         start_time=0,
         stop_time=0,
         pace=0,
         batch_size=0):
    video_folder = './utils/videos/{}'.format(video_name)
    if not os.path.exists('./utils/videos'):
        os.makedirs('./utils/videos')
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)
    ok, video_path = download_yt_video(url, video_folder, video_name)
    if ok:
        ok, frames_list = get_video_frames(video_path, video_folder, start_time*1000, stop_time*1000, pace)
        if ok:
            # If batch_size == 0, use length of frame_list
            if batch_size == 0:
                batch_size = len(frames_list)
                if batch_size > 50:
                    log.error('batch_size is too high!')
                    return False

            features_file = '{}/output_{}.csv'.format(video_folder, video_name)
            if extractor('utils/data/VGG_ILSVRC_16_layers.caffemodel',
                         'utils/data/vgg_orig_16layer.deploy.prototxt',
                         frames_list,
                         features_file,
                         batch_size):
                model_name = 's2vt_vgg_rgb'
                output_path = '{}/{}_captions'.format(video_folder, video_name)
                get_captions(model_name, features_file, output_path)
    return True


if __name__ == "__main__":
    i_url = raw_input("   URL   : ")
    i_video_name = raw_input("VID Name : ")
    i_start_time = raw_input("StartTime: ")
    i_stop_time = raw_input("StopTime : ")
    i_pace = raw_input("Pace(ms) : ")
    i_batch_size = raw_input("BatchSize: ")
    if "" not in [i_url, i_video_name, i_start_time, i_stop_time]:
        main(i_url, i_video_name, int(i_start_time), int(i_stop_time), int(i_pace), int(i_batch_size))
    else:
        main()
