FROM python:3.13-slim

ENV DJANGO_DEBUG=0

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN chown -R 1000:1000 /app
RUN DJANGO_DEBUG=1 python manage.py collectstatic --noinput
USER 1000

EXPOSE 8000
CMD ["gunicorn", "settings.wsgi:application", "--bind", "0.0.0.0:8000"]