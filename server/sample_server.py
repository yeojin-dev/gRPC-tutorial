import time
from concurrent import futures

import grpc

from protobuf import sample_pb2_grpc, sample_pb2


class SampleServiceServicer(sample_pb2_grpc.SampleServiceServicer):

	def __init__(self):
		pass

	def HelloServer(self, request: sample_pb2.HelloMessage, context: grpc._server._Context) -> sample_pb2.ReplyMessage:
		"""SampleService 서비스에서 정의한 RPC

		Args:
			request: protobuf 정의 메시지
			context: 서버 컨텍스트

		Returns:
			result: 클라이언트에 전달하는 메시지
		"""
		print(f'Receive new message! [name: {request.name}, msg: {request.msg}]')
		result = sample_pb2.ReplyMessage(reply_msg=f'Nice to meet you, {request.name}!')
		return result


if __name__ == '__main__':
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
	sample_pb2_grpc.add_SampleServiceServicer_to_server(SampleServiceServicer(), server)
	server.add_insecure_port('[::]:50000')
	server.start()
	print('Starting gRPC sample server...')

	try:
		while True:
			time.sleep(3600)
	except KeyboardInterrupt:
		server.stop(0)
