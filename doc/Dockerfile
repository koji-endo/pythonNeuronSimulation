FROM centos:centos6.9
RUN yum install -y gcc gcc-c++ zlib-devel bzip2 bzip2-devel readline readline-devel sqlite sqlite-devel openssl openssl-devel git patch wget openmpi openmpi-devel mpich2 mpich2-devel xorg-x11-apps ImageMagick ImageMagick-devel
RUN git clone https://github.com/pyenv/pyenv.git ~/.pyenv
RUN echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bash_profile
RUN echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
RUN source ~/.bash_profile
RUN pyenv install 2.7.5
RUN pyenv global 2.7.5 && pyenv rehash
RUN pip install numpy matplotlib 
RUN wget https://neuron.yale.edu/ftp/neuron/versions/v7.5/nrn-7.5.tar.gz
RUN tar xvf nrn-7.5.tar.gz
RUN cd nrn-7.5
RUN ./configure --prefix=`pwd` --with-paranrn --with-nrnpython=/root/.pyenv/shims/python && make && make install
RUN cd && git clone https://github.com/Hayato-t/pythonNeuronSimulation.git
