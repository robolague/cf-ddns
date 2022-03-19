FROM python:3.9-alpine

COPY main.py /opt/ddupdate/
#COPY dnslist /etc/ddupdate/
COPY README /opt/ddupdate/

RUN pip3 install requests
#RUN python3 /opt/ddupdate/main.py