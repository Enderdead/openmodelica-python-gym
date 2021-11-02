import openmodelica_python_gym as opg 
import numpy as np 
import matplotlib.pyplot as plt

import time
def reward_func(x):
    return 0.0


# Instanciation du modèle open modelica
sim = opg.omc.OmcRunner("./motor_model/DrivedMotor.mo","DrivedMotor", ["csvReader.mo"])
sim.set_simulation_option(start_Time=0, stop_Time=0.1*20, stepSize=0.001)


env = opg.env.ModelicaEnv(sim, reward_func, ["speedSensor", "time"],["PID.setpoint", "other"])

init_obs = env.start()

print(init_obs)
done = False

obs_data = []

while not done:
    obs, reward, done, info = env.step(np.array([0.0,1.0]))
    time.sleep(0.5)
    obs_data.append(float(obs[0]))
    print(obs)

data = sim.get_sim_data(["speedSensor.w"])


plt.plot(data.index, data["speedSensor.w"])
plt.plot(np.arange(0.1,0.1*20.,0.1), np.array(obs_data[:-1]))
plt.title("Observation de la vitesse du moteur (coté python)")
plt.xlabel("Temps (s)")
plt.ylabel("Vitesse de rotation (rad/s)")
plt.show()
