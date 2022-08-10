FROM python:3.9-slim-buster
EXPOSE 8001
RUN useradd -m meteor
USER meteor
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY app/ /app
CMD python -m app
