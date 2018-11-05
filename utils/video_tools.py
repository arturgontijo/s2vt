import logging
import cv2

logging.basicConfig(level=10, format="%(asctime)s - [%(levelname)8s] - %(name)s - %(message)s")
log = logging.getLogger("video_tools")


def get_video_frames(video_path, frames_path, start_time_ms, stop_time_ms):
    try:
        cap = cv2.VideoCapture(video_path)
        # Set video to start position
        cap.set(cv2.CAP_PROP_POS_MSEC, start_time_ms)

        frames_list = []
        ok = True
        current_frame = 1
        while ok and cap.get(cv2.CAP_PROP_POS_MSEC) <= stop_time_ms:
            ok, frame = cap.read()
            if not ok:
                break
            frame_path = '{}/frame_{:03}.jpg'.format(frames_path, current_frame)
            log.debug('Storing ' + frame_path)
            cv2.imwrite(frame_path, frame)
            frames_list.append(frame_path)
            current_frame += 1
            # FPS = 1
            cap.set(cv2.CAP_PROP_POS_MSEC, cap.get(cv2.CAP_PROP_POS_MSEC) + 1000)

        cap.release()
        cv2.destroyAllWindows()
        return True, frames_list
    except Exception as e:
        print e
        return False, []
