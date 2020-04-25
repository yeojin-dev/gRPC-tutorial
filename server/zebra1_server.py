import time
from concurrent import futures

import grpc
import tensorflow as tf

from protobuf import zebra_pb2_grpc, zebra_pb2


class Zebra1ServiceServicer(zebra_pb2_grpc.Zebra1ServiceServicer):

    def __init__(self):
        pass

    def Recognize(self, request, context):
        print(f'Filepath from request: {request.filepath}')
        print(f'File stream from request: {request.file_stream}')

        img_tensor = self.get_flatten_image_tensor(request.stream)

        with grpc.insecure_channel('localhost:60000') as channel:
            stub = zebra_pb2_grpc.Zebra2ServiceStub(channel)
            image_req_message = zebra_pb2.ImageReqMessage(pixel=img_tensor)
            response = stub.Inference(image_req_message)
            res_message = zebra_pb2.ResMessage(number=response.number)

        return res_message

    @staticmethod
    def get_flatten_image_tensor(stream: bytes) -> tf.Tensor:
        img_grayscale = tf.image.decode_png(stream, channels=1)
        img_resized = tf.image.resize(img_grayscale, [28, 28])
        img_casted = tf.cast(img_resized, tf.float32)
        img_tensor = tf.reshape(img_casted, [28 * 28, 1])
        return img_tensor


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
