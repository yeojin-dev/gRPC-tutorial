import time
from concurrent import futures
import random

import grpc

from protobuf import zebra_pb2_grpc, zebra_pb2


class Zebra2ServiceServicer(zebra_pb2_grpc.Zebra2ServiceServicer):

    def __init__(self):
        pass

    def Inference(self, request, context):
        # TODO: OCR
        number = random.randint(1, 100)
        print(f'Filepath from request: {request.filepath}')
        print(f'Result: {number}')

        res_message = zebra_pb2.ResMessage(number=number)

        return res_message


if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    zebra_pb2_grpc.add_Zebra2ServiceServicer_to_server(Zebra2ServiceServicer(), server)

    server.add_insecure_port('[::]:60000')
    server.start()

    print('Starting zebra2 server...')

    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        server.stop(0)
