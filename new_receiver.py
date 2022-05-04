import cv2
import zmq
import base64
import numpy as np,time
import pyshine as ps
from multiprocessing import Process
import torch, random, threading, queue
import matplotlib.pyplot as plt

import os

# fourcc = cv2.VideoWriter_fourcc(*'mpv4')
# output = cv2.VideoWriter('/Image/output_file.mp4', fourcc, 20.0, (640, 640))
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
classes = model.names

def score_frame(frame):
    """
    Takes a single frame as input, and scores the frame using yolo5 model.
    :param frame: input frame in numpy/list/tuple format.
    :return: Labels and Coordinates of objects detected by model in the frame.
    """
    model.to(device)
    frame = [frame]
    detects = model(frame)
    labels, cord = detects.xyxyn[0][:, -1], detects.xyxyn[0][:, :-1]
    return labels, cord


def class_to_label(x):
    """
    For a given label value, return corresponding string label.
    :param x: numeric label
    :return: corresponding string label
    """
    return classes[int(x)]


def plot_boxes(results, frame):
    """
    Takes a frame and its results as input, and plots the bounding boxes and label on to the frame.
    :param results: contains labels and coordinates predicted by model on the given frame.
    :param frame: Frame which has been scored.
    :return: Frame with bounding boxes and labels ploted on it.
    """
    labels, cord = results
    n = len(labels)
    x_shape, y_shape = frame.shape[1], frame.shape[0]
    for i in range(n):
        row = cord[i]
        if row[4] >= 0.3:
            x1, y1, x2, y2 = int(row[0] * x_shape), int(row[1] * y_shape), int(row[2] * x_shape), int(row[3] * y_shape)
            bgr = (0, 255, 0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
            cv2.putText(frame, class_to_label(labels[i]), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)
    return frame

def detection(source):
    results = score_frame(source)
    frame = plot_boxes(results, source)
    #output.write(frame)
    return frame




context = zmq.Context()
client_socket = context.socket(zmq.PULL)
client_socket.connect("tcp://localhost:5555")
#client_socket.setsockopt_string(zmq.SUBSCRIBE,optval='')
fps=0
st=0
frames_to_count=20
cnt=0

def pyshine_video_queue():
    frame = [0]
    q = queue.Queue(maxsize=10)
    print("function1")
    def getAudio():
        while True:

            try:
                new_frame = detection(source)

                q.put(new_frame)
            except:
                pass

    thread = threading.Thread(target=getAudio, args=())
    thread.start()
    return q


q = pyshine_video_queue()
while True:
    if cnt == frames_to_count:
        try:
            fps = round(frames_to_count/(time.time()-st))
            st = time.time()
            cnt=0
        except:
            pass
    cnt+=1
    frame = client_socket.recv_pyobj()
    img = base64.b64decode(frame)
    npimg = np.frombuffer(img, dtype=np.uint8)
    source = cv2.imdecode(npimg, 1)
    new_frame = q.get()
    text = 'FPS: ' + str(fps)
    source = ps.putBText(new_frame, text, text_offset_x=20, text_offset_y=30, background_RGB=(10, 20, 222))
    time.sleep(0.01)
    cv2.imshow("Threading_receiver_image", source)
    key = cv2.waitKey(1) & 0xFF
    time.sleep(0.01)
    if key == ord('q'):
        break

cv2.destroyAllWindows()