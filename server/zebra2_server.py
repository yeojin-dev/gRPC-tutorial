import time
from concurrent import futures

import grpc
import requests

from protobuf import zebra_pb2_grpc, zebra_pb2


class Zebra2ServiceServicer(zebra_pb2_grpc.Zebra2ServiceServicer):

    def __init__(self):
        pass

    def Inference(self, request, context):
        print(f'Filepath from request: {request.pixel}')

        # TODO: Zebra2 제거하고 Zebra1 서버에서 tenserflow/serving 도커 이미지에 직접 gRPC 프로토콜로 통신
        data = {'inputs': list(request.pixel)}
        response = requests.post(
            'http://127.0.0.1:8501/v1/models/mnist:predict',
            json=data,
        )

        result = response.json()['outputs'][0]
        number = result.index(max(result))

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
