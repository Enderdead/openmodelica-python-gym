#!/bin/bash

echo "Creating build dir"
mkdir -p ./openmodelica_python_gym/external_lib/grpc_interface/build || exit 1

echo "Start compiling..."
cmake -B ./openmodelica_python_gym/external_lib/grpc_interface/build ./openmodelica_python_gym/external_lib/grpc_interface || exit 1
make -C ./openmodelica_python_gym/external_lib/grpc_interface/build || exit 1
