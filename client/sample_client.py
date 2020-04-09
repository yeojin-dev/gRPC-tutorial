import grpc

import sample_pb2
import sample_pb2_grpc


def hello_server(stub, name, msg):
	message = sample_pb2.HelloMessage(name=name, msg=msg)
	response = stub.HelloServer(message)
	print(f'Received message {response.reply_msg}')


if __name__ == '__main__':
	with grpc.insecure_channel('localhost:50000') as channel:
		stub = sample_pb2_grpc.SampleServiceStub(channel)
		print('--- Client Start ---')

		while True:
			name = input('name? > ')
			msg = input('message? > ')
			hello_server(stub, name, msg)
