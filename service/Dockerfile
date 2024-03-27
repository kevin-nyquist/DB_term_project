FROM python:3.8

WORKDIR /app

RUN apt-get update


COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# EXPOSE 8001

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]