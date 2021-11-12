from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.install_lib import install_lib

from setuptools.command.install_scripts import install_scripts
import site
import os 
import sys




class ProxyProtobufGenerator(install):
    def run(self):
        prev_dir = os.curdir

        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        if (not os.path.isfile("./bin/generate_protoc.sh")) or (not os.path.isfile("./bin/generate_protoc.sh")):
            sys.stdout.write("\033[31m Can't find bin bash scripts ! \033[0m \n")
            return 

        # Generate protobuf files
        protoc_status = os.system("bash ./bin/generate_protoc.sh")
        
        if protoc_status!=0:
            sys.stdout.write("\033[31m Can't generated protobuf files. Please check your protbuf and grpc installation ! \033[0m \n")
            return

        # Compile library files
        protoc_status = os.system("bash ./bin/compile_libs.sh")
        
        if protoc_status!=0:
            sys.stdout.write("\033[31m Cannot compile cpp libraries. Make sure protobuf and gRPC are correcly installed. \033[0m \n")
            return    
        

        os.chdir(prev_dir)
        install.run(self)



class ProxyProtobufMover(install_lib):
    def run(self):
        prev_dir = os.curdir

        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        os.system("mkdir -p ./build/lib/openmodelica_python_gym/external_lib/grpc_interface/build")
        os.system("cp ./openmodelica_python_gym/external_lib/grpc_interface/build/libgrpc_interface.so ./build/lib/openmodelica_python_gym/external_lib/grpc_interface/build/libgrpc_interface.so")
        os.system("cp ./openmodelica_python_gym/omc_gym_lib/BaseClasses/Emitter.mo ./build/lib/openmodelica_python_gym/omc_gym_lib/BaseClasses/Emitter.mo")
        os.system("cp ./openmodelica_python_gym/omc_gym_lib/BaseClasses/package.mo ./build/lib/openmodelica_python_gym/omc_gym_lib/BaseClasses/package.mo")
        os.system("cp ./openmodelica_python_gym/omc_gym_lib/BaseClasses/package.order ./build/lib/openmodelica_python_gym/omc_gym_lib/BaseClasses/package.order")
        os.system("cp ./openmodelica_python_gym/omc_gym_lib/BaseClasses/Receiver.mo ./build/lib/openmodelica_python_gym/omc_gym_lib/BaseClasses/Receiver.mo")
        os.system("cp ./openmodelica_python_gym/omc_gym_lib/package.mo ./build/lib/openmodelica_python_gym/omc_gym_lib/package.mo")
        os.system("cp ./openmodelica_python_gym/omc_gym_lib/package.order ./build/lib/openmodelica_python_gym/omc_gym_lib/package.order")


        os.chdir(prev_dir)
        install_lib.run(self)



setup(
    name='openmodelica_python_gym',
    version='1.0',
    description='A small library using grpc to communicate with openmodelica process',
    author='François Gauthier-Clerc',
    author_email='francois@gauthier-clerc.fr',
    url="https://github.com/Enderdead/openmodelica-python-gym",
    packages=find_packages(exclude=[])+['openmodelica_python_gym.external_lib.grpc_interface','openmodelica_python_gym.omc_gym_lib.BaseClasses'],
    package_data={'external_lib' : ['grpc_interface/build/libgrpc_interface.so'], "omc_gym_lib" : ["BaseClasses/Emitter.mo"]},
    include_package_data=True,
    install_requires=["grpclib>=0.4.2",
                      "grpcio-tools>=1.32.0",
                      "grpcio-tools>=1.32.0",
                      "protobuf",
                      "OMPython>=3.3.0",
                      "numpy",
                      "gym>=0.17.1"],
    scripts=[],
    cmdclass={'install': ProxyProtobufGenerator, 'install_lib':ProxyProtobufMover },
)
