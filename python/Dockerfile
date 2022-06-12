FROM python:3.8-slim

WORKDIR /app
COPY rest_filter.py rest_filter.py
COPY lib lib
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt
RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "vim"]
ENTRYPOINT ["python3"]
EXPOSE 5559
ENV PYTHONUNBUFFERED=1
CMD ["rest_filter.py"]
