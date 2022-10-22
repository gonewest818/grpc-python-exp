from concurrent import futures
import logging
import queue
import time

import grpc

import hellostream_pb2
import hellostream_pb2_grpc

logging.basicConfig(format='%(asctime)s:%(name)s : %(message)s', level=logging.DEBUG)


class SpeakerServicer(hellostream_pb2_grpc.SpeakerServicer):
    def __init__(self):
        self.client_streams = {}

    def getStream(self, request, context):
        logging.info('getStream started %s', request)

        # make a queue for this client session
        event_queue = queue.SimpleQueue()
        self.client_streams[request.client_id] = event_queue

        # register a callback to cleanup when the client disconnects
        def cleanup():
            logging.debug('cleanup stream for client_id %s', request.client_id)
            if request.client_id in self.client_streams:
                del self.client_streams[request.client_id]

        context.add_callback(cleanup)

        # pull events from the queue and yield to client
        stream_is_terminating = False
        while not stream_is_terminating:
            ev = event_queue.get()
            # for now the queue literally contains protobufs,
            # but in general we could queue the event details
            # and construct the protobuf at the last minute
            yield ev

    def add_event(self, message, level):
        logging.info('new event %s %d for streams %d',
                     message, level, len(self.client_streams))
        event = hellostream_pb2.Response(message=message, level=level)
        for s in self.client_streams.keys():
            self.client_streams[s].put(event)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = SpeakerServicer()
    hellostream_pb2_grpc.add_SpeakerServicer_to_server(servicer, server)
    server.add_insecure_port('localhost:50051')
    server.start()
    logging.debug('server up')

    i = 1
    while True:
        servicer.add_event(f'hello {i}', i)
        i = i + 1
        time.sleep(2)

    server.wait_for_termination()

if __name__ == '__main__':
    serve()

