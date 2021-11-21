FROM python:3.6
WORKDIR /web_service
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY server/run.py run.py
COPY server/cas_ops.py cas_ops.py

ENV CONSISTENCY_LEVEL LOCAL_ONE
ENV SERIAL_CONSISTENCY_LEVEL LOCAL_SERIAL
CMD ["python3", "run.py", "--host", "0.0.0.0", "--port", "4000"]