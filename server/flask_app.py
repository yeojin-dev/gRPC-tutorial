import os

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/recognize', methods=['POST'])
def recognize_a_number():
	img = request.files['image']

	# TODO: 파일명 중복 피하기
	filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'image', secure_filename(img.filename))
	img.save(filepath)

	# TODO: gRPC 연결

	result = {'result': 'ok'}
	return jsonify(result)


if __name__ == '__main__':
	app.run('0.0.0.0', port=40000, debug=True)
