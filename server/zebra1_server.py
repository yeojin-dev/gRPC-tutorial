import time
from concurrent import futures

import grpc
import numpy as np
import tensorflow as tf
from tensorflow_core.core.framework import tensor_pb2, tensor_shape_pb2, types_pb2
from tensorflow_serving.apis import predict_pb2, prediction_service_pb2_grpc

from protobuf import zebra_pb2_grpc, zebra_pb2


class Zebra1ServiceServicer(zebra_pb2_grpc.Zebra1ServiceServicer):

    def __init__(self):
        pass

    def Recognize(self, request, context):
        print(f'Filepath from request: {request.filepath}')
        print(f'File stream from request: {request.file_stream}')

        img_tensor = self.get_flatten_image_tensor(request.file_stream)
        predict_request = self.get_predict_request_from_image_tensor(img_tensor)

        with grpc.insecure_channel('localhost:8500') as channel:
            stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
            response = stub.Predict(predict_request)

        outputs = dict(response.outputs)
        result = list(outputs['dense_1'].float_val)
        number = result.index(max(result))

        res_message = zebra_pb2.ResMessage(number=number)

        return res_message

    @staticmethod
    def get_flatten_image_tensor(stream: bytes) -> tf.Tensor:
        img_grayscale = tf.image.decode_png(stream, channels=1)
        img_resized = tf.image.resize(img_grayscale, [28, 28])
        img_casted = tf.cast(img_resized, tf.float32)
        img_tensor = tf.reshape(img_casted, [28 * 28, 1])
        return img_tensor

    @staticmethod
    def get_predict_request_from_image_tensor(tensor: tf.Tensor) -> predict_pb2.PredictRequest:
        request = predict_pb2.PredictRequest()
        request.model_spec.name = 'mnist'

        dim = [tensor_shape_pb2.TensorShapeProto.Dim(size=28 * 28)]
        shape = tensor_shape_pb2.TensorShapeProto(dim=dim)
        img_tensor_content = np.array(tensor).tostring()
        tensor = tensor_pb2.TensorProto(
            dtype=types_pb2.DT_FLOAT, tensor_shape=shape, tensor_content=img_tensor_content,
        )
        request.inputs['flatten_input'].CopyFrom(tensor)

        return request


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
