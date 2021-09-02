#python3 -m grpc_tools.protoc -I./openmodelica-python-gym/protocol/ --python_out=./openmodelica-python-gym/protocol/ --grpc_python_out=./openmodelica-python-gym/protocol/ ./openmodelica-python-gym/protocol/python_gym.proto


protoc -I ./openmodelica_python_gym/protocol/  --grpc_out=./openmodelica_python_gym/external_lib/grpc_interface/generated --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` ./openmodelica_python_gym/protocol/python_gym.proto
protoc -I ./openmodelica_python_gym/protocol/   --cpp_out=./openmodelica_python_gym/external_lib/grpc_interface/generated  ./openmodelica_python_gym/protocol/python_gym.proto


mkdir -p ./openmodelica_python_gym/external_lib/grpc_interface/build

cmake -B ./openmodelica_python_gym/external_lib/grpc_interface/build ./openmodelica_python_gym/external_lib/grpc_interface 
make -C ./openmodelica_python_gym/external_lib/grpc_interface/build