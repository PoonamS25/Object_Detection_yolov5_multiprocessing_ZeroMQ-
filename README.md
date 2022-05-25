# Object_Detection_yolov5_multiprocessing_ZeroMQ-
Sending video files over socket using pyzmq library. I am using Push/Pull patteren to send and receive frames. 

Push and Pull sockets let you distribute messages to multiple workers, arranged in a pipeline. A Push socket will distribute sent messages to its Pull clients evenly. This is equivalent to producer/consumer model but the results computed by consumer are not sent upstream but downstream to another pull/consumer socket.

Data always flows down the pipeline, and each stage of the pipeline is connected to at least one node. When a pipeline stage is connected to multiple nodes data is load-balanced among all connected nodes.

Here I am using threading to process frames and save it into queue.

https://sharing.clickup.com/clip/p/t37441271/173bfba1-215e-4c0c-8c68-18ae0c1028f3/screen-recording-2022-05-06-18%3A42.webm?open=true?open=true
