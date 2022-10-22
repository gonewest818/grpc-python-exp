
APP = \
    hellostream_pb2.py \
    hellostream_pb2_grpc.py

all: ${APP}

%_pb2.py %_pb2_grpc.py : %.proto
	python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. $<


