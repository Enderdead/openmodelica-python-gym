import os 
from OMPython import OMCSessionZMQ, ModelicaSystem
import scipy.io
import numpy as np
from openmodelica_python_gym.util.find_omc_interface import find_omc_interface
import pandas
import threading
import atexit
import psutil
import time
import pandas as pd

#TODO il gère le thread

class OmcRunner():
    """
    Charger de verifier les fichiers, pousser 
    """
    def __init__(self, fileName, modelName, lmodel=None, project_dir=None):
        """ Create the modelica objectf  """

        self.init = False

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

        target_blocs = find_omc_interface(self.model.tree.getroot())

        if len(target_blocs)==0:
            raise RuntimeError("Can't find the gym interface in your modelica project !")

        if len(target_blocs)>1:
            raise RuntimeError("Too many gym interface in your modelica project ! (only one supported)")

        self.time_label = target_blocs[0]+".t"
        self.thread = None
        self.init = True
        self.pids = None

    def is_ready(self):
        return self.init

    def start(self, end_signal, start_Time=0.0, stop_Time=1.0, solving_method="dassl"):
        if not  self.init:
            raise RuntimeError("OMC Simulator is not initialized !")
        #TODO find way to select solving method
        self.model.setSimulationOptions([f"startTime={start_Time}",f"stopTime={stop_Time}"])

        def aux_main():
            self.model.simulate()
            end_signal()
        
        self.thread  = threading.Thread(target=aux_main)
        self.thread.start()
        time.sleep(1)
        p = psutil.Process()
        procs = psutil.Process().children()# TODO go through all process to find process with name=omc
        self.pids =  [ psutil.Process(procs[0].pid).children()[0].pid, procs[0].pid]
        atexit.register(self.__del__)
        


    def get_sim_variables(self):
        if not self.init:
            raise RuntimeError("")
        return list(self.model.getContinuous().keys())


    def get_sim_data(self, var_list):
        res    = self.model.getSolutions([self.time_label,]+var_list)
        data_dict = dict(zip( var_list, [res[i+1,:] for i in range(len(var_list))]))
        pd_frame = pd.DataFrame(index=res[0,:], data=data_dict)
        pd_frame.index.name = "t"
        return pd_frame

    def close(self):
        pass    


    def __del__(self):
        if not self.pids is None:
            try:
                os.kill(self.pids[0], 0)
                os.kill(self.pids[0], 9)
            except OSError:
                pass
            try:
                os.kill(self.pids[1], 0)
                os.kill(self.pids[1], 9)
            except OSError:
                pass


