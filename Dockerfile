FROM python:3.11-slim

RUN pip install flask

WORKDIR /sandbox

COPY zwc /sandbox/zwc

RUN cd zwc && \
    pip install -e .

COPY src/evaluation/worker.py /sandbox/worker.py

CMD ["python", "worker.py"]
