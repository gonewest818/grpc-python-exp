from concurrent import futures
import logging

import grpc

import hellostream_pb2
import hellostream_pb2_grpc

logging.basicConfig(format='%(asctime)s:%(name)s : %(message)s', level=logging.DEBUG)


class SpeakerServicer(hellostream_pb2_grpc.SpeakerServicer):
    def getStream(self, request, context):
        logging.info('getStream started %s', request)
        for i in range(10):
            response = hellostream_pb2.Response(message=f'hello {i}', level=i)
            yield response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hellostream_pb2_grpc.add_SpeakerServicer_to_server(SpeakerServicer(), server)
    server.add_insecure_port('localhost:50051')
    server.start()
    logging.debug('server up')
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

