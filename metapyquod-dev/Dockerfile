FROM python:3.8

WORKDIR /usr/src/app

RUN apt-get update &&\
    apt-get install -y bash git gfortran libgfortran5 libopenblas-base libopenblas-dev cmake &&\
    apt-get clean
ENV PATH="/root/.local/bin:${PATH}"
RUN pip install --extra-index-url=https://www.piwheels.org/simple numpy scipy matplotlib ipython jupyter pandas sympy nose pytoml web-pdb &&\
    rm -Rf /root/.cache
#RUN pip install scipy
#RUN pip install matplotlib 
#RUN pip install --user ipython jupyter pandas sympy nose pytoml web-pdb
#RUN apt-get install cmake -y
#RUN pip install cmake
#RUN curl -L https://github.com/unicode-org/icu/releases/download/release-61-1/icu4c-61_1-src.tgz > /tmp/icu4c-61_1-src.tgz
#RUN mkdir /tmp/icu4c-61_1-src
#RUN tar -xzvf /tmp/icu4c-61_1-src.tgz -C /tmp/icu4c-61_1-src
#RUN pip install --user metapy --install-option="--icu-root=/tmp/icu4c-61_1-src"
RUN git clone --recurse-submodules https://github.com/meta-toolkit/metapy.git /tmp/metapy-src &&\
    sed -i 's/http:\/\/download.icu-project.org\/files\/icu4c\/61.1\/icu4c-61_1-src.tgz/https:\/\/github.com\/unicode-org\/icu\/releases\/download\/release-61-1\/icu4c-61_1-src.tgz/g' /tmp/metapy-src/deps/meta/CMakeLists.txt &&\
    pip install /tmp/metapy-src &&\
    rm -Rf /tmp/metapy-src
COPY requirements.txt ./
COPY dot-jupyter /root/.jupyter
RUN pip install --no-cache-dir -r requirements.txt

#COPY . .

EXPOSE 8888/tcp
EXPOSE 5555/tcp

CMD [ "/bin/bash" ]
