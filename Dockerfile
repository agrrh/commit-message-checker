FROM python:3.8-slim

RUN apt-get update -qq \
  && apt-get install git -y \
  && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE true
ENV PYTHONUNBUFFERED true

WORKDIR /code

COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

COPY ./ /app

ENTRYPOINT [""]
CMD ["/bin/bash", "-c", "/usr/local/bin/python /app/check.py"]
