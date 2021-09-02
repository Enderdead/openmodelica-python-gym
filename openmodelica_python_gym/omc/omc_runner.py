import os 
from OMPython import OMCSessionZMQ, ModelicaSystem
import scipy.io
import numpy as np


class OmcRunner():
    """
    Charger de verifier les fichiers, pousser 
    """
    def __init__(self, fileName, modelName, lmodel=None, project_dir=None):
        """ Create the modelica objectf  """

        if project_dir is None:
            self.project_dir = os.path.abspath(os.path.dirname(fileName))
        else:
            self.project_dir = os.path.abspath(project_dir)
        self.fileName = os.path.basename(fileName)
        if not lmodel is None:
            for i in range(len(lmodel)):
                if not os.path.isfile(lmodel[i]):
                    lmodel[i] = os.path.join(self.project_dir, lmodel[i])
            self.lmodel = lmodel
        else:
            self.lmodel=[]
        self.modelName = modelName

        # Improve the path gesture.
        self._build()
        
    def _build(self):
        # Check if build dir is availiable 
        if not os.path.isdir(os.path.join(self.project_dir, "build")):
            os.makedirs(os.path.join(self.project_dir, "build"))

        # Check if Resources/Library is availiable   
        if not os.path.isdir(os.path.join(self.project_dir, "Resources/Library")):
            os.makedirs(os.path.join(self.project_dir, "Resources/Library"))

        # Include our own library
        self.lmodel.append(os.path.join(os.path.dirname(__file__), "../omc_gym_lib/package.mo"))

        # Create a symbolic link to our c library
        local_so_file = os.path.join(os.path.dirname(__file__), "../external_lib/grpc_interface/build/libgrpc_interface.so")
        if not os.path.isfile(os.path.join(self.project_dir, "Resources/Library/libgrpc_interface.so")):
            os.symlink(local_so_file, os.path.join(self.project_dir, "Resources/Library/libgrpc_interface.so"))

        curr_dir = os.curdir
        os.chdir(os.path.join(self.project_dir, "build"))
        self.model = ModelicaSystem(os.path.join(self.project_dir, self.fileName), self.modelName, lmodel=self.lmodel )
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
