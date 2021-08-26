FROM python
COPY . .
RUN apt-get update
RUN apt-get install -y wget git nano htop screen
RUN pip install -r /requirements.txt

CMD python logs.py