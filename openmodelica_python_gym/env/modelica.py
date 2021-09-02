import gym

class ModelicaEnv(gym.Env):
    def __init__(self, omc_runner, input_list, output_list):
        self.model = omc_runner
        self.input_list = input_list
        self.output_list = output_list

    def step(self, action):
        pass

    def render(self, mode="human"):
        pass
    
    def close(self):
        pass 

    def seed(self):
        pass