FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y libpq-dev

WORKDIR /student-backend

COPY . .

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Run collectstatic
RUN python manage.py collectstatic --noinput

# Run database migrations
# RUN python manage.py migrate --noinput

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "studentconnect.asgi:application"]
