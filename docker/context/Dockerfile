FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y openssh-server  && \
    mkdir /var/run/sshd  && \
    echo 'root:root' |chpasswd
    #sed -ri 's/^PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
    #sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config && \

COPY sshd_config /etc/ssh/sshd_config
COPY requirements.txt ./
RUN mkdir /app
COPY dockerdist/*.py /app/
RUN mkdir /app/google
COPY dockerdist/google /app/google
RUN mkdir /app/face_reco
COPY dockerdist/face_reco /app/face_reco
RUN mkdir /app/extractor
COPY dockerdist/extractor /app/extractor
RUN mkdir /app/samples
COPY dockerdist/samples /app/samples

RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y vim
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install -y python3-pip
RUN apt-get install -y curl
RUN apt-get install -y unzip

RUN pip3 install --no-cache-dir -r requirements.txt

RUN  apt-get -y autoclean && apt-get -y autoremove && \
     apt-get -y purge $(dpkg --get-selections | grep deinstall | sed s/deinstall//g) && \
     rm -rf /var/lib/apt/lists/*

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]