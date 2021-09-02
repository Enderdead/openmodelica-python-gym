within ;
package omc_gym_lib "Library for electrical power systems"
  extends Modelica.Icons.Package;
  package UsersGuide "User's Guide"
    extends Modelica.Icons.Information;
    class References "References"
      extends Modelica.Icons.References;
      annotation(Documentation(info="<html><p>TODO</p></html>"));
    end References;
    class Contact "Contact"
      extends Modelica.Icons.Contact;
      annotation(Documentation(info="<html><p>The OmcGymLib is part of the openmodelica python cym that is developed at <a href=\"https://github.com/Enderdead/openmodelica-python-gym\">GitHub</a>.</p></html>"));
    end Contact;
    annotation(DocumentationClass=true,
      Documentation(info="<html><p>Documentation under development... </p></html>"));
  end UsersGuide;

  import Modelica.Blocks.Interfaces.RealOutput;
  import Modelica.Blocks.Interfaces.RealInput;
  import Modelica.Blocks.Interfaces.DiscreteBlock;

block FunctionProxy "Generate step signal of type Real"
  annotation(Dialog(groupImage="modelica://Modelica/Resources/Images/Blocks/Sources/Step.png"));
  extends DiscreteBlock(samplePeriod=0.1);
    RealOutput y "Connector of Real output signal" annotation (Placement(
        transformation(extent={{100,-10},{120,10}})));  
        
    RealInput u "Connector of Real input signal"
    annotation (Placement(transformation(extent={{-140,-20},{-100,20}})));      
        
    Real t(start=0);   


  /*function ExternalFunc2
    input Real x[:];
    input String label[:];
    output Real y;
  external "C" annotation(Library={"-lprotobuf", "-lgrpc", "-lgpr", "-lgrpc++", "-L/home/francois/Documents/Programme/grpc/cmake/build/", "ExternalFunc2"}, LibraryDirectory={"/home/francois/Documents/Modeling/motor_protobuf/
"}, IncludeDirectory={"/home/francois/Documents/Modeling/motor_protobuf/source2"});
  end ExternalFunc2;*/


equation
  /*when sampleTrigger */
    when sampleTrigger then
    y = 0.0;/*ExternalFunc2({u, u*2}, {"speed_captor", "mdr"});*/
  end when;
  der(t) = 1;
  annotation (
    Icon(coordinateSystem(
        preserveAspectRatio=true,
        extent={{-100,-100},{100,100}}), graphics={
        Line(points={{-80,68},{-80,-80}}, color={192,192,192}),
        Polygon(
          points={{-80,90},{-88,68},{-72,68},{-80,90}},
          lineColor={192,192,192},
          fillColor={192,192,192},
          fillPattern=FillPattern.Solid),
        Line(points={{-90,-70},{82,-70}}, color={192,192,192}),
        Polygon(
          points={{90,-70},{68,-62},{68,-78},{90,-70}},
          lineColor={192,192,192},
          fillColor={192,192,192},
          fillPattern=FillPattern.Solid),
        Line(points={{-80,-70},{0,-70},{0,50},{80,50}}),
        Text(
          extent={{-150,-150},{150,-110}},
          textString="startTime=%startTime")}),
    Diagram(coordinateSystem(
        preserveAspectRatio=true,
        extent={{-100,-100},{100,100}}), graphics={
        Polygon(
          points={{-80,90},{-86,68},{-74,68},{-80,90}},
          lineColor={95,95,95},
          fillColor={95,95,95},
          fillPattern=FillPattern.Solid),
        Line(points={{-80,68},{-80,-80}}, color={95,95,95}),
        Line(
          points={{-80,-18},{0,-18},{0,50},{80,50}},
          color={0,0,255},
          thickness=0.5),
        Line(points={{-90,-70},{82,-70}}, color={95,95,95}),
        Polygon(
          points={{90,-70},{68,-64},{68,-76},{90,-70}},
          lineColor={95,95,95},
          fillColor={95,95,95},
          fillPattern=FillPattern.Solid),
        Text(
          extent={{70,-80},{94,-100}},
          textString="time"),
        Text(
          extent={{-21,-72},{25,-90}},
          textString="startTime"),
        Line(points={{0,-18},{0,-70}}, color={95,95,95}),
        Text(
          extent={{-68,-36},{-22,-54}},
          textString="offset"),
        Line(points={{-13,50},{-13,-17}}, color={95,95,95}),
        Polygon(
          points={{0,50},{-21,50},{0,50}},
          lineColor={95,95,95},
          fillColor={95,95,95},
          fillPattern=FillPattern.Solid),
        Polygon(
          points={{-13,-18},{-16,-5},{-10,-5},{-13,-18},{-13,-18}},
          lineColor={95,95,95},
          fillColor={95,95,95},
          fillPattern=FillPattern.Solid),
        Polygon(
          points={{-13,50},{-16,37},{-10,37},{-13,50}},
          lineColor={95,95,95},
          fillColor={95,95,95},
          fillPattern=FillPattern.Solid),
        Text(
          extent={{-68,26},{-22,8}},
          textString="height"),
        Polygon(
          points={{-13,-70},{-16,-57},{-10,-57},{-13,-70},{-13,-70}},
          lineColor={95,95,95},
          fillColor={95,95,95},
          fillPattern=FillPattern.Solid),
        Line(points={{-13,-18},{-13,-70}}, color={95,95,95}),
        Polygon(
          points={{-13,-18},{-16,-31},{-10,-31},{-13,-18}},
          lineColor={95,95,95},
          fillColor={95,95,95},
          fillPattern=FillPattern.Solid),
        Text(
          extent={{-72,100},{-31,80}},
          textString="y")}));
end FunctionProxy;




end omc_gym_lib;