import gym
import numpy as np
from openmodelica_python_gym.grpc import grpcInterface
import queue
import atexit

class EndSignal():
    pass

class ModelicaEnv(gym.Env):
    def __init__(self, omc_runner, reward_func, input_list, output_list):
        super(ModelicaEnv, self).__init__()

        self.model = omc_runner
        self.input_list = input_list
        self.output_list = output_list

        self.reward_func = reward_func

        self.observation_space = gym.spaces.Box(np.array([-np.inf,]*len(self.input_list)), 
                                           np.array([ np.inf,]*len(self.input_list)))

        self.action_space = gym.spaces.Box(np.array([-np.inf,]*len(self.output_list)), 
                                           np.array([ np.inf,]*len(self.output_list)))

        if not omc_runner.is_ready():
            raise RuntimeError("")

        self.simulator = omc_runner
        self.grpc_server = grpcInterface(self.input_list, self.output_list, self._recv)
        
        self.data_in_queue  = queue.Queue(maxsize=2)
        self.data_out_queue = queue.Queue(maxsize=2)


    def _recv(self, input_data):
        # receive func
        self.data_in_queue.put(input_data)    

        return self.data_out_queue.get(block=True)

    def _end_signal(self):
        self.data_in_queue.put(EndSignal())

    def start(self):
        atexit.register(self.__del__)
        # Je lance le GRPC server
        self.grpc_server.start()
        # Je lance la simu sur un thread
        self.simulator.start(self._end_signal)

        # J'attend la première observation
        first_obs = self.data_in_queue.get(block=True, timeout=10)

        return first_obs, self.reward_func(first_obs), False, {}

        

    def step(self, action):
        # TODO get real final observation ...

        # Upload data
        self.data_out_queue.put(action)

        # Wait simulation computation
        obs = self.data_in_queue.get(block=True, timeout=10)

        if isinstance(obs, EndSignal):
            return np.zeros(shape=(len(self.input_list))), 0, True, {}

        return obs, self.reward_func(obs), False, {}


    def render(self, mode="human"):
        pass
    
    def close(self):
        self.grpc_server.stop()
        #self.simulator.stop() maybe 

    def seed(self):
        pass

    def __del__(self):
        if not self.grpc_server is None:
            self.grpc_server.stop()

