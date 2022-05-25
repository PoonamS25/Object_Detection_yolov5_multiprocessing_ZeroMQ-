import cv2, imutils
import zmq
import base64, time
import queue, threading
import pyshine as ps
import pafy
import youtube_dl

context = zmq.Context()
server_socket = context.socket(zmq.PUSH)
server_socket.bind("tcp://*:5555")
get_url = "https://www.youtube.com/watch?v=ORrrKXGx2SE"
    #get_url = "https://www.youtube.com/watch?v=-d_iBRRVlVE"
path = pafy.new(get_url).streams[0]   #https://youtu.be/uCy5OuSQnyA
#vid = CamGear(source="https://youtu.be/j1GLs_fMn1s", stream_mode= True, logging= True).start()
# camera = True
# if camera == True:
#     vid = cv2.VideoCapture(0)
# else:
#     vid = cv2.VideoCapture('videos/mario.mp4')
vid = cv2.VideoCapture(path.url)

frames_to_count = 20
cnt = 0
fps = 0
st = 0
while True:
    if cnt == frames_to_count:
        try:
            fps = round(frames_to_count/(time.time()-st))
            st = time.time()
            cnt = 0
        except:
            pass
    cnt += 1
    ret, frame = vid.read()
    frame = imutils.resize(frame, width=480)
    encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
    data = base64.b64encode(buffer)
    server_socket.send_pyobj(data)
    text = 'FPS: ' + str(fps)
    source = ps.putBText(frame, text, text_offset_x=20, text_offset_y=30, background_RGB=(10, 20, 222))
    cv2.imshow("Threading_sender_image", frame)
    key = cv2.waitKey(1) & 0xFF
    time.sleep(0.01)
    if key == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()
