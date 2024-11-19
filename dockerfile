FROM debian:12

RUN apt-get update -y
#RUN apt-get upgrade -yy
RUN apt-get install -y \
    g++ gcc libxml2-dev \
    libxslt-dev libffi-dev \
    make curl python3 pip \
    vim cron whois


COPY requirements.txt /home/requirements.txt

RUN pip3 install -r /home/requirements.txt \
	--break-system-packages

RUN playwright install
RUN playwright install-deps

# CMD /etc/init.d/cron start

# docker build -t xran .
# docker run -it --network host --name xran1 -v /path/to/xransomware:/home/xransomware xran
