cmake_minimum_required(VERSION 3.20)
project(grpc_interface)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set (CMAKE_CXX_FLAGS "-fPIC")

find_package(Protobuf REQUIRED)
find_package(gRPC CONFIG REQUIRED)

add_library(grpc_interface  SHARED grpc_interface.cc ./generated/python_gym.grpc.pb.cc ./generated/python_gym.grpc.pb.cc)

target_link_libraries(grpc_interface
        protobuf::libprotobuf
        )
target_link_libraries(grpc_interface
        gRPC::grpc++_reflection
        )