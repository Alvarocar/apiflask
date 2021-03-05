FROM python:3.9.1-alpine3.13

LABEL maintainer="brayansuarez123@gmail.com"

ENV MONGO_URI=mongodb://localhost:27017/student

EXPOSE 8080

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "./src/app.py"]