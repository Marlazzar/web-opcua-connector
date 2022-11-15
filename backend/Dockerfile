FROM python:3.10

WORKDIR /code

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["flask", "--app backend --debug run"]


