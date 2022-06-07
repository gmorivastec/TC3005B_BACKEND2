FROM python:3

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# para deploy local
#CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "4", "app:app"]

EXPOSE 8000

CMD gunicorn app:app