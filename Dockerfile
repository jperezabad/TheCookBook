FROM python:3.7-alpine
RUN apk add --no-cache gcc musl-dev linux-headers libressl-dev musl-dev libffi-dev
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "wsgy.py"]

