FROM ubuntu

ADD flask /
RUN cd go-ipfs && ./ipfs init

RUN apt-get update -y 
RUN apt-get install -y python3 python3-pip 
RUN pip3 install flask flask_cors ipfsapi umbral

ENTRYPOINT cd go-ipfs && ./ipfs daemon & python3 file_encryption.py
