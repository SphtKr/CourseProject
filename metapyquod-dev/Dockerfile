FROM python:3.6

WORKDIR /usr/src/app

RUN apt-get install bash git
ENV PATH="/root/.local/bin:${PATH}"
RUN pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose pytoml metapy
COPY requirements.txt ./
COPY dot-jupyter /root/.jupyter
RUN pip install --no-cache-dir -r requirements.txt

#COPY . .

EXPOSE 8888/tcp

CMD [ "/bin/bash" ]
