FROM python:3.11

WORKDIR /work

COPY requirements.txt /work/

RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt --no-deps --default-timeout=100

COPY script.py /work/

ENTRYPOINT [ "python", "script.py" ]
