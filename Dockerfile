FROM python:3.8

WORKDIR /app

RUN curl -fsSL https://code-server.dev/install.sh | sh

COPY requirements.txt /app/


RUN pip install --upgrade pip

COPY . /app

EXPOSE 8000 8080

ENTRYPOINT ["code-server", "--bind-addr", "0.0.0.0:8080", "--auth", "none"]
