FROM python:3.10-slim

WORKDIR /app
COPY . /app
RUN pip3 install -r /app/requirements.txt --no-cache-dir
RUN echo yes | python3 manage.py collectstatic --noinput

CMD ["gunicorn", "fabrique_mailing.wsgi:application", "--bind", "0:8000" ]