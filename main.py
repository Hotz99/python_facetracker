from face_landmarker import FaceLandmarker
from face_detector import FaceDetector
import sys
import os

UDP_RECEIVER_IP = None
UDP_RECEIVER_PORT = None 

# arbitrary video file for performance testing
SAMPLE_VIDEO_FILE = None 

# https://ai.google.dev/edge/api/mediapipe/python/mp/tasks/vision/FaceLandmarker
LANDMARKER_TASK_FILE = "./models/face_landmarker.task"
FACE_LANDMARKER_LOG_FILE = "../perf_metrics/logs/python_face_landmarker_log.txt"

# https://ai.google.dev/edge/api/mediapipe/python/mp/tasks/vision/FaceDetector
FACE_DETECTOR_FILE = "./models/blaze_face_short_range.tflite"
FACE_DETECTOR_LOG_FILE = "../perf_metrics/logs/python_face_detector_log.txt"

# optional delay between frames in seconds
FRAME_DELAY_SECS = None

def main():
    model = sys.argv[1] if len(sys.argv) > 1 else "landmarker"
    perf_mode = len(sys.argv) > 2 and sys.argv[2] == "perf"
    video_file = SAMPLE_VIDEO_FILE if perf_mode else None

    if perf_mode and not video_file:
        print("error: performance mode requires a video file")
        sys.exit(1)

    try:
        if model == "landmarker":
            if FACE_LANDMARKER_LOG_FILE and os.path.exists(FACE_LANDMARKER_LOG_FILE):
                os.remove(FACE_LANDMARKER_LOG_FILE)
            landmarker = FaceLandmarker(UDP_RECEIVER_IP, UDP_RECEIVER_PORT, LANDMARKER_TASK_FILE, video_file, FACE_LANDMARKER_LOG_FILE, FRAME_DELAY_SECS)
            try:
                landmarker.run()
            except KeyboardInterrupt:
                landmarker.stop()
        elif model == "detector":
            if FACE_DETECTOR_LOG_FILE and os.path.exists(FACE_DETECTOR_LOG_FILE):
                os.remove(FACE_DETECTOR_LOG_FILE)
            detector = FaceDetector(UDP_RECEIVER_IP, UDP_RECEIVER_PORT, FACE_DETECTOR_FILE, video_file, FACE_DETECTOR_LOG_FILE, FRAME_DELAY_SECS)
            try:
                detector.run()
            except KeyboardInterrupt:
                detector.stop()
        else:
            print("invalid model: use 'landmarker' or 'detector'")
    except Exception as e:
        print(f"error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
