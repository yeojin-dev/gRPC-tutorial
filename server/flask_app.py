import os

import grpc
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

from protobuf import zebra_pb2_grpc, zebra_pb2

app = Flask(__name__)


@app.route('/recognize', methods=['POST'])
def recognize_a_number():
	img = request.files['image']

	# TODO: 파일명 중복 피하기
	filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'image', secure_filename(img.filename))
	file_stream = img.stream.read()

	with grpc.insecure_channel('localhost:50000') as channel:
		stub = zebra_pb2_grpc.Zebra1ServiceStub(channel)
		message = zebra_pb2.ReqMessage(filepath=filepath, file_stream=file_stream)
		response = stub.Recognize(message)
		number = response.number

	result = {'result': number}
	return jsonify(result)


if __name__ == '__main__':
	app.run('0.0.0.0', port=40000, debug=True)
