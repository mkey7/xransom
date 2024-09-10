# docker build --network host -t ran .
# docker run -it --name ran1 -v /mnt/e/work/ransomware:/home/ransomwatch ran

FROM debian:12

RUN apt-get update -y
#RUN apt-get upgrade -yy
RUN apt-get install -y \
    g++ gcc libxml2-dev \
    libxslt-dev libffi-dev \
    make curl python3 pip \
    vim cron

RUN pip3 install -r /home/requirements.txt \
	--break-system-packages

RUN playwright install
RUN playwright install-deps

# CMD /etc/init.d/cron start
