import argparse

from grpc_tools import protoc


def arg_process():
	parser = argparse.ArgumentParser('Generate pb2 files from protobuf')

	parser.add_argument(
		'-p',
		'--protobuf_path',
		type=str,
		required=True,
	)

	args, unknown = parser.parse_known_args()
	return args, unknown


if __name__ == '__main__':
	flags, unparsed = arg_process()
	protobuf_path = flags.protobuf_path

	print(f'Generate pb2 files from {protobuf_path}')
	protoc.main(('', '-I.', '--python_out=./protobuf', '--grpc_python_out=./protobuf', protobuf_path))
