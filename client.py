import logging

import grpc

import hellostream_pb2
import hellostream_pb2_grpc

logging.basicConfig(format='%(asctime)s:%(name)s : %(message)s', level=logging.DEBUG)

socket = 'localhost:50051'
channel = grpc.insecure_channel(socket)
client = hellostream_pb2_grpc.SpeakerStub(channel)
logging.info("Connected to the Server %s", socket)


request = hellostream_pb2.OpenStream(client_id="foo")
response = client.getStream(request)
for item in response:
    logging.info("item received %s", item)
