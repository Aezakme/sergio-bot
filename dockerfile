FROM python:3.9.13

WORKDIR /app

COPY . ./

RUN ["pip3", "install", "-r", "requirements.txt"]

CMD ["python", "main.py"]