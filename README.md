# Object_Detection_yolov5_multiprocessing_ZeroMQ-
Sending video files over socket using pyzmq library. I am using Push/Pull patteren to send and receive frames. 

Push and Pull sockets let you distribute messages to multiple workers, arranged in a pipeline. A Push socket will distribute sent messages to its Pull clients evenly. This is equivalent to producer/consumer model but the results computed by consumer are not sent upstream but downstream to another pull/consumer socket.

Data always flows down the pipeline, and each stage of the pipeline is connected to at least one node. When a pipeline stage is connected to multiple nodes data is load-balanced among all connected nodes.

Here I am using threading to process frames and save it into queue.
