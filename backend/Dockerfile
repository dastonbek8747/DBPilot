FROM  python:3.11


WORKDIR /backend


COPY requirements.txt .


RUN pip install -r requirements.txt

COPY backend/ .

EXPOSE 8000

CMD ["python","main.py"]

