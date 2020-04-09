from grpc_tools import protoc


protoc.main(('', '-I.', '--python_out=./client', '--grpc_python_out=./server', './sample.proto'))
