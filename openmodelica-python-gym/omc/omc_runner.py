import os 
from OMPython import OMCSessionZMQ, ModelicaSystem
import scipy.io
import numpy as np


class OmcRunner():
    """
    Charger de verifier les fichiers, pousser 
    """
    def __init__(fileName, modelName, lmodel=None, project_dir=None):
        """ Create the modelica objectf  """

        if project_dir is None:
            self.project_dir = os.path.dirname(fileName)
        else:
            self.project_dir = project_dir
        self.fileName = os.path.basename(fileName)
        self.lmodel = lmodel
        self.modelName = modelName

        # Improve the path gesture.
        self.model = ModelicaSystem(os.path.join(self.project_dir, self.fileName), self.modelName, lmodel=self.lmodel )
        
    def build(self):
        # Check if build dir is availiable 
        if not os.path.isdir(os.path.join(self.project_dir, "build")):
            os.makedirs(os.path.join(self.project_dir, "build"))

        curr_dir = os.curdir
        os.chdir(os.path.join(self.project_dir, "build"))
        self.model.buildModel()
        os.chdir(curr_dir)

    def start(self, start_Time=0.0, stop_Time=1.0):
        self.model.setSimulationOptions([f"startTime={start_Time}",f"stopTime={stop_Time}"])

        pass

    def get_sim_data(self, vars):
        res    =self.model.getSolutions(["functionProxy.t", "functionProxy.y", "speedSensor.w"])
        return res

    def close(self):
        pass    
