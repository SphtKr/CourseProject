FROM python:3.6

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apt-get update &&\
    apt-get install -y bash git gfortran libgfortran5 libopenblas-base libopenblas-dev cmake libmagic1 &&\
    apt-get clean
RUN pip install python-magic bs4 pytoml &&\
    rm -Rf /root/.cache
RUN git clone --recurse-submodules https://github.com/meta-toolkit/metapy.git /tmp/metapy-src &&\
    sed -i 's/http:\/\/download.icu-project.org\/files\/icu4c\/61.1\/icu4c-61_1-src.tgz/https:\/\/github.com\/unicode-org\/icu\/releases\/download\/release-61-1\/icu4c-61_1-src.tgz/g' /tmp/metapy-src/deps/meta/CMakeLists.txt &&\
    pip install /tmp/metapy-src &&\
    rm -Rf /root/.cache &&\
    rm -Rf /tmp/metapy-src

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["/usr/src/app/indexer.py"]