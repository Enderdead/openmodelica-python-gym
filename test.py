import openmodelica_python_gym as opg 




sim = opg.omc.OmcRunner("./motor_model/DrivedMotor.mo","DrivedMotor", ["csvReader.mo"])

#sim.build()
