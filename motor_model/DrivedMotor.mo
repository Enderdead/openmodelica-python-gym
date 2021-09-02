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
    Placement(visible = true, transformation(origin = {-36, -46}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  omc_gym_lib.pyGymInterface functionProxy(n_input=1, n_output=1, input_labels={"a"}, output_labels={"b"}) annotation(
    Placement(visible = true, transformation(origin = {-66, -2}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Rotational.Sources.ConstantTorque constantTorque(tau_constant = -0.01)  annotation(
    Placement(visible = true, transformation(origin = {104, 44}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.TimeTable timeTable(table = matrix([0, 0; 1, 0; 3, 1]))  annotation(
    Placement(visible = true, transformation(origin = {-6, 86}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Mechanics.Rotational.Sources.Torque torque1 annotation(
    Placement(visible = true, transformation(origin = {34, 64}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));

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
    Line(points = {{-24, -46}, {20, -46}, {20, -10}}, color = {0, 0, 127}));
  connect(functionProxy.y[1], pid.u_s) annotation(
    Line(points = {{-54, -2}, {2, -2}, {2, 2}}, color = {0, 0, 127}));
  connect(speedSensor.w, functionProxy.u[1]) annotation(
    Line(points = {{126, -34}, {-86, -34}, {-86, -2}, {-78, -2}}, color = {0, 0, 127}));
  connect(constantTorque.flange, inertia.flange_b) annotation(
    Line(points = {{114, 44}, {146, 44}, {146, 2}, {134, 2}}));
  connect(torque1.flange, torque.flange) annotation(
    Line(points = {{44, 64}, {78, 64}, {78, 2}}));
  connect(zero.y, torque1.tau) annotation(
    Line(points = {{-62, 54}, {22, 54}, {22, 64}}, color = {0, 0, 127}));
protected
  annotation(
    uses(Modelica(version = "3.2.3")),
    Diagram(coordinateSystem(extent = {{-100, -200}, {200, 100}})),
    Icon(coordinateSystem(extent = {{-100, -200}, {200, 100}})),
    version = "");
end DrivedMotor;