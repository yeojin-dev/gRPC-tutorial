import time
from concurrent import futures

import grpc

from protobuf import zebra_pb2_grpc, zebra_pb2


class Zebra1ServiceServicer(zebra_pb2_grpc.Zebra1ServiceServicer):

    def __init__(self):
        pass

    def Recognize(self, request, context):
        # TODO: image pre-processing
        print(f'Filepath from request: {request.filepath}')
        print(f'File stream from request: {request.file_stream}')

        with grpc.insecure_channel('localhost:60000') as channel:
            stub = zebra_pb2_grpc.Zebra2ServiceStub(channel)
            req_message = zebra_pb2.ReqMessage(filepath=request.filepath, file_stream=request.file_stream)
            response = stub.Inference(req_message)
            res_message = zebra_pb2.ResMessage(number=response.number)

        return res_message


if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    zebra_pb2_grpc.add_Zebra1ServiceServicer_to_server(Zebra1ServiceServicer(), server)

    server.add_insecure_port('[::]:50000')
    server.start()

    print('Starting zebra1 server...')

    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        server.stop(0)
