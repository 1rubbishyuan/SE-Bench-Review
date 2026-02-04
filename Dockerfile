FROM python:3.11-slim

RUN pip install flask -i https://pypi.tuna.tsinghua.edu.cn/simple

WORKDIR /sandbox

COPY zwc /sandbox/zwc

RUN cd zwc && \
    pip install -e . -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY src/evaluation/worker.py /sandbox/worker.py

CMD ["python", "worker.py"]
