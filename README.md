# gRPC-tutorial

* 딥러닝 모델을 gRPC 프로토콜을 이용해 end-to-end 서비스로 구현하는 예제

## 텐서플로, mnist 데이터셋을 이용한 숫자 손글씨 인식 서비스

### 모델 학습

* [텐서플로 2.0 기본 튜토리얼](https://www.tensorflow.org/tutorials/quickstart/beginner?hl=ko) 문서를 이용해 숫자 손글씨 분류 모델 구현

```shell script
# 모델 구현 및 SavedModel 저장 
python ./model/sample_mnist.py
```

### 텐서플로 서빙 REST API 서버 구축(local)

* `tensorflow/serving` 도커 이미지를 이용

```shell script
docker run --rm -p 8501:8501 --name tensorflow-mnist --mount type=bind,source=$(pwd)/protobuf/model/mnist,target=/models/mnist -e MODEL_NAME=mnist -t tensorflow/serving
```

### 텐서플로 서빙 서버 호출 예시

#### 메타데이터

* GET http://127.0.0.1:8501/v1/models/mnist/metadata

##### 응답 예시

```json
{
    "model_spec": {
        "name": "mnist",
        "signature_name": "",
        "version": "0"
    },
    "metadata": {
        "signature_def": {
            "signature_def": {
                "serving_default": {
                    "inputs": {
                        "flatten_input": {
                            "dtype": "DT_FLOAT",
                            "tensor_shape": {
                                "dim": [
                                    {
                                        "size": "-1",
                                        "name": ""
                                    },
                                    {
                                        "size": "28",
                                        "name": ""
                                    },
                                    {
                                        "size": "28",
                                        "name": ""
                                    }
                                ],
                                "unknown_rank": false
                            },
                            "name": "serving_default_flatten_input:0"
                        }
                    },
                    "outputs": {
                        "dense_1": {
                            "dtype": "DT_FLOAT",
                            "tensor_shape": {
                                "dim": [
                                    {
                                        "size": "-1",
                                        "name": ""
                                    },
                                    {
                                        "size": "10",
                                        "name": ""
                                    }
                                ],
                                "unknown_rank": false
                            },
                            "name": "StatefulPartitionedCall:0"
                        }
                    },
                    "method_name": "tensorflow/serving/predict"
                },
                "__saved_model_init_op": {
                    "inputs": {},
                    "outputs": {
                        "__saved_model_init_op": {
                            "dtype": "DT_INVALID",
                            "tensor_shape": {
                                "dim": [],
                                "unknown_rank": true
                            },
                            "name": "NoOp"
                        }
                    },
                    "method_name": ""
                }
            }
        }
    }
}
```

#### 추론

* POST http://127.0.0.1:8501/v1/models/mnist/metadata

##### body

* mnist 데이터셋의 이미지 픽셀 정보를 flatten 처리
* 28 * 28 픽셀의 이미지이기 때문에 길이 784의 array 필요

```json
{
    "inputs": [
        0, 
        0,
        ...
        0
    ]
}
```

##### 응답 예시

```json
{
    "outputs": [
        [
            -3.95562673,
            -6.8210392,
            -3.59877825,
            8.60473824,
            -24.2328682,
            12.1519499,
            -14.8646755,
            -3.63648438,
            -8.98115826,
            -3.38781738
        ]
    ]
}
```
