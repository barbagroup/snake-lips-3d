# Dockerfile for OpenFOAM-v6 with Intel MPI 5.1 on CentOS 7 for use with Batch Shipyard on Azure Batch.
# Based on https://github.com/Azure/batch-shipyard/blob/master/recipes/OpenFOAM-Infiniband-IntelMPI/docker/Dockerfile
# Based on https://github.com/richardlock/docker-openfoam6-paraview54-intelmpi/blob/master/Dockerfile

FROM centos:7.8.2003
MAINTAINER Olivier Mesnard <mesnardo@gwu.edu>

# set up base and ssh keys
COPY ssh_config /root/.ssh/config
RUN yum swap -y fakesystemd systemd && \
    yum install -y epel-release && \
    yum install -y \
        boost-devel cmake3 flex gcc gcc-c++ gnuplot \
        libGLU-devel libXt-devel make man mesa-libGL-devel mpfr-devel \
        ncurses-devel qt-x11 qt4-devel qtwebkit-devel readline-devel zlib-devel && \
    yum install -y \
        openssh-clients openssh-server net-tools \
        libmlx4 librdmacm libibverbs dapl rdma && \
    yum clean all && \
    mkdir -p /var/run/sshd && \
    ssh-keygen -A && \
    sed -i 's/UsePAM yes/UsePAM no/g' /etc/ssh/sshd_config && \
    sed -i 's/#PermitRootLogin yes/PermitRootLogin yes/g' /etc/ssh/sshd_config && \
    sed -i 's/#RSAAuthentication yes/RSAAuthentication yes/g' /etc/ssh/sshd_config && \
    sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/g' /etc/ssh/sshd_config && \
    ssh-keygen -f /root/.ssh/id_rsa -t rsa -N '' && \
    chmod 600 /root/.ssh/config && \
    chmod 700 /root/.ssh && \
    cp /root/.ssh/id_rsa.pub /root/.ssh/authorized_keys

# Configure cmake alias
RUN alternatives --install /usr/local/bin/cmake cmake /usr/bin/cmake3 10 \
        --slave /usr/local/bin/ctest ctest /usr/bin/ctest3 \
        --slave /usr/local/bin/cpack cpack /usr/bin/cpack3 \
        --slave /usr/local/bin/ccmake ccmake /usr/bin/ccmake3 \
        --family cmake

# Download and install Intel MPI Library 5.1.
WORKDIR /tmp
ENV INTEL_DIR=/opt/intel
ENV MPI_ROOT=${INTEL_DIR}/compilers_and_libraries/linux/mpi
RUN curl http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9278/l_mpi_p_5.1.3.223.tgz | tar zxv && \
    cd l_mpi_p_5.1.3.223 && \
    sed -i 's/ACCEPT_EULA=decline/ACCEPT_EULA=accept/' silent.cfg && \
    sed -i 's/ACTIVATION_TYPE=exist_lic/ACTIVATION_TYPE=trial_lic/' silent.cfg && \
    ./install.sh -s silent.cfg && \
    rm -rf \
        /tmp/l_mpi_p_5.1.3.223 \
        /tmp/l_mpi_p_5.1.3.223.tgz \
        /opt/intel/documentation_2016 \
        /opt/intel/ism \
        /opt/intel/parallel_studio_xe_2016.3.068

# Download and build OpenFOAM-v6.
ENV FOAM_INST_DIR=/opt/OpenFOAM
ENV PATH=$PATH:/usr/lib64/qt4/bin
WORKDIR ${FOAM_INST_DIR}
RUN source ${INTEL_DIR}/bin/compilervars.sh intel64 && \
    source ${MPI_ROOT}/bin64/mpivars.sh && \
    curl -L http://dl.openfoam.org/source/6 | tar xvz && \
    curl -L http://dl.openfoam.org/third-party/6 | tar xvz && \
    mv OpenFOAM-6-version-6 OpenFOAM-6 && \
    mv ThirdParty-6-version-6 ThirdParty-6 && \
    OF_BASHRC=${FOAM_INST_DIR}/OpenFOAM-6/etc/bashrc && \
    sed -i 's,FOAM_INST_DIR=$HOME/$WM_PROJECT,FOAM_INST_DIR=/opt/$WM_PROJECT,g' ${OF_BASHRC} && \
    sed -i 's,export WM_MPLIB=SYSTEMOPENMPI,export WM_MPLIB=INTELMPI,g' ${OF_BASHRC} && \
    source ${OF_BASHRC} && \
    ${FOAM_INST_DIR}/ThirdParty-6/Allwmake && \
    ${FOAM_INST_DIR}/ThirdParty-6/makeParaView -config && \
    sed -i '/DOCUMENTATION_DIR "\${CMAKE_CURRENT_SOURCE_DIR}\/doc"/d' /opt/OpenFOAM/ThirdParty-6/ParaView-5.4.0/Plugins/StreamLinesRepresentation/CMakeLists.txt && \
    ${FOAM_INST_DIR}/ThirdParty-6/makeParaView && \
    wmRefresh && \
    ${FOAM_INST_DIR}/OpenFOAM-6/Allwmake -j && \
    # Remove intermediate build files
    rm -rf \
        ${FOAM_INST_DIR}/OpenFOAM-6/platforms/*/applications \
        ${FOAM_INST_DIR}/OpenFOAM-6/platforms/*/src \
        ${FOAM_INST_DIR}/ThirdParty-6/build \
        ${FOAM_INST_DIR}/ThirdParty-6/gcc-* \
        ${FOAM_INST_DIR}/ThirdParty-6/gmp-* \
        ${FOAM_INST_DIR}/ThirdParty-6/mpfr-* \
        ${FOAM_INST_DIR}/ThirdParty-6/binutils-* \
        ${FOAM_INST_DIR}/ThirdParty-6/boost* \
        ${FOAM_INST_DIR}/ThirdParty-6/ParaView-* \
        ${FOAM_INST_DIR}/ThirdParty-6/qt-*

# Set sshd command.
EXPOSE 23
CMD ["/usr/sbin/sshd", "-D", "-p", "23"]
