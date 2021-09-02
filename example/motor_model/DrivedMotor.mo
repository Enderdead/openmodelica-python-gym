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
    Placement(visible = true, transformation(origin = {-4, -82}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Rotational.Sources.ConstantTorque constantTorque(tau_constant = -0.01)  annotation(
    Placement(visible = true, transformation(origin = {104, 44}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  omc_gym_lib.pyGymInterface pyGymInterface(n_input=1, n_output=1, input_labels={"speedSensor"}, output_labels={"PID.setpoint"}) annotation(
    Placement(visible = true, transformation(origin = {-56, 2}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
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
    Line(points = {{7, -82}, {20, -82}, {20, -10}}, color = {0, 0, 127}));
  connect(constantTorque.flange, inertia.flange_b) annotation(
    Line(points = {{114, 44}, {146, 44}, {146, 2}, {134, 2}}));
  connect(pyGymInterface.y[1], pid.u_s) annotation(
    Line(points = {{-45, 2}, {2, 2}}, color = {0, 0, 127}));
  connect(speedSensor.w, pyGymInterface.u[1]) annotation(
    Line(points = {{126, -34}, {-82, -34}, {-82, 2}, {-68, 2}}, color = {0, 0, 127}));
protected
  annotation(
    uses(Modelica(version = "3.2.3")),
    Diagram(coordinateSystem(extent = {{-100, -200}, {200, 100}})),
    Icon(coordinateSystem(extent = {{-100, -200}, {200, 100}})),
    version = "");
end DrivedMotor;