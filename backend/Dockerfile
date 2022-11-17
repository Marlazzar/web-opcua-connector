FROM python:3.10

WORKDIR /code

COPY . ./backend

RUN pip install --no-cache-dir -r ./backend/requirements.txt

EXPOSE 5000

#CMD ["waitress-serve", "--host", "localhost", "--port", "5000", "--call", "backend:create_app"]
CMD ["flask", "--app", "backend", "run", "--host=0.0.0.0", "--port=5000"]

