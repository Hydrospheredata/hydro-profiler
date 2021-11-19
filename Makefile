proto:
	cd profiler && poetry run python -m grpc_tools.protoc -I profiler/protobuf/ --python_out=profiler/protobuf/ --grpc_python_out=profiler/protobuf/ profiler/protobuf/monitoring_manager.proto

image:
	docker build -f profiler/Dockerfile -t hydrosphere/profiler:latest .