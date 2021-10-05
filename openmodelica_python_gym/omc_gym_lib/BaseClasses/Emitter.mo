within omc_gym_lib.BaseClasses;

block Emitter

  parameter Integer nin=1 "Number of inputs";
  parameter Integer nout=1 "Number of outputs";
  parameter String  input_labels[:] "Ordered input labels";
  parameter String  output_labels[:] "Ordered output labels";
    extends DiscreteBlock;


  Modelica.Blocks.Interfaces.RealInput u[nin](each stateSelect=StateSelect.never) "Connector of Real input signals" annotation (Placement(transformation(extent={{-140,-20},{-100,20}})));
  
  function grpcInterface
    input Real t;
    input Real x[nin];
    input String in_label[nin];
    input String out_label[nout];
    input Real sampling_rate;
    
  external "C" annotation(Library={"-lprotobuf", "-lgrpc", "-lgpr", "-lgrpc++", "grpc_interface"},
  LibraryDirectory={"/home/francois/Documents/git/Purecontrol/openmodelica-python-gym/motor_model/"},
  IncludeDirectory={"/home/francois/Documents/git/Purecontrol/openmodelica-python-gym/openmodelica_python_gym/external_lib/grpc_interface"});
  end grpcInterface;



  Real t(start=0);   
    equation
    when { sampleTrigger } then
        grpcInterface(t, u, input_labels, output_labels, samplePeriod);
    end when;
    der(t) = 1;

end Emitter;