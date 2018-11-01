import logging
from pytube import YouTube

logging.basicConfig(level=10, format="%(asctime)s - [%(levelname)8s] - %(name)s - %(message)s")
log = logging.getLogger("run_video_cap_service")


def download_yt_video(url, video_path):
    try:
        video_path = YouTube(url).streams.first().download(output_path="/", filename=video_path)
        log.info("Video stored at: ", video_path)
        return True
    except Exception as e:
        print(e)
        return False


def main():

    return


if __name__ == "__main__":
    main()
