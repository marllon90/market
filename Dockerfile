FROM python:latest
RUN apt-get update
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN mkdir -p /app
RUN mkdir -p /app/pip_cache
RUN mkdir -p /app/main
COPY requirements.txt /app/
COPY . /app/main/
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 80
STOPSIGNAL SIGTERM
CMD ["/app/main/server.sh"]