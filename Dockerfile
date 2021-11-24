FROM python:3.6
WORKDIR /web_service
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY server/run.py run.py
COPY server/cas_ops.py cas_ops.py

ENV CONSISTENCY_LEVEL LOCAL_ONE
ENV SERIAL_CONSISTENCY_LEVEL LOCAL_SERIAL
CMD ["uwsgi",\
         "--http", "0.0.0.0:4000",\
         "--threads", "5",\
         "--manage-script-name",\
         "--mount", "/=run:app"]