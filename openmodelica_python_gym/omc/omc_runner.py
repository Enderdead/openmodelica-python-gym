import os 
from OMPython import OMCSession, OMCSessionZMQ, ModelicaSystem
import scipy.io
import numpy as np
from openmodelica_python_gym.util.find_omc_interface import find_omc_interface
import pandas
import threading
import atexit
import xml.etree.ElementTree as ET
import warnings
import psutil
import hashlib
import time
import pandas as pd

#TODO il gère le thread

class OmcRunner():
    """
    Charger de verifier les fichiers, pousser 
    """
    def __init__(self, fileName, modelName, lmodel=None, smodel=None, project_dir=None, use_cache=False):
        """ Create the modelica objectf  """

        self.init = False
        self.use_cache = use_cache

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
        
        self.smodel = smodel if not (smodel is None) else  []
        self.modelName = modelName

        # Improve the path gesture.
        self._build()

        # start option (default value)
        self.start_Time = 0
        self.stop_Time = 1
        self.solving_method = "dassl" 
        self.stepSize = 0.1
        
    def _build(self):
        # Check if build dir is availiable 
        if not os.path.isdir(os.path.join(self.project_dir, "build")):
            os.makedirs(os.path.join(self.project_dir, "build"))



        # Check if Resources/Library is availiable   
        if not os.path.isdir(os.path.join(self.project_dir, "Resources/Library")):
            os.makedirs(os.path.join(self.project_dir, "Resources/Library"))

        # if cached asked # TODO make a cache with all files 
        if self.use_cache:
            warnings.warn(f"Be aware that the following file will be used to check futur update : {self.fileName}")
            file_hasher = hashlib.sha256()
            if not os.path.exists(self.fileName):  # if file does not eixt
                raise RuntimeError("Can't file your main modelica file !")
            fil = open(self.fileName, "r")
            file_hasher.update("".join(fil.readlines()).encode('utf-8'))
            fil.close()
            hash_project = file_hasher.hexdigest()

            #Check if hash is present 
            if os.path.isfile(os.path.join(self.project_dir, "build", "hash_cache.txt")):
                local_hash_file = open(os.path.join(self.project_dir, "build", "hash_cache.txt"), "r")
                local_hash, self.time_label = local_hash_file.readline(200).split(",") # TODO add try catch

                if local_hash == hash_project:
                    need_build = False
                else:
                    need_build = True
            else:
                need_build = True
        else:
            # default hash value
            hash_project = -1
            need_build = True



        # Include our own library
        self.lmodel.append(os.path.join(os.path.dirname(__file__), "../omc_gym_lib/package.mo"))

        # Create a symbolic link to our c library
        local_so_file = os.path.join(os.path.dirname(__file__), "../external_lib/grpc_interface/build/libgrpc_interface.so")
        if not os.path.isfile(os.path.join(self.project_dir, "Resources/Library/libgrpc_interface.so")):
            os.symlink(local_so_file, os.path.join(self.project_dir, "Resources/Library/libgrpc_interface.so"))

        curr_dir = os.curdir
        os.chdir(os.path.join(self.project_dir, "build"))
        if need_build:
            
            self.model = ModelicaSystem(os.path.join(self.project_dir, self.fileName), self.modelName, lmodel=self.smodel+self.lmodel )
            self.model.setParameters("d=bltdump")
            self.model.buildModel()
            
            target_blocs = find_omc_interface(self.model.tree.getroot())

            if len(target_blocs)==0:
                raise RuntimeError("Can't find the gym interface in your modelica project !")

            if len(target_blocs)>1:
                raise RuntimeError("Too many gym interface in your modelica project ! (only one supported)")

            self.time_label = target_blocs[0]+".t"
        else:
            self.model = FakeModel(os.path.join(self.project_dir, self.fileName), self.modelName, lmodel=self.smodel+self.lmodel )
        os.chdir(curr_dir)

        

        self.thread = None
        self.init = True
        self.pids = None

        # Generate hash file
        if self.use_cache:
            print("WE need to do something here ! ")
            hash_file = open(os.path.join(self.project_dir, "build", "hash_cache.txt"), "w")
            hash_file.write(f"{hash_project},{self.time_label}")
            hash_file.close()

    def is_ready(self):
        return self.init

    def set_simulation_option(self, start_Time=None, stop_Time=None, solving_method=None, stepSize=None):
        if not start_Time is None : # Weird way to do this. Redo this in the futur.
            self.start_Time = start_Time
        if not stop_Time is None :
            self.stop_Time = stop_Time

        if not solving_method is None :
            self.solving_method = solving_method

        if not stepSize is None :
            self.stepSize = stepSize

    def start(self, end_signal):
        if not  self.init:
            raise RuntimeError("OMC Simulator is not initialized !")
        #TODO find way to select solving method
        print(self.model.setSimulationOptions)
        self.model.setSimulationOptions([f"startTime={self.start_Time}",f"stopTime={self.stop_Time}",f"solver={self.solving_method}",f"stepSize={self.stepSize}"])

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


class FakeModel():
    def __init__(self, fileName=None, modelName=None, lmodel=[], useCorba=False, commandLineOptions=None):
        self.fileName = fileName
        self.modelName = modelName
        self.lmodel = lmodel
        self.useCorba = useCorba
        self.simulationOption = None

        self.xmlFile = os.path.join(os.getcwd(), self.modelName+"_init.xml").replace("\\", "/")
        self.resultfile = os.path.join(os.getcwd(), self.modelName+"_res.mat").replace("\\", "/")
        self.paramlist = dict()
        self.quantitiesList=[]
        self.paramlist={}
        self.inputlist={}
        self.outputlist={}
        self.continuouslist={}
        self.overridevariables={}
        self.linearquantitiesList = []  # linearization  quantity list
        self.linearparameters={}
        self.linearinputs = []  # linearization input list
        self.linearoutputs = []  # linearization output list
        self.linearstates = []  # linearization  states list
        self.simulationFlag = {}
        self.inputFlag = False  # for model with input quantity
        self.simulationFlag = False  # if the model is simulated?
        self.linearizationFlag = False
        self.outputFlag = False

        if useCorba:
            self.getconn = OMCSession()
        else:
            self.getconn = OMCSessionZMQ()


        self.xmlparse()


    def setSimulationOptions(self, string):
        self.simulationOption = string

    def getSolutions(self, varList=None, resultfile=None):  # 12

        if (resultfile == None):
            resFile = self.resultfile
        else:
            resFile = resultfile

        # check for result file exits
        if (not os.path.exists(resFile)):
            print("Error: Result file does not exist")
            return
            #exit()
        else:
            if (varList == None):
                # validSolution = ['time'] + self.__getInputNames() + self.__getContinuousNames() + self.__getParameterNames()
                validSolution = self.getconn.sendExpression("readSimulationResultVars(\"" + resFile + "\")")
                self.getconn.sendExpression("closeSimulationResultFile()")
                return validSolution
            elif (isinstance(varList,str)):
                if (varList not in [l["name"] for l in self.quantitiesList] and varList!="time"):
                    print('!!! ', varList, ' does not exist\n')
                    return
                exp = "readSimulationResult(\"" + resFile + '",{' + varList + "})"
                res = self.getconn.sendExpression(exp)
                npRes = np.array(res)
                exp2 = "closeSimulationResultFile()"
                self.getconn.sendExpression(exp2)
                return npRes
            elif (isinstance(varList, list)):
                #varList, = varList
                for v in varList:
                    if v == "time":
                        continue
                    if v not in [l["name"] for l in self.quantitiesList]:
                        print('!!! ', v, ' does not exist\n')
                        return
                variables = ",".join(varList)
                exp = "readSimulationResult(\"" + resFile + '",{' + variables + "})"
                res = self.getconn.sendExpression(exp)
                npRes = np.array(res)
                exp2 = "closeSimulationResultFile()"
                self.getconn.sendExpression(exp2)
                return npRes

    def getContinuous(self, names=None):
        if not self.simulationFlag:
            if(names==None):
                return self.continuouslist
            elif(isinstance(names, str)):
                return [self.continuouslist.get(names ,"NotExist")]
            elif(isinstance(names, list)):
                return ([self.continuouslist.get(x ,"NotExist") for x in names])
        else:
            if(names==None):
                for i in self.continuouslist:
                    try:
                        value = self.getSolutions(i)
                        self.continuouslist[i]=value[0][-1]
                    except Exception:
                        print(i,"could not be computed")
                return self.continuouslist

            elif(isinstance(names, str)):
                if names in self.continuouslist:
                    value = self.getSolutions(names)
                    self.continuouslist[names]=value[0][-1]
                    return [self.continuouslist.get(names)]
                else:
                    return (names, "  is not continuous")

            elif(isinstance(names, list)):
                valuelist=[]
                for i in names:
                    if i in self.continuouslist:
                        value=self.getSolutions(i)
                        self.continuouslist[i]=value[0][-1]
                        valuelist.append(value[0][-1])
                    else:
                        return (i,"  is not continuous")
                return valuelist


    def simulate(self):
        getExeFile = os.path.join(os.getcwd(), self.modelName).replace("\\", "/")


        if not self.simulationOption is None:
            override = " -override=" + ",".join(self.simulationOption)
        else:
            override = " "
        cmd = getExeFile + override #+ " -lv LOG_LS"
        os.system(cmd)


    def xmlparse(self):
        if(os.path.exists(self.xmlFile)):
            self.tree = ET.parse(self.xmlFile)
            self.root = self.tree.getroot()
            rootCQ = self.root

            for sv in rootCQ.iter('ScalarVariable'):
                scalar={}
                scalar["name"] = sv.get('name')
                scalar["changeable"] = sv.get('isValueChangeable')
                scalar["description"] = sv.get('description')
                scalar["variability"] = sv.get('variability')
                scalar["causality"] = sv.get('causality')
                scalar["alias"] = sv.get('alias')
                scalar["aliasvariable"] = sv.get('aliasVariable')
                ch = list(sv)
                start = None
                for att in ch:
                    start = att.get('start')
                scalar["start"] =start

                if(self.linearizationFlag==False):
                    if(scalar["variability"]=="parameter"):
                        if scalar["name"] in self.overridevariables:
                            self.paramlist[scalar["name"]] = self.overridevariables[scalar["name"]]
                        else:
                            self.paramlist[scalar["name"]] = scalar["start"]
                    if(scalar["variability"]=="continuous"):
                        self.continuouslist[scalar["name"]]=scalar["start"]
                    if(scalar["causality"]=="input"):
                        self.inputlist[scalar["name"]]=scalar["start"]
                    if(scalar["causality"]=="output"):
                        self.outputlist[scalar["name"]]=scalar["start"]

                if(self.linearizationFlag==True):
                    if(scalar["variability"]=="parameter"):
                        self.linearparameters[scalar["name"]]=scalar["start"]
                    if(scalar["alias"]=="alias"):
                        name=scalar["name"]
                        if (name[1] == 'x'):
                            self.linearstates.append(name[3:-1])
                        if (name[1] == 'u'):
                            self.linearinputs.append(name[3:-1])
                        if (name[1] == 'y'):
                            self.linearoutputs.append(name[3:-1])
                    self.linearquantitiesList.append(scalar)
                else:
                    self.quantitiesList.append(scalar)
        else:
            print("Error: ! XML file not generated")
            return