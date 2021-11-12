FROM nvcr.io/nvidia/tensorflow:21.02-tf2-py3 as intermediate

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

RUN apt-get update \
&& export DEBIAN_FRONTEND=noninteractive \
&& apt-get remove -y python3-pip \
&& apt-get install -y python3-pip \
&& apt-get install -y git  openssh-server \
&& /usr/bin/pip3 install   scikit-learn==0.22.2.post1 \
  scikit-optimize==0.7.4  pandas==1.0.5


# Install required packages
RUN apt install htop
RUN python3 -m pip install --user --upgrade pip
RUN python3 -m pip install mpld3 progressbar2 tigramite statsmodels
RUN python3 -m pip install cvxpy
RUN python3 -m pip install jax
RUN python3 -m pip install jaxlib
RUN python3 -m pip install pysindy
RUN apt install -y build-essential pkg-config libssl-dev
RUN apt install -y python-dev cython python-numpy
RUN apt install -y liblapack-dev


# Install modelica
RUN echo "deb http://build.openmodelica.org/apt `lsb_release -cs` release" | tee /etc/apt/sources.list.d/openmodelica.list
RUN wget -q http://build.openmodelica.org/apt/openmodelica.asc -O- | apt-key add - 
#RUN for deb in deb deb-src; do echo "$deb http://build.openmodelica.org/apt `lsb_release -cs release"; done | sudo tee /etc/apt/sources.list.d/openmodelica.list
RUN apt update
RUN apt install -y -q openmodelica
RUN for PKG in `apt-cache search "omlib-.*" | cut -d" " -f1`; do apt-get install -y -q "$PKG"; done 

# Install CMAKE
RUN mkdir -p /root/libs

RUN cd /root/libs \
&& wget https://github.com/Kitware/CMake/releases/download/v3.20.6/cmake-3.20.6.tar.gz \
&& tar -xf cmake-3.20.6.tar.gz \
&& cd /root/libs/cmake-3.20.6 \
&& ./bootstrap \
&& make -j 8 \
&& make install


# Close GRPC lib
RUN cd /root/libs/ \
&& git clone --recurse-submodules -b v1.40.0 https://github.com/grpc/grpc; exit 0


# Install bazel 
RUN cd /root/libs/grpc/third_party/abseil-cpp \
&& mkdir build && cd build \
&& cmake -DBUILD_TESTING=ON -DABSL_USE_GOOGLETEST_HEAD=ON .. \
&& make -j 8 \
&& make install


RUN apt-get install -y -q autoconf
RUN apt-get install -y -q libtool

# Install protobuf
RUN cd /root/libs/grpc/third_party/protobuf \
&& bash ./autogen.sh \
&&  ./configure \
&& make -j 8 \
&& make install \
&& ldconfig


# Install GRPC
RUN cd /root/libs/grpc/ \
&& mkdir -p cmake/build && cd cmake/build \
&&  cmake -DgRPC_INSTALL=ON \
      -DgRPC_BUILD_TESTS=OFF \
      -DCMAKE_INSTALL_PREFIX= \
      -DBUILD_SHARED_LIBS=ON \
      -DgRPC_PROTOBUF_PROVIDER=package \
      ../.. \
&& make -j 8 \
&& make install \
&& ldconfig

RUN python3 -m pip install grpcio-tools==1.32.0

# Put suitable modelica right
RUN useradd modelica
RUN chown modelica:root /usr/bin/omc  && chmod 4755 /usr/bin/omc

# Install OMPython
RUN python3 -m pip install OMPython
RUN python3 -m pip install gym

# clone & install openmodelica gy lib
RUN  cd /root/libs && git clone https://github.com/Enderdead/openmodelica-python-gym.git \
 && cd openmodelica-python-gym && python3 setup.py install && bash ./install_on_docker.sh \
  && python3 -m pip install -r ./requirements.txt



RUN usermod -aG root modelica
ENV PATH="/root/libs/grpc/cmake/build/:/usr/bin/:${PATH}"


# Setup modelica user
RUN mkdir /home/modelica 
RUN chown -R modelica:modelica  /home/modelica

RUN su modelica 
WORKDIR /home/modelica/
