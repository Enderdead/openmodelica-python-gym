within omc_gym_lib.BaseClasses;

block Receiver
  parameter Integer index=1 "Number of outputs";
    extends DiscreteBlock;
  Modelica.Blocks.Interfaces.RealOutput y "Connector of Real output signals"
    annotation (Placement(transformation(extent={{100,-10},{120,10}})));
    
  function grpcGetter
    input  Real t;
    input  Integer index;    
    output Real y;
    
  external "C" annotation(Library={"-lprotobuf", "-lgrpc", "-lgpr", "-lgrpc++", "grpc_interface"},
  LibraryDirectory={"/home/francois/Documents/git/Purecontrol/openmodelica-python-gym/motor_model/"},
  IncludeDirectory={"/home/francois/Documents/git/Purecontrol/openmodelica-python-gym/openmodelica_python_gym/external_lib/grpc_interface"});
  end grpcGetter;

  Real t(start=0);
    
    equation
    when { sampleTrigger } then
        y = grpcGetter(t, index);
    end when;
    der(t) = 1;

end Receiver;