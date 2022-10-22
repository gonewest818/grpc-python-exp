import logging
import uuid

import grpc

import hellostream_pb2
import hellostream_pb2_grpc

logging.basicConfig(format='%(asctime)s:%(name)s : %(message)s', level=logging.DEBUG)

socket = 'localhost:50051'
channel = grpc.insecure_channel(socket)
client = hellostream_pb2_grpc.SpeakerStub(channel)
logging.info("Connected to the Server %s", socket)
client_id = str(uuid.uuid4())
logging.info("My id is %s", client_id)

request = hellostream_pb2.OpenStream(client_id=client_id)
response = client.getStream(request)
for item in response:
    logging.info("item received %s", item)
