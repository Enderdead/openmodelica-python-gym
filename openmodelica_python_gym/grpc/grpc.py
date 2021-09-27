from concurrent import futures
import time
import math
import logging

import grpc
import numpy as np
import os


from ..grpc import python_gym_pb2
from ..grpc import python_gym_pb2_grpc
#https://stackoverflow.com/questions/14132789/relative-imports-for-the-billionth-time


import json


class grpcInterface(python_gym_pb2_grpc.pythonGym):
    def __init__(self, input_label, output_label, target_func):
        self.input_label = input_label
        self.output_label = output_label
        self.target_func = target_func

        self.server = None

    def start(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
        python_gym_pb2_grpc.add_pythonGymServicer_to_server(
                self, self.server) # A little bit dirty...

        self.server.add_insecure_port('[::]:50051')
        self.server.start()

    def stop(self):
        if self.server is None:
            return 

        self.server.stop(0.5)
        self.server = None


    def next(self, request, context):
        np_x = np.array([np.nan, ]*len(self.input_label))
        
        while len(request.data) >0:
            data = request.data.pop()
            if data.id in self.input_label:
                np_x[self.input_label.index(data.id)] = data.value

        if np.sum(np.isnan(np_x)) >= 1:
            # Mising values
            print(np.isnan(np_x))
            raise RuntimeError("TODO")

        np_y = self.target_func(np_x)
        # Push dict

        output_data = python_gym_pb2.DataSet()
        for idx, label in enumerate(self.output_label):
            batch_data = python_gym_pb2.Data()
            batch_data.id = label
            batch_data.value = float(np_y[idx])
            output_data.data.append(batch_data)

        return output_data



    def __del__(self):
        print("del")

        