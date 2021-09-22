import openmodelica_python_gym as opg 
import numpy as np 
import matplotlib.pyplot as plt

sim = opg.omc.OmcRunner("./motor_model/DrivedMotor.mo","DrivedMotor", ["csvReader.mo"])

def reward_func(x):
    return 0.0

env = opg.env.ModelicaEnv(sim, reward_func, ["speedSensor"],["PID.setpoint"])

init_obs = env.start()

print(init_obs)
done = False

obs_data = []

while not done:
    obs, reward, done, info = env.step(np.array([0.0]))
    obs_data.append(float(obs[0]))
    print(obs)

data = sim.get_sim_data(["speedSensor.w"])


plt.plot(data.index, data["speedSensor.w"])
plt.plot(np.arange(0.1,1.1,0.1), np.array(obs_data[:-1]))
plt.show()
