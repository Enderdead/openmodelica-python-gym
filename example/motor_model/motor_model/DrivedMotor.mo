model DrivedMotor
  Modelica.Mechanics.Rotational.Sources.Torque torque annotation(
    Placement(visible = true, transformation(origin = {68, 2}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Rotational.Components.Inertia inertia(J = 3)  annotation(
    Placement(visible = true, transformation(origin = {124, 2}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Rotational.Sensors.SpeedSensor speedSensor annotation(
    Placement(visible = true, transformation(origin = {136, -34}, extent = {{-10, -10}, {10, 10}}, rotation = 180)));
  Modelica.Blocks.Continuous.LimPID pid(Td = 0.0, Ti = 0.1, controllerType = Modelica.Blocks.Types.SimpleController.PI, k = 2, limitsAtInit = true) annotation(
    Placement(visible = true, transformation(origin = {14, 2}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.Constant zero(k = 0) annotation(
    Placement(visible = true, transformation(origin = {-12, -60}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Rotational.Sources.ConstantTorque constantTorque(tau_constant = -0.01)  annotation(
    Placement(visible = true, transformation(origin = {104, 44}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  omc_gym_lib.pyGymInterface client( input_labels={"speedSensor", "time"}, nin = 2, nout = 2, output_labels={"PID.setpoint", "other"}, samplePeriod = 0.1) annotation(
    Placement(visible = true, transformation(origin = {-60, 2}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Rotational.Sources.Torque torque1 annotation(
    Placement(visible = true, transformation(origin = {70, -84}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Rotational.Components.Inertia inertia1(J = 10.0)  annotation(
    Placement(visible = true, transformation(origin = {112, -86}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Continuous.LimPID pid1(controllerType = Modelica.Blocks.Types.SimpleController.P, k = 0.5, limitsAtInit = true)  annotation(
    Placement(visible = true, transformation(origin = {26, -84}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Rotational.Sensors.SpeedSensor speedSensor1 annotation(
    Placement(visible = true, transformation(origin = {156, -86}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Buildings.Utilities.Time.ModelTime modTim annotation(
    Placement(visible = true, transformation(origin = {-124, 4}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
  connect(torque.flange, inertia.flange_a) annotation(
    Line(points = {{78, 2}, {114, 2}}));
  connect(inertia.flange_b, speedSensor.flange) annotation(
    Line(points = {{134, 2}, {168, 2}, {168, -34}, {146, -34}}));
  connect(pid.y, torque.tau) annotation(
    Line(points = {{26, 2}, {56, 2}}, color = {0, 0, 127}));
  connect(speedSensor.w, pid.u_m) annotation(
    Line(points = {{126, -34}, {14, -34}, {14, -10}}, color = {0, 0, 127}));
  connect(zero.y, pid.u_ff) annotation(
    Line(points = {{-1, -60}, {20, -60}, {20, -10}}, color = {0, 0, 127}));
  connect(constantTorque.flange, inertia.flange_b) annotation(
    Line(points = {{114, 44}, {146, 44}, {146, 2}, {134, 2}}));
  connect(client.y[1], pid.u_s) annotation(
    Line(points = {{-49, 2}, {2, 2}}, color = {0, 0, 127}));
  connect(speedSensor.w, client.u[1]) annotation(
    Line(points = {{126, -34}, {-82, -34}, {-82, 2}, {-72, 2}}, color = {0, 0, 127}));
  connect(torque1.flange, inertia1.flange_a) annotation(
    Line(points = {{80, -84}, {91, -84}, {91, -86}, {102, -86}}));
  connect(pid1.y, torque1.tau) annotation(
    Line(points = {{38, -84}, {58, -84}}, color = {0, 0, 127}));
  connect(pid1.u_s, client.y[2]) annotation(
    Line(points = {{14, -84}, {-49, -84}, {-49, 2}}, color = {0, 0, 127}));
  connect(inertia1.flange_b, speedSensor1.flange) annotation(
    Line(points = {{122, -86}, {146, -86}}));
  connect(speedSensor1.w, pid1.u_m) annotation(
    Line(points = {{168, -86}, {188, -86}, {188, -130}, {26, -130}, {26, -96}}, color = {0, 0, 127}));
  connect(modTim.y, client.u[2]) annotation(
    Line(points = {{-112, 4}, {-90, 4}, {-90, 2}, {-72, 2}}, color = {0, 0, 127}));
protected
  annotation(
    uses(Modelica(version = "3.2.3"), Buildings(version = "8.0.0")),
    Diagram(coordinateSystem(extent = {{-200, -200}, {200, 200}})),
    Icon(coordinateSystem(extent = {{-200, -200}, {200, 200}})),
    version = "");
end DrivedMotor;